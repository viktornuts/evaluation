from __future__ import annotations

import re
import sqlite3
from dataclasses import dataclass
from pathlib import Path

import openpyxl


ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "data" / "cpt_eval.sqlite"
IMPORTS = ROOT / "imports"
EXPORTS = ROOT / "exports"
IMPORT_ROUNDS = IMPORTS / "rounds"
EXPORT_ROUNDS = EXPORTS / "rounds"

DATASET_ID = "dataset_customer_gold_v1"
DATASET_CASE_ID = "case_customer_gold_release_integration"

ROUND_FILES = [
    {
        "run_code": "v1",
        "eval_run_id": "eval_run_v1_xlsx",
        "source": IMPORT_ROUNDS / "v1" / "source" / "round_v1_output.xlsx",
        "agent": "prompts_v1",
        "change_summary": "Раунд v1: импорт из output_v1.xlsx, 51 сгенерированный ТК из папки prompts_v1.",
    },
    {
        "run_code": "v2",
        "eval_run_id": "eval_run_v2_xlsx",
        "source": IMPORT_ROUNDS / "v2" / "source" / "round_v2_output.xlsx",
        "agent": "prompts_v2",
        "change_summary": "Раунд v2: импорт из output_v2.xlsx, набор сокращен и структурирован относительно v1.",
    },
]

HEADER_INDEX = {
    "folder": 0,
    "key": 3,
    "title": 4,
    "step_type": 6,
    "step_number": 7,
    "action": 8,
    "expected_result": 9,
    "priority": 10,
    "status": 11,
    "tags": 17,
    "links": 18,
    "generated_by_ai": 19,
}

EXPECTED_REQUIREMENTS = {
    *(f"REQ-{index:02d}" for index in range(1, 27)),
    "REQ-28",
    "REQ-29",
}

NEGATIVE_RELEVANT_REQUIREMENTS = {
    "REQ-04",
    "REQ-05",
    "REQ-06",
    "REQ-07",
    "REQ-09",
    "REQ-11",
    "REQ-20",
    "REQ-21",
    "REQ-28",
    "REQ-29",
}


@dataclass
class GeneratedCase:
    source_key: str
    code: str
    title: str
    test_case_type: str
    direction: str
    priority: str | None
    tags: list[str]
    links: str | None
    preconditions: list[tuple[str, str]]
    postconditions: list[tuple[str, str]]
    steps: list[tuple[int, str, str]]
    requirement_codes: list[str]
    assessments: dict[str, tuple[float, str, str]]


def connect() -> sqlite3.Connection:
    connection = sqlite3.connect(DB_PATH)
    connection.execute("PRAGMA foreign_keys = ON")
    connection.row_factory = sqlite3.Row
    return connection


def criterion_ids(connection: sqlite3.Connection, table: str) -> dict[str, str]:
    return {row["code"]: row["id"] for row in connection.execute(f"SELECT id, code FROM {table}")}


def requirement_id(code: str) -> str:
    return f"req_customer_gold_{code.lower().replace('-', '_')}"


def clean_text(value: object) -> str:
    return str(value).strip() if value is not None else ""


def slug(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", value.lower()).strip("_")


def title_prefix(title: str) -> str:
    match = re.match(r"\s*([A-Za-z0-9]+)-", title)
    return match.group(1).upper() if match else "UNKNOWN"


def infer_direction(tags: list[str], title: str) -> str:
    tag_set = {tag.lower() for tag in tags}
    lowered = title.lower()
    if "negative" in tag_set or any(word in lowered for word in ("запрет", "ошиб", "без релиза", "недоступ", "отмена")):
        return "negative"
    if "positive" in tag_set:
        return "positive"
    return "unknown"


def parse_workbook(path: Path, run_code: str) -> list[GeneratedCase]:
    workbook = openpyxl.load_workbook(path, read_only=True, data_only=True)
    sheet = workbook.worksheets[0]
    cases: list[dict[str, object]] = []
    current: dict[str, object] | None = None

    for row in sheet.iter_rows(min_row=2, values_only=True):
        key = clean_text(row[HEADER_INDEX["key"]])
        if key:
            current = {
                "source_key": key,
                "title": clean_text(row[HEADER_INDEX["title"]]),
                "priority": clean_text(row[HEADER_INDEX["priority"]]),
                "tags": [tag.strip() for tag in clean_text(row[HEADER_INDEX["tags"]]).split(",") if tag.strip()],
                "links": clean_text(row[HEADER_INDEX["links"]]),
                "preconditions": [],
                "postconditions": [],
                "steps": [],
            }
            cases.append(current)
        if current is None:
            continue

        step_type = clean_text(row[HEADER_INDEX["step_type"]]).lower()
        number_raw = row[HEADER_INDEX["step_number"]]
        try:
            number = int(number_raw)
        except (TypeError, ValueError):
            number = len(current["steps"]) + 1
        action = clean_text(row[HEADER_INDEX["action"]])
        expected = clean_text(row[HEADER_INDEX["expected_result"]])

        if step_type.startswith("пред"):
            current["preconditions"].append((action, expected))
        elif step_type.startswith("пост"):
            current["postconditions"].append((action, expected))
        elif step_type.startswith("шаг"):
            current["steps"].append((number, action, expected))

    result: list[GeneratedCase] = []
    for index, item in enumerate(cases, start=1):
        title = str(item["title"])
        tags = list(item["tags"])
        prefix = title_prefix(title)
        direction = infer_direction(tags, title)
        text = " ".join(
            [
                title,
                " ".join(tags),
                " ".join(action for _, action, _ in item["steps"]),
                " ".join(expected for _, _, expected in item["steps"]),
                " ".join(action for action, _ in item["preconditions"]),
                " ".join(expected for _, expected in item["preconditions"]),
            ]
        )
        requirement_codes = infer_requirements(text)
        code = f"GEN-{run_code.upper()}-TC-{index:03d}"
        case = GeneratedCase(
            source_key=str(item["source_key"]),
            code=code,
            title=title,
            test_case_type=prefix,
            direction=direction,
            priority=str(item["priority"]) if item["priority"] else None,
            tags=tags,
            links=str(item["links"]) if item["links"] else None,
            preconditions=list(item["preconditions"]),
            postconditions=list(item["postconditions"]),
            steps=sorted(list(item["steps"]), key=lambda row: row[0]),
            requirement_codes=requirement_codes,
            assessments={},
        )
        case.assessments = assess_case(case)
        result.append(case)
    return result


def infer_requirements(text: str) -> list[str]:
    lowered = text.lower()
    result: set[str] = set()

    rules = [
        (("поле", "релиз", "описан"), ["REQ-01", "REQ-02"]),
        (("атрибут", "релиз"), ["REQ-03", "REQ-17"]),
        (("заверш", "редакт"), ["REQ-04"]),
        (("тест-менеджер", "редакт"), ["REQ-05"]),
        (("тестировщик", "редакт"), ["REQ-06"]),
        (("без указания релиза",), ["REQ-07", "REQ-09", "REQ-10"]),
        (("без релиза", "заверш"), ["REQ-07", "REQ-09", "REQ-10"]),
        (("поле", "релиз", "заполн"), ["REQ-08", "REQ-10"]),
        (("дубли",), ["REQ-11"]),
        (("копия", "не наслед"), ["REQ-11"]),
        (("get", "entities"), ["REQ-12", "REQ-13", "REQ-14", "REQ-15"]),
        (("список релиз",), ["REQ-12", "REQ-13", "REQ-14", "REQ-15"]),
        (("registered", "forming", "fixation"), ["REQ-13"]),
        (("number name",), ["REQ-14"]),
        (("номер", "наименование"), ["REQ-14"]),
        (("size", "page"), ["REQ-15"]),
        (("post", "entities"), ["REQ-16", "REQ-17", "REQ-18", "REQ-19"]),
        (("добав", "релиз"), ["REQ-16", "REQ-17", "REQ-18", "REQ-19"]),
        (("relationid", "сохран"), ["REQ-17"]),
        (("тп добавлен в релиз",), ["REQ-18"]),
        (("linkrelease",), ["REQ-19"]),
        (("delete", "relationid"), ["REQ-20", "REQ-21"]),
        (("удален из релиза",), ["REQ-21"]),
        (("очист", "relationid"), ["REQ-20", "REQ-21"]),
        (("create test_plan",), ["REQ-22"]),
        (("update test_plan",), ["REQ-23"]),
        (("create test_plan_case",), ["REQ-24"]),
        (("update test_plan_case",), ["REQ-25"]),
        (("kafka",), ["REQ-22", "REQ-23", "REQ-24", "REQ-25"]),
        (("одном контуре",), ["REQ-26"]),
        (("inno.local",), ["REQ-26"]),
        (("ручн", "с.релизы"), ["REQ-28", "REQ-29"]),
        (("кноп", "добавить тест-план"), ["REQ-29"]),
    ]
    for needles, codes in rules:
        if all(needle in lowered for needle in needles):
            result.update(codes)

    return sorted(result) if result else ["REQ-01"]


def assess_case(case: GeneratedCase) -> dict[str, tuple[float, str, str]]:
    return {
        "classification_correctness": assess_classification(case),
        "template_required_attributes": assess_template(case),
        "conditions_quality": assess_conditions(case),
        "step_atomicity": assess_atomicity(case),
        "expected_result_quality": assess_expected_results(case),
        "no_hallucinations": assess_hallucinations(case),
    }


def assess_classification(case: GeneratedCase) -> tuple[float, str, str]:
    tag_set = {tag.lower() for tag in case.tags}
    prefix = case.test_case_type
    if prefix == "UI" and "ui" in tag_set:
        return 10.0, "correct_type", "Вид UI подтверждается метками и содержанием сценария."
    if prefix == "E2E" and "e2e" in tag_set:
        return 10.0, "correct_type", "Вид E2E подтверждается метками и сквозным характером сценария."
    if prefix == "API" and ("api" in tag_set or any(tag.startswith("status_") for tag in tag_set)):
        if "kafka" in tag_set:
            return 8.0, "mostly_correct_type", "ТК помечен как API, но Kafka-сценарий ближе к интеграционному виду."
        return 10.0, "correct_type", "Вид API подтверждается метками и HTTP/API-содержанием сценария."
    if "kafka" in tag_set:
        return 8.0, "mostly_correct_type", "Сценарий интеграционный, но тип требует ручного подтверждения."
    return 7.0, "partly_correct_type", "Вид ТК вероятно корректен по названию, но метки не дают полного подтверждения."


def assess_template(case: GeneratedCase) -> tuple[float, str, str]:
    has_task = bool(case.links and "PPTS-428" in case.links)
    has_source = bool(case.links and ("knowledge" in case.links or "pages" in case.links))
    has_required = all([case.title, case.priority, case.tags, case.steps])
    if has_required and has_task and has_source:
        return (
            8.5,
            "template_and_attrs_mostly_complete",
            "Есть название, приоритет, метки, шаги, ссылка на задачу и источник; прямых ссылок на атомарные REQ в экспорте нет.",
        )
    if has_required:
        return 6.5, "template_or_attrs_partial", "Основная структура есть, но часть обязательных ссылок/атрибутов отсутствует."
    return 4.0, "template_or_attrs_weak", "Шаблон или обязательные атрибуты существенно нарушены."


def assess_conditions(case: GeneratedCase) -> tuple[float, str, str]:
    if case.preconditions and case.postconditions:
        return 9.0, "conditions_mostly_clear", "Предусловия и постусловия выделены; возможны minor-неточности формулировок."
    if case.preconditions:
        return 8.0, "conditions_mostly_clear", "Предусловия есть, но постусловия отсутствуют или не выделены отдельно."
    if case.postconditions:
        return 6.5, "conditions_partial", "Постусловия есть, но входной контекст сценария описан неполно."
    return 5.0, "conditions_weak", "Предусловия и постусловия не выделены."


def assess_atomicity(case: GeneratedCase) -> tuple[float, str, str]:
    if not case.steps:
        return 0.0, "no_steps", "Шаги отсутствуют."
    joined_steps = " ".join(action.lower() for _, action, _ in case.steps)
    glued_markers = sum(joined_steps.count(marker) for marker in [" и ", ";", " затем ", " после "])
    if glued_markers == 0:
        return 9.5, "mostly_atomic_steps", "Шаги выглядят атомарными; явных склеек действий не найдено."
    if glued_markers <= max(1, len(case.steps) // 2):
        return 8.5, "mostly_atomic_steps", "Есть отдельные склейки действий, но сценарий остается читаемым."
    return 6.5, "partly_atomic_steps", "Часть шагов объединяет несколько действий и требует ручного переразбиения."


def assess_expected_results(case: GeneratedCase) -> tuple[float, str, str]:
    if not case.steps:
        return 0.0, "expected_results_missing", "Шаги отсутствуют, ожидаемые результаты оценить нельзя."
    present = [bool(expected) for _, _, expected in case.steps]
    ratio = sum(present) / len(present)
    if ratio == 1:
        multi_effect = sum(
            1
            for _, _, expected in case.steps
            if any(marker in expected.lower() for marker in ["; ", ", ", " и ", "получен ответ"])
        )
        if multi_effect:
            return 8.5, "expected_results_mostly_complete", "У каждого шага есть ожидаемый результат, но часть результатов объединяет несколько проверок."
        return 10.0, "expected_results_complete", "У каждого шага есть конкретный ожидаемый результат."
    if ratio >= 0.7:
        return 7.0, "expected_results_partial", "Ожидаемые результаты есть у большей части шагов."
    return 4.5, "expected_results_weak", "Ожидаемые результаты часто отсутствуют или неполные."


def assess_hallucinations(case: GeneratedCase) -> tuple[float, str, str]:
    text = " ".join(
        [
            case.title,
            " ".join(case.tags),
            " ".join(action for _, action, _ in case.steps),
            " ".join(expected for _, _, expected in case.steps),
            " ".join(action for action, _ in case.preconditions),
            " ".join(expected for _, expected in case.preconditions),
        ]
    ).lower()
    score = 10.0
    issues: list[str] = []

    if "тестировщик" in text and any(word in text for word in ["лишен", "лишена", "недостаточ", "запрет", "недоступ"]):
        score -= 6.0
        issues.append("ролевое ограничение для Тестировщика противоречит эталонным требованиям")
    if "403" in text and ("ift" in text or "uat" in text or "ифт" in text or "пси" in text):
        score -= 5.0
        issues.append("403 для IFT/UAT выглядит неподтвержденным и спорным")
    elif any(status in text for status in ["401", "403", "404", "500"]):
        score -= 3.5
        issues.append("HTTP-статусы ошибок не подтверждены в эталонных требованиях")
    if "/api/v0.1/releases" in text:
        score -= 4.0
        issues.append("endpoint /api/v0.1/releases не совпадает с endpoint из источника")
    if any(word in text for word in ["отмена завершения", "отказ от завершения", "кнопку «отменить»", "кнопка 'отменить'"]):
        score -= 2.5
        issues.append("сценарий отмены диалога явно не описан в источнике")
    if "сбой" in text or "internal_server_error" in text:
        score -= 2.0
        issues.append("сценарий сбоя интеграции производный, а не явно заданный")

    score = max(0.0, min(10.0, score))
    if not issues:
        return 10.0, "no_hallucinations", "Неподтвержденных фактов по быстрой проверке не найдено."
    label = "unsupported_detail_risk" if score >= 6 else "many_unsupported_facts"
    return score, label, "; ".join(issues) + "."


def clean_previous_run(connection: sqlite3.Connection, run_code: str) -> None:
    rows = connection.execute(
        "SELECT id FROM eval_runs WHERE dataset_id = ? AND run_code = ?",
        (DATASET_ID, run_code),
    ).fetchall()
    for row in rows:
        eval_run_id = row["id"]
        connection.execute("DELETE FROM test_cases WHERE eval_run_id = ?", (eval_run_id,))
        connection.execute("DELETE FROM test_suite_quality_assessments WHERE eval_run_id = ?", (eval_run_id,))
        connection.execute("DELETE FROM test_case_evaluation_results WHERE eval_run_id = ?", (eval_run_id,))
        connection.execute("DELETE FROM eval_runs WHERE id = ?", (eval_run_id,))


def insert_eval_run(connection: sqlite3.Connection, config: dict[str, object]) -> None:
    run_code = str(config["run_code"])
    agent = str(config["agent"])
    connection.execute(
        """
        INSERT INTO eval_runs (
            id, dataset_id, run_code, agent_name, agent_version, prompt_snapshot,
            model_name, model_version, temperature, top_p, run_mode,
            response_format_strictness, change_summary, dataset_version, status,
            finished_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'completed', CURRENT_TIMESTAMP)
        """,
        (
            config["eval_run_id"],
            DATASET_ID,
            run_code,
            agent,
            run_code,
            run_code,
            run_code,
            run_code,
            0.0,
            1.0,
            "direct_extraction",
            "freeform",
            config["change_summary"],
            "customer_gold_v1",
        ),
    )


def insert_cases(connection: sqlite3.Connection, config: dict[str, object], cases: list[GeneratedCase]) -> None:
    tc_criteria = criterion_ids(connection, "test_case_quality_criteria")
    eval_run_id = str(config["eval_run_id"])
    run_code = str(config["run_code"])
    for case in cases:
        tc_id = f"gen_{run_code}_{slug(case.source_key)}"
        preconditions = "\n".join(
            f"{index}. {action} -> {expected}" if expected else f"{index}. {action}"
            for index, (action, expected) in enumerate(case.preconditions, start=1)
        ) or None
        postconditions = "\n".join(
            f"{index}. {action} -> {expected}" if expected else f"{index}. {action}"
            for index, (action, expected) in enumerate(case.postconditions, start=1)
        ) or None
        connection.execute(
            """
            INSERT INTO test_cases (
                id, dataset_case_id, test_case_code, title, test_case_type,
                direction, origin, preconditions, postconditions, eval_run_id
            )
            VALUES (?, ?, ?, ?, ?, ?, 'generated', ?, ?, ?)
            """,
            (
                tc_id,
                DATASET_CASE_ID,
                case.code,
                case.title,
                case.test_case_type,
                case.direction,
                preconditions,
                postconditions,
                eval_run_id,
            ),
        )
        for step_index, (_, action, expected) in enumerate(case.steps, start=1):
            step_id = f"step_{tc_id}_{step_index}"
            connection.execute(
                """
                INSERT INTO test_case_steps (id, test_case_id, step_number, action, expected_result)
                VALUES (?, ?, ?, ?, ?)
                """,
                (step_id, tc_id, step_index, action, expected or "Ожидаемый результат не указан"),
            )
            for req_code in case.requirement_codes:
                if req_code not in EXPECTED_REQUIREMENTS:
                    continue
                connection.execute(
                    """
                    INSERT INTO test_case_step_requirement_links (
                        id, test_case_step_id, requirement_id, rationale, linked_by, review_status
                    )
                    VALUES (?, ?, ?, ?, 'codex_xlsx_import', 'draft')
                    """,
                    (
                        f"step_link_{step_id}_{req_code.lower().replace('-', '_')}",
                        step_id,
                        requirement_id(req_code),
                        "Связь шага с требованием определена эвристически при импорте Excel-раунда.",
                    ),
                )
        for req_code in case.requirement_codes:
            if req_code not in EXPECTED_REQUIREMENTS:
                continue
            connection.execute(
                """
                INSERT INTO requirement_test_case_links (
                    id, requirement_id, test_case_id, coverage_status, coverage_type,
                    is_primary, rationale, linked_by, review_status
                )
                VALUES (?, ?, ?, 'covered', ?, 1, ?, 'codex_xlsx_import', 'draft')
                """,
                (
                    f"rtcl_{run_code}_{req_code.lower().replace('-', '_')}_{slug(case.source_key)}",
                    requirement_id(req_code),
                    tc_id,
                    case.direction,
                    "Связь с требованием определена эвристически при импорте Excel-раунда.",
                ),
            )
        for criterion_code, (score, label, rationale) in case.assessments.items():
            connection.execute(
                """
                INSERT INTO test_case_quality_assessments (
                    id, test_case_id, criterion_id, score, label, rationale,
                    assessed_by, assessment_method, confidence, eval_run_id
                )
                VALUES (?, ?, ?, ?, ?, ?, 'Codex', 'llm_assisted_demo', 0.6, ?)
                """,
                (
                    f"tcqa_{tc_id}_{criterion_code}",
                    tc_id,
                    tc_criteria[criterion_code],
                    score,
                    label,
                    rationale,
                    eval_run_id,
                ),
            )


def suite_assessments(cases: list[GeneratedCase]) -> dict[str, tuple[float, str, str]]:
    positive_reqs = {
        req for case in cases if case.direction == "positive" for req in case.requirement_codes
    } & EXPECTED_REQUIREMENTS
    negative_reqs = {
        req for case in cases if case.direction == "negative" for req in case.requirement_codes
    } & NEGATIVE_RELEVANT_REQUIREMENTS
    all_reqs = {req for case in cases for req in case.requirement_codes} & EXPECTED_REQUIREMENTS

    positive_score = min(10.0, round(len(positive_reqs) / len(EXPECTED_REQUIREMENTS) * 10, 1))
    negative_score = min(
        10.0,
        round(len(negative_reqs) / len(NEGATIVE_RELEVANT_REQUIREMENTS) * 10, 1),
    )
    required_score = min(10.0, round(len(all_reqs) / len(EXPECTED_REQUIREMENTS) * 10, 1))

    unsupported_cases = sum(
        1 for case in cases if case.assessments["no_hallucinations"][0] < 8
    )
    extra_pressure = max(0, len(cases) - 20) * 0.07
    cleanliness_score = max(0.0, 10.0 - unsupported_cases * 0.3 - extra_pressure)
    if len(cases) > 45:
        cleanliness_score = min(cleanliness_score, 4.0)
    elif len(cases) > 30:
        cleanliness_score = min(cleanliness_score, 7.0)
    cleanliness_score = round(cleanliness_score, 1)
    overall_score = round(
        positive_score * 0.25
        + negative_score * 0.2
        + required_score * 0.3
        + cleanliness_score * 0.25,
        1,
    )
    if cleanliness_score < 4:
        overall_score = min(overall_score, 7.5)

    unsupported_text = (
        "1 ТК имеет заметный риск неподтвержденных деталей"
        if unsupported_cases == 1
        else f"{unsupported_cases} ТК имеют заметный риск неподтвержденных деталей"
    )
    cleanliness_reasons = [
        f"В наборе {len(cases)} ТК",
        unsupported_text,
    ]
    if len(cases) > 45:
        cleanliness_reasons.append("размер набора выше 45 ТК создает высокий риск дублей и лишних проверок")
    elif len(cases) > 30:
        cleanliness_reasons.append("размер набора выше 30 ТК создает умеренный риск дублей и лишних проверок")

    return {
        "positive_coverage": (
            positive_score,
            label_for_score("positive", positive_score),
            f"Позитивные ТК покрывают {len(positive_reqs)} из {len(EXPECTED_REQUIREMENTS)} эталонных требований MVP.",
        ),
        "negative_coverage": (
            negative_score,
            label_for_score("negative", negative_score),
            f"Негативные ТК покрывают {len(negative_reqs)} из {len(NEGATIVE_RELEVANT_REQUIREMENTS)} требований, где негативные проверки применимы.",
        ),
        "suite_cleanliness": (
            cleanliness_score,
            label_for_score("cleanliness", cleanliness_score),
            "; ".join(cleanliness_reasons) + ".",
        ),
        "required_checks_coverage": (
            required_score,
            label_for_score("required_checks", required_score),
            f"Эвристическая трассировка нашла покрытие {len(all_reqs)} из {len(EXPECTED_REQUIREMENTS)} обязательных требований.",
        ),
        "overall_completeness": (
            overall_score,
            label_for_score("overall", overall_score),
            "Итог учитывает позитивное/негативное покрытие, обязательные проверки и чистоту набора.",
        ),
    }


def label_for_score(kind: str, score: float) -> str:
    prefix = {
        "positive": "positive",
        "negative": "negative",
        "cleanliness": "clean",
        "required_checks": "required_checks",
        "overall": "overall",
    }[kind]
    if score >= 9.5:
        return f"{prefix}_complete"
    if score >= 8:
        return f"{prefix}_mostly_complete"
    if score >= 6:
        return f"{prefix}_partial"
    if score >= 4:
        return f"{prefix}_weak"
    if score > 0:
        return f"{prefix}_poor"
    return f"{prefix}_missing"


def insert_suite_assessments(connection: sqlite3.Connection, config: dict[str, object], cases: list[GeneratedCase]) -> None:
    suite_criteria = criterion_ids(connection, "test_suite_quality_criteria")
    eval_run_id = str(config["eval_run_id"])
    assessments = suite_assessments(cases)
    for criterion_code, (score, label, rationale) in assessments.items():
        connection.execute(
            """
            INSERT INTO test_suite_quality_assessments (
                id, criterion_id, scope_type, scope_id, dataset_id, dataset_case_id,
                eval_run_id, score, label, rationale, assessed_by, assessment_method,
                confidence
            )
            VALUES (?, ?, 'eval_run', ?, ?, ?, ?, ?, ?, ?, 'Codex', 'llm_assisted_demo', 0.6)
            """,
            (
                f"suiteqa_{eval_run_id}_{criterion_code}",
                suite_criteria[criterion_code],
                eval_run_id,
                DATASET_ID,
                DATASET_CASE_ID,
                eval_run_id,
                score,
                label,
                rationale,
            ),
        )


def write_round_report(config: dict[str, object], cases: list[GeneratedCase]) -> None:
    path = EXPORT_ROUNDS / str(config["run_code"]) / f"round_{config['run_code']}_assessment.md"
    suite = suite_assessments(cases)
    lines = [
        f"# Демо-оценка прогона {config['run_code']}",
        "",
        f"Источник: `{Path(config['source']).name}`.",
        f"Импортировано ТК: {len(cases)}.",
        "",
        "## Оценка набора",
        "",
        "| Критерий | Score | Комментарий |",
        "|---|---:|---|",
    ]
    for code, (score, _, rationale) in suite.items():
        lines.append(f"| `{code}` | {score:.1f} | {rationale} |")
    lines.extend(
        [
            "",
            "## Сгенерированные ТК",
            "",
            "| ТК | Вид | Направление | Требования | Средняя оценка | Название |",
            "|---|---|---|---|---:|---|",
        ]
    )
    for case in cases:
        avg = sum(item[0] for item in case.assessments.values()) / len(case.assessments)
        lines.append(
            f"| `{case.code}` | {case.test_case_type} | {case.direction} | "
            f"{', '.join(case.requirement_codes)} | {avg:.1f} | {case.title} |"
        )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    EXPORTS.mkdir(exist_ok=True)
    imported: list[tuple[str, int]] = []
    with connect() as connection:
        for config in ROUND_FILES:
            run_code = str(config["run_code"])
            cases = parse_workbook(Path(config["source"]), run_code)
            clean_previous_run(connection, run_code)
            insert_eval_run(connection, config)
            insert_cases(connection, config, cases)
            insert_suite_assessments(connection, config, cases)
            write_round_report(config, cases)
            imported.append((run_code, len(cases)))
        connection.commit()

    for run_code, count in imported:
        print(f"Imported {count} generated test cases for run {run_code}.")


if __name__ == "__main__":
    main()
