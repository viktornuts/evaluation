from __future__ import annotations

import re
from pathlib import Path

from import_xlsx_eval_rounds import (
    GeneratedCase,
    clean_previous_run,
    connect,
    infer_direction,
    infer_requirements,
    insert_cases,
    insert_eval_run,
    insert_suite_assessments,
    suite_assessments,
)


ROOT = Path(__file__).resolve().parents[1]
SOURCE_PATH = ROOT / "imports" / "rounds" / "v3" / "source" / "tc-export-326428.txt"
REPORT_PATH = ROOT / "exports" / "rounds" / "v3" / "round_v3_assessment.md"

RUN_CONFIG = {
    "run_code": "v3",
    "eval_run_id": "eval_run_v3_txt",
    "source": SOURCE_PATH,
    "agent": "v3",
    "change_summary": (
        "Раунд v3: импорт из txt-экспорта tc-export-326428, 43 сгенерированных ТК. "
        "Файл версии агента, промпты и декомпозиция требований не переданы; параметры агента заполнены заглушками v3."
    ),
}


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


def parse_numbered_section(text: str) -> list[tuple[str, str]]:
    rows: list[tuple[str, str]] = []
    current_action: str | None = None
    current_expected = ""
    for line in text.splitlines():
        match = re.match(r"\s*(?:\[(\d+)\]|\d+\.)\s*(.+)", line)
        if match:
            if current_action is not None:
                rows.append((current_action, current_expected))
            current_action = match.group(2).strip()
            current_expected = ""
            continue
        if current_action is not None and "Ожидаемый результат:" in line:
            current_expected = line.split("Ожидаемый результат:", 1)[1].strip()
        elif current_action is not None and "Результат:" in line:
            current_expected = line.split("Результат:", 1)[1].strip()
    if current_action is not None:
        rows.append((current_action, current_expected))
    return rows


def parse_steps(text: str) -> list[tuple[int, str, str]]:
    rows = parse_numbered_section(text)
    return [(index, action, expected) for index, (action, expected) in enumerate(rows, start=1)]


def infer_case_type(title: str, body: str) -> str:
    text = f"{title} {body}".lower()
    if "e2e" in text or "end-to-end" in text:
        return "E2E"
    if "kafka" in text or "топик" in text or "событ" in text:
        return "INT"
    if any(marker in text for marker in ["api", "post-запрос", "get-запрос", "delete-запрос", "http", "endpoint"]):
        return "API"
    return "UI"


def parse_field(body: str, field: str) -> str:
    match = re.search(rf"(?m)^{re.escape(field)}:\s*(.+)$", body)
    return match.group(1).strip() if match else ""


def split_blocks(text: str) -> list[tuple[str, str]]:
    parts = re.split(r"(?m)^===\s+(.+?)\s+===\s*$", text)
    return [(parts[index].strip(), parts[index + 1]) for index in range(1, len(parts), 2)]


def parse_cases(path: Path) -> list[GeneratedCase]:
    text = path.read_text(encoding="utf-8")
    result: list[GeneratedCase] = []
    for index, (source_key, body) in enumerate(split_blocks(text), start=1):
        title = parse_field(body, "Название")
        priority = parse_field(body, "Приоритет") or None
        tags = [tag.strip() for tag in parse_field(body, "Метки").split(",") if tag.strip()]
        preconditions = parse_numbered_section(section_text(body, "Предусловия", ["Шаги", "Постусловия", "Ссылки"]))
        postconditions = parse_numbered_section(section_text(body, "Постусловия", ["Ссылки"]))
        steps = parse_steps(section_text(body, "Шаги", ["Постусловия", "Ссылки"]))
        links = section_text(body, "Ссылки", []).replace("\n", "; ").strip() or None
        case_type = infer_case_type(title, body)

        classification_tags = list(tags)
        classification_tags.append(case_type.lower())
        direction = infer_direction(classification_tags, title)
        if direction == "unknown":
            direction = "negative" if re.search(r"попытка|ошиб|некоррект|пуст|запрещ|отсутств", title.lower()) else "positive"
        classification_tags.append(direction)

        trace_text = " ".join(
            [
                title,
                body,
                " ".join(action for action, _ in preconditions),
                " ".join(expected for _, expected in preconditions),
                " ".join(action for _, action, _ in steps),
                " ".join(expected for _, _, expected in steps),
            ]
        )
        case = GeneratedCase(
            source_key=source_key,
            code=f"GEN-V3-TC-{index:03d}",
            title=title,
            test_case_type=case_type,
            direction=direction,
            priority=priority,
            tags=classification_tags,
            links=links,
            preconditions=preconditions,
            postconditions=postconditions,
            steps=steps,
            requirement_codes=infer_requirements(trace_text),
            assessments={},
        )
        case.assessments = adjust_assessments(case)
        result.append(case)
    return result


def adjust_assessments(case: GeneratedCase) -> dict[str, tuple[float, str, str]]:
    from import_xlsx_eval_rounds import assess_case

    assessments = assess_case(case)
    title = case.title.lower()
    unsupported_markers = [
        "areaCode".lower(),
        "пустым полем \"name\"",
        "отсутствующим полем \"owner\"",
        "некорректным форматом json",
    ]
    if any(marker in title for marker in unsupported_markers):
        assessments["no_hallucinations"] = (
            3.0,
            "many_unsupported_facts",
            "Сценарий проверяет поля/ошибки или техническое поведение, которые не заданы в эталонных требованиях.",
        )
    if not case.links:
        assessments["template_required_attributes"] = (
            6.0,
            "template_or_attrs_partial",
            "Основная структура есть, но ссылка на источник/задачу отсутствует.",
        )
    return assessments


def write_round_report(cases: list[GeneratedCase]) -> None:
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    suite = suite_assessments(cases)
    lines = [
        "# Демо-оценка прогона v3",
        "",
        "Источник: `tc-export-326428.txt`.",
        f"Импортировано ТК: {len(cases)}.",
        "Файл версии агента, промпты и декомпозиция требований не переданы; в `eval_runs` проставлены заглушки `v3`.",
        "Метки экспорта содержат только `AI_gen`, поэтому вид и направление ТК определены эвристически по названию и шагам.",
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
            "| ТК | Исходный ключ | Вид | Направление | Требования | Средняя оценка | Название |",
            "|---|---|---|---|---|---:|---|",
        ]
    )
    for case in cases:
        avg = sum(item[0] for item in case.assessments.values()) / len(case.assessments)
        lines.append(
            f"| `{case.code}` | `{case.source_key}` | {case.test_case_type} | {case.direction} | "
            f"{', '.join(case.requirement_codes)} | {avg:.1f} | {case.title} |"
        )
    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    cases = parse_cases(SOURCE_PATH)
    with connect() as connection:
        clean_previous_run(connection, "v3")
        insert_eval_run(connection, RUN_CONFIG)
        insert_cases(connection, RUN_CONFIG, cases)
        insert_suite_assessments(connection, RUN_CONFIG, cases)
        connection.commit()
    write_round_report(cases)
    print(f"Imported {len(cases)} generated test cases for run v3.")
    print(f"Wrote {REPORT_PATH}")


if __name__ == "__main__":
    main()
