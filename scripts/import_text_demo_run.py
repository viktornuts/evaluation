from __future__ import annotations

import re
import sqlite3
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "data" / "cpt_eval.sqlite"
SOURCE_PATH = ROOT / "imports" / "rounds" / "v0" / "source" / "round_v1_generated_test_cases.txt"
REPORT_PATH = ROOT / "exports" / "rounds" / "v0" / "round_v0_assessment.md"

DATASET_ID = "dataset_customer_gold_v1"
DATASET_CASE_ID = "case_customer_gold_release_integration"
EVAL_RUN_ID = "eval_run_v0_text_demo"
RUN_CODE = "v0"


@dataclass
class GeneratedTestCase:
    source_id: str
    code: str
    title: str
    priority: str
    tags: list[str]
    test_case_type: str
    direction: str
    preconditions: str | None
    postconditions: str | None
    steps: list[dict[str, object]]
    requirement_codes: list[str]
    assessments: dict[str, tuple[float, str, str]]


REQUIREMENT_LINKS: dict[int, list[str]] = {
    1: ["REQ-12", "REQ-14"],
    2: ["REQ-06", "REQ-12", "REQ-13"],
    3: ["REQ-16", "REQ-17", "REQ-18"],
    4: ["REQ-11"],
    5: ["REQ-09"],
    6: ["REQ-09", "REQ-10"],
    7: ["REQ-07", "REQ-09"],
    8: ["REQ-08", "REQ-10"],
    9: ["REQ-04"],
    10: ["REQ-04", "REQ-05"],
    11: ["REQ-03"],
    12: ["REQ-01", "REQ-02"],
    13: ["REQ-11"],
    14: ["REQ-04", "REQ-05", "REQ-06"],
    15: ["REQ-04"],
    16: ["REQ-08", "REQ-10"],
    17: ["REQ-07", "REQ-09", "REQ-10"],
    18: ["REQ-28", "REQ-29"],
    19: ["REQ-22", "REQ-23", "REQ-24", "REQ-25"],
    20: ["REQ-20", "REQ-21"],
    21: ["REQ-17"],
    22: ["REQ-16", "REQ-17"],
    23: ["REQ-12", "REQ-14"],
    24: ["REQ-12", "REQ-13", "REQ-14"],
}

NO_HALLUCINATION_SCORES: dict[int, tuple[float, str]] = {
    1: (9.0, "Формат релиза следует из ТЗ; UI-сценарий релевантен."),
    2: (9.0, "Список статусов соответствует ТЗ; сценарий связан с ролью Тестировщик."),
    3: (8.0, "Сценарий релевантен, но объединяет выбор релиза, сохранение relationId и сообщение."),
    4: (10.0, "Проверка наследования поля Релиз напрямую следует из ТЗ."),
    5: (4.0, "Поведение кнопки Отменить явно не описано в ТЗ; это производная проверка."),
    6: (9.0, "Подтверждение завершения без релиза соответствует описанному диалогу."),
    7: (10.0, "Диалог подтверждения и его текст соответствуют ТЗ."),
    8: (10.0, "Завершение при заполненном Релизе соответствует ТЗ."),
    9: (10.0, "Недоступность редактирования в статусе Завершен следует из ТЗ."),
    10: (9.0, "Редактирование в активном статусе релевантно, но проверяет только одну роль."),
    11: (10.0, "Отображение поля в разделе Атрибуты соответствует ТЗ."),
    12: (10.0, "Положение поля на форме создания соответствует ТЗ."),
    13: (5.0, "Проверка релевантна, но endpoint duplicate и HTTP 201 в ТЗ не заданы."),
    14: (5.0, "Права редактирования релевантны, но API обновления ТП в таком виде не подтвержден ТЗ."),
    15: (5.0, "Ограничение релевантно, но HTTP 400 и API-метод не заданы в ТЗ."),
    16: (5.0, "Поведение релевантно, но status endpoint в ТЗ не описан."),
    17: (5.0, "Подтверждение релевантно, но API-статусный сценарий и HTTP 200 не описаны в ТЗ."),
    18: (6.0, "Запрет ручного добавления есть в ТЗ, но HTTP 403 для POST не задан."),
    19: (7.0, "Kafka-события есть в ТЗ, но конкретный API-вызов сформулирован обобщенно."),
    20: (10.0, "DELETE по relationId и 204 напрямую описаны в ТЗ."),
    21: (9.0, "Сохранение release и relationId соответствует ТЗ."),
    22: (9.0, "POST добавления ТП в релиз соответствует ТЗ."),
    23: (4.0, "Используется endpoint /api/v0.1/releases, тогда как в ТЗ приведен запрос entities."),
    24: (4.0, "Используется endpoint /api/v0.1/releases и иной формат фильтрации, чем в ТЗ."),
}


def split_blocks(text: str) -> list[tuple[str, str]]:
    parts = re.split(r"(?m)^=== ([0-9a-f-]{36}) ===\s*$", text)
    blocks = []
    for index in range(1, len(parts), 2):
        blocks.append((parts[index], parts[index + 1]))
    return blocks


def section_text(body: str, section: str, next_sections: list[str]) -> str:
    start = body.find(f"{section}:")
    if start == -1:
        return ""
    start += len(section) + 1
    end = len(body)
    for next_section in next_sections:
        position = body.find(f"{next_section}:", start)
        if position != -1:
            end = min(end, position)
    return body[start:end].strip()


def parse_numbered_conditions(text: str) -> str | None:
    if not text:
        return None
    lines = [line.rstrip() for line in text.splitlines() if line.strip()]
    result: list[str] = []
    current: list[str] = []
    for line in lines:
        number_match = re.match(r"\s*\d+\.\s*(.+)", line)
        if number_match:
            if current:
                result.append(" ".join(current))
            current = [number_match.group(1).strip()]
        else:
            stripped = line.strip()
            if stripped.startswith("Ожидаемый результат:"):
                stripped = stripped.replace("Ожидаемый результат:", "Ожидаемый результат:", 1).strip()
            current.append(stripped)
    if current:
        result.append(" ".join(current))
    return "\n".join(f"{index}. {item}" for index, item in enumerate(result, start=1)) if result else None


def parse_steps(text: str) -> list[dict[str, object]]:
    steps: list[dict[str, object]] = []
    current: dict[str, object] | None = None
    for line in text.splitlines():
        step_match = re.match(r"\s*\[(\d+)\]\s*(.+)", line)
        if step_match:
            if current:
                steps.append(current)
            current = {
                "step_number": int(step_match.group(1)),
                "action": step_match.group(2).strip(),
                "expected_result": "",
            }
            continue
        if current and "Результат:" in line:
            current["expected_result"] = line.split("Результат:", 1)[1].strip()
    if current:
        steps.append(current)
    return steps


def infer_type(tags: list[str], steps: list[dict[str, object]]) -> str:
    has_api_step = any(
        str(step["action"]).upper().startswith(("GET ", "POST ", "DELETE ", "PUT ", "PATCH "))
        for step in steps
    )
    if "kafka" in tags:
        return "INT"
    if "api" in tags or has_api_step:
        return "API"
    return "WEB"


def infer_direction(tags: list[str]) -> str:
    if "negative" in tags:
        return "negative"
    if "positive" in tags:
        return "positive"
    return "unknown"


def base_assessments(index: int, tc_type: str, direction: str) -> dict[str, tuple[float, str, str]]:
    no_hall_score, no_hall_rationale = NO_HALLUCINATION_SCORES[index]
    classification_score = 10.0
    classification_rationale = "Метки и фактический шаг согласованы с определенным видом и направлением ТК."
    if index == 19:
        classification_score = 8.0
        classification_rationale = "Kafka-сценарий помечен как api, но по смыслу это интеграционный ТК."

    return {
        "classification_correctness": (
            classification_score,
            "classification_ok" if classification_score >= 9 else "classification_minor_issue",
            classification_rationale,
        ),
        "template_required_attributes": (
            5.0,
            "missing_requirement_links",
            "В человекочитаемом экспорте есть название, метки, предусловия и шаги, но нет явных ссылок на требования и задачу.",
        ),
        "conditions_quality": (
            8.0,
            "conditions_mostly_clear",
            "Предусловия заданы, но постусловия почти везде отсутствуют или не выделены отдельно.",
        ),
        "step_atomicity": (
            9.0,
            "mostly_atomic_steps",
            "Шаги в основном атомарны; часть проверок объединяет несколько последствий в одном ожидаемом результате.",
        ),
        "expected_result_quality": (
            8.5,
            "expected_results_mostly_complete",
            "У каждого шага есть ожидаемый результат, но часть результатов объединяет несколько проверок или содержит техническую конкретику без отдельной трассировки.",
        ),
        "no_hallucinations": (
            no_hall_score,
            "no_hallucinations" if no_hall_score >= 9 else "unsupported_detail_risk",
            no_hall_rationale,
        ),
    }


def parse_test_cases() -> list[GeneratedTestCase]:
    text = SOURCE_PATH.read_text(encoding="utf-8")
    result: list[GeneratedTestCase] = []
    for index, (source_id, body) in enumerate(split_blocks(text), start=1):
        lines = [line.rstrip() for line in body.strip().splitlines() if line.strip()]
        title = lines[0].split(":", 1)[1].strip()
        priority = lines[1].split(":", 1)[1].strip()
        tags = [tag.strip() for tag in lines[2].split(":", 1)[1].split(",")]
        preconditions = parse_numbered_conditions(
            section_text(body, "Предусловия", ["Шаги", "Постусловия"])
        )
        postconditions = parse_numbered_conditions(section_text(body, "Постусловия", []))
        steps = parse_steps(section_text(body, "Шаги", ["Постусловия"]))
        tc_type = infer_type(tags, steps)
        direction = infer_direction(tags)
        result.append(
            GeneratedTestCase(
                source_id=source_id,
                code=f"GEN-V0-TC-{index:03d}",
                title=title,
                priority=priority,
                tags=tags,
                test_case_type=tc_type,
                direction=direction,
                preconditions=preconditions,
                postconditions=postconditions,
                steps=steps,
                requirement_codes=REQUIREMENT_LINKS[index],
                assessments=base_assessments(index, tc_type, direction),
            )
        )
    return result


def connect() -> sqlite3.Connection:
    connection = sqlite3.connect(DB_PATH)
    connection.execute("PRAGMA foreign_keys = ON")
    connection.row_factory = sqlite3.Row
    return connection


def criterion_ids(connection: sqlite3.Connection, table: str) -> dict[str, str]:
    return {row["code"]: row["id"] for row in connection.execute(f"SELECT id, code FROM {table}")}


def requirement_id(code: str) -> str:
    return f"req_customer_gold_{code.lower().replace('-', '_')}"


def test_case_id(code: str) -> str:
    return f"gen_v0_{code.lower().replace('-', '_')}"


def clean_previous_run(connection: sqlite3.Connection) -> None:
    connection.execute("DELETE FROM test_suite_quality_assessments WHERE eval_run_id = ?", (EVAL_RUN_ID,))
    connection.execute(
        "DELETE FROM test_case_evaluation_results WHERE eval_run_id = ?",
        (EVAL_RUN_ID,),
    )
    connection.execute("DELETE FROM test_cases WHERE eval_run_id = ?", (EVAL_RUN_ID,))
    connection.execute("DELETE FROM eval_runs WHERE id = ?", (EVAL_RUN_ID,))


def insert_eval_run(connection: sqlite3.Connection) -> None:
    connection.execute(
        """
        INSERT INTO eval_runs (
            id, dataset_id, run_code, agent_name, agent_version, prompt_snapshot,
            model_name, model_version, temperature, top_p, run_mode,
            response_format_strictness, change_summary, dataset_version, status,
            finished_at
        )
        VALUES (
            :id, :dataset_id, :run_code, :agent_name, :agent_version, :prompt_snapshot,
            :model_name, :model_version, :temperature, :top_p, :run_mode,
            :response_format_strictness, :change_summary, :dataset_version, :status,
            CURRENT_TIMESTAMP
        )
        """,
        {
            "id": EVAL_RUN_ID,
            "dataset_id": DATASET_ID,
            "run_code": RUN_CODE,
            "agent_name": "text_demo",
            "agent_version": "v0",
            "prompt_snapshot": "v0",
            "model_name": "v0",
            "model_version": "v0",
            "temperature": 0.0,
            "top_p": 1.0,
            "run_mode": "direct_extraction",
            "response_format_strictness": "freeform",
            "change_summary": "Тестовый демо-прогон v0: человекочитаемый экспорт ТК, без полных данных об агенте, промпте и декомпозиции.",
            "dataset_version": "customer_gold_v1",
            "status": "completed",
        },
    )


def insert_test_cases(connection: sqlite3.Connection, test_cases: list[GeneratedTestCase]) -> None:
    tc_criteria = criterion_ids(connection, "test_case_quality_criteria")
    for tc in test_cases:
        tc_id = test_case_id(tc.code)
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
                tc.code,
                tc.title,
                tc.test_case_type,
                tc.direction,
                tc.preconditions,
                tc.postconditions,
                EVAL_RUN_ID,
            ),
        )
        for step in tc.steps:
            step_id = f"step_{tc_id}_{step['step_number']}"
            connection.execute(
                """
                INSERT INTO test_case_steps (id, test_case_id, step_number, action, expected_result)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    step_id,
                    tc_id,
                    step["step_number"],
                    step["action"],
                    step["expected_result"],
                ),
            )
            for req_code in tc.requirement_codes:
                connection.execute(
                    """
                    INSERT INTO test_case_step_requirement_links (
                        id, test_case_step_id, requirement_id, rationale, linked_by, review_status
                    )
                    VALUES (?, ?, ?, ?, 'codex_demo_assessment', 'draft')
                    """,
                    (
                        f"step_link_{step_id}_{req_code.lower().replace('-', '_')}",
                        step_id,
                        requirement_id(req_code),
                        "Связь шага унаследована от ручной демо-разметки сгенерированного ТК.",
                    ),
                )
        for req_code in tc.requirement_codes:
            connection.execute(
                """
                INSERT INTO requirement_test_case_links (
                    id, requirement_id, test_case_id, coverage_status, coverage_type,
                    is_primary, rationale, linked_by, review_status
                )
                VALUES (?, ?, ?, 'covered', ?, 1, ?, 'codex_demo_assessment', 'draft')
                """,
                (
                    f"rtcl_gen_v0_{req_code.lower().replace('-', '_')}_{tc.code.lower().replace('-', '_')}",
                    requirement_id(req_code),
                    tc_id,
                    tc.direction,
                    "Связь с требованием проставлена Codex для демонстрационной оценки v0.",
                ),
            )
        for criterion_code, (score, label, rationale) in tc.assessments.items():
            connection.execute(
                """
                INSERT INTO test_case_quality_assessments (
                    id, test_case_id, criterion_id, score, label, rationale,
                    assessed_by, assessment_method, confidence, eval_run_id
                )
                VALUES (?, ?, ?, ?, ?, ?, 'Codex', 'llm_assisted_demo', 0.65, ?)
                """,
                (
                    f"tcqa_{tc_id}_{criterion_code}",
                    tc_id,
                    tc_criteria[criterion_code],
                    score,
                    label,
                    rationale,
                    EVAL_RUN_ID,
                ),
            )


def insert_suite_assessments(connection: sqlite3.Connection) -> None:
    suite_criteria = criterion_ids(connection, "test_suite_quality_criteria")
    assessments = {
        "positive_coverage": (
            7.0,
            "positive_partial",
            "Позитивные сценарии покрывают значимую часть эталона, но нет явного покрытия size/page, одного контура и полноценного E2E-сценария.",
        ),
        "negative_coverage": (
            6.0,
            "negative_partial",
            "Есть негативные UI/API проверки, но часть негативов производная или не подтверждена ТЗ.",
        ),
        "suite_cleanliness": (
            4.0,
            "weak_cleanliness",
            "Набор раздроблен на 24 одношаговых ТК, есть дубли UI/API и проверки вне явно заданных endpoint в ТЗ.",
        ),
        "required_checks_coverage": (
            6.5,
            "required_checks_partial",
            "Часть обязательных проверок покрыта, но отсутствуют или слабо покрыты size/page, контурность, полноценная трассировка и часть эталонных комплексных сценариев.",
        ),
        "overall_completeness": (
            6.0,
            "partly_complete_suite",
            "Набор демонстрирует основную возможность генерации ТК, но требует ручной чистки, объединения дублей и проверки трассировки.",
        ),
    }
    for criterion_code, (score, label, rationale) in assessments.items():
        connection.execute(
            """
            INSERT INTO test_suite_quality_assessments (
                id, criterion_id, scope_type, scope_id, dataset_id, dataset_case_id,
                eval_run_id, score, label, rationale, assessed_by, assessment_method,
                confidence
            )
            VALUES (?, ?, 'eval_run', ?, ?, ?, ?, ?, ?, ?, 'Codex', 'llm_assisted_demo', 0.65)
            """,
            (
                f"suiteqa_{EVAL_RUN_ID}_{criterion_code}",
                suite_criteria[criterion_code],
                EVAL_RUN_ID,
                DATASET_ID,
                DATASET_CASE_ID,
                EVAL_RUN_ID,
                score,
                label,
                rationale,
            ),
        )


def write_report(test_cases: list[GeneratedTestCase]) -> None:
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Демо-оценка тестового прогона v0",
        "",
        "Данные об агенте, модели и промпте отсутствуют; в `eval_runs` проставлены заглушки `v0`.",
        "",
        "## Сгенерированные ТК",
        "",
        "| ТК | Вид | Направление | Требования | Средняя оценка ТК | Название |",
        "|---|---|---|---|---:|---|",
    ]
    for tc in test_cases:
        avg_score = sum(value[0] for value in tc.assessments.values()) / len(tc.assessments)
        lines.append(
            f"| `{tc.code}` | {tc.test_case_type} | {tc.direction} | "
            f"{', '.join(tc.requirement_codes)} | {avg_score:.1f} | {tc.title} |"
        )
    lines.extend(
        [
            "",
            "## Оценка набора",
            "",
            "| Критерий | Score | Комментарий |",
            "|---|---:|---|",
            "| `positive_coverage` | 7.0 | Позитивные сценарии покрывают значимую часть эталона, но есть пропуски. |",
            "| `negative_coverage` | 6.0 | Есть негативные проверки, но часть производная или не подтверждена ТЗ. |",
            "| `suite_cleanliness` | 4.0 | Много одношаговых ТК, дубли UI/API, есть проверки вне явно заданных endpoint. |",
            "| `required_checks_coverage` | 6.5 | Часть обязательных проверок покрыта, но не все. |",
            "| `overall_completeness` | 6.0 | Для демонстрации достаточно, для приемки нужна ручная чистка. |",
        ]
    )
    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    test_cases = parse_test_cases()
    with connect() as connection:
        clean_previous_run(connection)
        insert_eval_run(connection)
        insert_test_cases(connection, test_cases)
        insert_suite_assessments(connection)
        connection.commit()
    write_report(test_cases)
    print(f"Imported {len(test_cases)} generated test cases for eval run {RUN_CODE}.")
    print(f"Wrote {REPORT_PATH}")


if __name__ == "__main__":
    main()
