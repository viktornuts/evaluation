from __future__ import annotations

import argparse
import re
import sqlite3
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DB = ROOT / "data" / "cpt_eval.sqlite"
DEFAULT_OUTPUT = ROOT / "exports" / "eval_rounds_report.md"

DATASET_ID = "dataset_customer_gold_v1"

DECOMPOSITION_ROWS = [
    ("decomposition_completeness", "Полнота декомпозиции"),
    ("decomposition_boundaries", "Границы требований"),
    ("requirement_consolidation", "Консолидация требований"),
]

SUITE_ROWS = [
    ("positive_coverage", "Позитивное покрытие"),
    ("negative_coverage", "Негативное покрытие"),
    ("suite_cleanliness", "Чистота набора"),
    ("required_checks_coverage", "Покрытие обязательных проверок"),
    ("overall_completeness", "Общая полнота набора"),
]

TEST_CASE_ROWS = [
    ("classification_correctness", "Корректность вида ТК"),
    ("template_required_attributes", "Шаблон и обязательные атрибуты"),
    ("conditions_quality", "Предусловия и постусловия"),
    ("step_atomicity", "Атомарность шагов"),
    ("expected_result_quality", "Ожидаемый результат"),
    ("no_hallucinations", "Достоверность"),
]


def connect(db_path: Path) -> sqlite3.Connection:
    connection = sqlite3.connect(db_path)
    connection.row_factory = sqlite3.Row
    return connection


def natural_run_key(run: sqlite3.Row) -> tuple[int, str]:
    match = re.search(r"(\d+)", run["run_code"])
    return (int(match.group(1)) if match else 9999, run["run_code"])


def eval_runs(connection: sqlite3.Connection, up_to_run_code: str | None = None) -> list[sqlite3.Row]:
    rows = connection.execute(
        """
        SELECT *
        FROM eval_runs
        WHERE dataset_id = ?
        ORDER BY started_at, run_code
        """,
        (DATASET_ID,),
    ).fetchall()
    sorted_rows = sorted(rows, key=natural_run_key)
    if up_to_run_code is None:
        return sorted_rows
    for index, run in enumerate(sorted_rows):
        if run["run_code"] == up_to_run_code:
            return sorted_rows[: index + 1]
    return sorted_rows


def target_map(connection: sqlite3.Connection, table: str) -> dict[str, str]:
    rows = connection.execute(f"SELECT code, target_display FROM {table}").fetchall()
    return {row["code"]: row["target_display"] or "10" for row in rows}


def suite_scores(connection: sqlite3.Connection, eval_run_id: str) -> dict[str, str]:
    rows = connection.execute(
        """
        SELECT c.code, a.score
        FROM test_suite_quality_assessments a
        JOIN test_suite_quality_criteria c ON c.id = a.criterion_id
        WHERE a.eval_run_id = ?
        """,
        (eval_run_id,),
    ).fetchall()
    return {row["code"]: f"{row['score']:.1f}/10" for row in rows}


def suite_rationales(connection: sqlite3.Connection, eval_run_id: str) -> dict[str, tuple[float, str]]:
    rows = connection.execute(
        """
        SELECT c.code, a.score, a.rationale
        FROM test_suite_quality_assessments a
        JOIN test_suite_quality_criteria c ON c.id = a.criterion_id
        WHERE a.eval_run_id = ?
        ORDER BY c.code
        """,
        (eval_run_id,),
    ).fetchall()
    return {row["code"]: (row["score"], row["rationale"] or "") for row in rows}


def test_case_average_rationales(connection: sqlite3.Connection, eval_run_id: str) -> dict[str, tuple[float, int, float, float]]:
    rows = connection.execute(
        """
        SELECT c.code, AVG(a.score) AS avg_score, COUNT(*) AS count,
               MIN(a.score) AS min_score, MAX(a.score) AS max_score
        FROM test_case_quality_assessments a
        JOIN test_case_quality_criteria c ON c.id = a.criterion_id
        WHERE a.eval_run_id = ?
        GROUP BY c.code
        """,
        (eval_run_id,),
    ).fetchall()
    return {
        row["code"]: (
            row["avg_score"],
            row["count"],
            row["min_score"],
            row["max_score"],
        )
        for row in rows
    }


def test_case_average_scores(connection: sqlite3.Connection, eval_run_id: str) -> dict[str, str]:
    rows = connection.execute(
        """
        SELECT c.code, AVG(a.score) AS avg_score
        FROM test_case_quality_assessments a
        JOIN test_case_quality_criteria c ON c.id = a.criterion_id
        WHERE a.eval_run_id = ?
        GROUP BY c.code
        """,
        (eval_run_id,),
    ).fetchall()
    return {row["code"]: f"{row['avg_score']:.1f}/10" for row in rows}


def decomposition_scores(connection: sqlite3.Connection, eval_run_id: str) -> dict[str, str]:
    rows = connection.execute(
        """
        SELECT c.code, AVG(a.score) AS avg_score
        FROM requirement_decomposition_quality_assessments a
        JOIN requirement_decomposition_quality_criteria c ON c.id = a.criterion_id
        JOIN requirement_decomposition_evaluation_results r
            ON r.id = a.decomposition_evaluation_result_id
        WHERE r.eval_run_id = ?
        GROUP BY c.code
        """,
        (eval_run_id,),
    ).fetchall()
    return {row["code"]: f"{row['avg_score']:.1f}/10" for row in rows}


def generated_case_count(connection: sqlite3.Connection, eval_run_id: str) -> int:
    row = connection.execute(
        "SELECT COUNT(*) AS count FROM test_cases WHERE eval_run_id = ?",
        (eval_run_id,),
    ).fetchone()
    return int(row["count"])


def compact_name_version(name: str | None, version: str | None) -> str:
    values = [value for value in (name, version) if value]
    if not values:
        return "—"
    if len(values) == 2 and values[0] == values[1]:
        return values[0]
    return " ".join(values)


def table_block(
    title: str,
    rows: list[tuple[str, str]],
    targets: dict[str, str],
    run_values: list[dict[str, str]],
) -> list[str]:
    run_headers = [f"Раунд {index}" for index in range(1, len(run_values) + 1)]
    header = ["Критерий", "Цель", "Baseline", *run_headers]
    separator = ["---", "---:", "---:", *(["---:"] * len(run_values))]
    lines = [
        f"## {title}",
        "",
        "| " + " | ".join(header) + " |",
        "| " + " | ".join(separator) + " |",
    ]
    for code, name in rows:
        values = [run_value.get(code, "—") for run_value in run_values]
        lines.append(
            "| "
            + " | ".join([name, targets.get(code, "—"), "—", *values])
            + " |"
        )
    lines.append("")
    return lines


def decomposition_conclusion_block(runs: list[sqlite3.Row]) -> list[str]:
    lines = [
        "### Вывод по блоку декомпозиции",
        "",
    ]
    if not runs:
        lines.append("Данных по прогонам пока нет.")
    else:
        current_run = runs[-1]["run_code"]
        lines.append(
            f"Для текущего раунда `{current_run}` результат декомпозиции требований от агента не импортировался. "
            "На вход отчета передавались только сгенерированные тест-кейсы. "
            "Поэтому критерии `decomposition_completeness`, `decomposition_boundaries` "
            "и `requirement_consolidation` пока не измерялись."
        )
    lines.append("")
    return lines


def run_summary_table(connection: sqlite3.Connection, runs: list[sqlite3.Row]) -> list[str]:
    lines = [
        "## Параметры прогонов",
        "",
        "| Раунд | Run code | ТК | Что изменили | Агент | Модель | Temperature | Top P | Режим |",
        "|---:|---|---:|---|---|---|---:|---:|---|",
    ]
    if not runs:
        lines.append("| 1 | — | — | — | — | — | — | — | — |")
    for index, run in enumerate(runs, start=1):
        lines.append(
            "| "
            f"{index} | "
            f"`{run['run_code']}` | "
            f"{generated_case_count(connection, run['id'])} | "
            f"{run['change_summary'] or '—'} | "
            f"{compact_name_version(run['agent_name'], run['agent_version'])} | "
            f"{compact_name_version(run['model_name'], run['model_version'])} | "
            f"{run['temperature']} | "
            f"{run['top_p']} | "
            f"{run['run_mode']} |"
        )
    lines.append("")
    return lines


def suite_conclusion_block(connection: sqlite3.Connection, runs: list[sqlite3.Row]) -> list[str]:
    lines = [
        "### Вывод по блоку набора ТК",
        "",
        "| Раунд | Критерий | Score | Почему такая оценка |",
        "|---:|---|---:|---|",
    ]
    if not runs:
        lines.append("| — | — | — | Данных по прогонам пока нет. |")
        lines.append("")
        return lines

    run = runs[-1]
    round_index = len(runs)
    rationales = suite_rationales(connection, run["id"])
    for code, name in SUITE_ROWS:
        if code not in rationales:
            continue
        score, rationale = rationales[code]
        lines.append(f"| {round_index} | {name} | {score:.1f}/10 | {rationale} |")
    lines.append("")
    return lines


def test_case_reason(code: str, avg_score: float, count: int, min_score: float, max_score: float) -> str:
    if code == "classification_correctness":
        return (
            f"Среднее по {count} ТК: типы в основном совпадают с названиями/метками; "
            "снижение связано со спорными API/Kafka или E2E-классификациями."
        )
    if code == "template_required_attributes":
        return (
            f"Среднее по {count} ТК: структура есть, но часть экспортов не содержит прямых ссылок "
            "на атомарные требования, поэтому оценка ниже целевых 100%."
        )
    if code == "conditions_quality":
        return (
            f"Среднее по {count} ТК: предусловия в основном есть, но постусловия часто отсутствуют "
            "или не выделены отдельно."
        )
    if code == "step_atomicity":
        return (
            f"Среднее по {count} ТК: шаги в основном атомарны; отдельные снижения связаны со склейкой "
            "нескольких действий или проверок в одном шаге."
        )
    if code == "expected_result_quality":
        return (
            f"Среднее по {count} ТК: ожидаемые результаты заполнены, но часть результатов объединяет "
            "несколько проверок или требует уточнения."
        )
    if code == "no_hallucinations":
        return (
            f"Среднее по {count} ТК: диапазон оценок {min_score:.1f}-{max_score:.1f}; снижение связано "
            "с неподтвержденными endpoint/status/role деталями и производными сценариями."
        )
    return f"Среднее по {count} ТК: {avg_score:.1f}/10."


def test_case_conclusion_block(connection: sqlite3.Connection, runs: list[sqlite3.Row]) -> list[str]:
    lines = [
        "### Вывод по блоку отдельных ТК",
        "",
        "| Раунд | Критерий | Score | Почему такая оценка |",
        "|---:|---|---:|---|",
    ]
    if not runs:
        lines.append("| — | — | — | Данных по прогонам пока нет. |")
        lines.append("")
        return lines

    run = runs[-1]
    round_index = len(runs)
    rationales = test_case_average_rationales(connection, run["id"])
    for code, name in TEST_CASE_ROWS:
        if code not in rationales:
            continue
        avg_score, count, min_score, max_score = rationales[code]
        reason = test_case_reason(code, avg_score, count, min_score, max_score)
        lines.append(f"| {round_index} | {name} | {avg_score:.1f}/10 | {reason} |")
    lines.append("")
    return lines


def numeric_score(value: str | None) -> float | None:
    if not value or value == "—":
        return None
    try:
        return float(value.split("/", 1)[0])
    except (TypeError, ValueError):
        return None


def score_delta_summary(
    rows: list[tuple[str, str]],
    previous: dict[str, str],
    current: dict[str, str],
) -> tuple[list[str], list[str], list[str]]:
    improved: list[str] = []
    worsened: list[str] = []
    unchanged: list[str] = []
    for code, name in rows:
        prev_score = numeric_score(previous.get(code))
        curr_score = numeric_score(current.get(code))
        if prev_score is None or curr_score is None:
            continue
        delta = round(curr_score - prev_score, 1)
        line = f"{name}: {prev_score:.1f} -> {curr_score:.1f} ({delta:+.1f})"
        if delta >= 0.2:
            improved.append(line)
        elif delta <= -0.2:
            worsened.append(line)
        else:
            unchanged.append(line)
    return improved, worsened, unchanged


def benchmark_key(suite_scores_map: dict[str, str], tc_scores_map: dict[str, str]) -> tuple[float, float, float]:
    overall = numeric_score(suite_scores_map.get("overall_completeness")) or -1.0
    cleanliness = numeric_score(suite_scores_map.get("suite_cleanliness")) or -1.0
    trust = numeric_score(tc_scores_map.get("no_hallucinations")) or -1.0
    return overall, cleanliness, trust


def benchmark_index_for_current(
    runs: list[sqlite3.Row],
    run_suite: list[dict[str, str]],
    run_tc: list[dict[str, str]],
) -> int:
    if len(runs) <= 2:
        return len(runs) - 2
    previous_indexes = range(0, len(runs) - 1)
    return max(previous_indexes, key=lambda index: benchmark_key(run_suite[index], run_tc[index]))


def benchmark_block(
    runs: list[sqlite3.Row],
    run_suite: list[dict[str, str]],
    run_tc: list[dict[str, str]],
) -> list[str]:
    lines = ["## TOP benchmark", ""]
    if not runs:
        return lines + ["Данных по прогонам пока нет.", ""]

    current_run = runs[-1]["run_code"]
    if len(runs) == 1:
        return lines + [
            f"Текущий раунд `{current_run}` является первым доступным прогоном. TOP benchmark пока не выбран.",
            "",
        ]

    benchmark_index = benchmark_index_for_current(runs, run_suite, run_tc)
    benchmark_run = runs[benchmark_index]["run_code"]
    overall, cleanliness, trust = benchmark_key(run_suite[benchmark_index], run_tc[benchmark_index])
    mode = "последовательное сравнение с предыдущим раундом" if len(runs) <= 2 else "автоматический TOP benchmark"
    lines.extend(
        [
            "TOP benchmark - это лучшая предыдущая версия агента по текущей методике оценки. "
            "Она используется как точка сравнения, чтобы новый раунд оценивался не только относительно прошлого запуска, "
            "но и относительно лучшего результата, который уже был получен ранее.",
            "",
            "| Поле | Значение |",
            "|---|---|",
            f"| Режим сравнения | {mode} |",
            f"| TOP benchmark | `{benchmark_run}` |",
            f"| Почему выбран | Общая полнота набора: {overall:.1f}/10; чистота набора: {cleanliness:.1f}/10; достоверность отдельных ТК: {trust:.1f}/10 |",
            "",
            f"Текущий раунд `{current_run}` сравнивается с `{benchmark_run}`, которая сейчас является TOP benchmark.",
            "",
            "Начиная с третьего раунда benchmark выбирается среди всех предыдущих раундов: сначала по общей полноте набора, затем по чистоте набора, затем по достоверности отдельных ТК.",
            "",
        ]
    )
    return lines


def verdict_block(
    runs: list[sqlite3.Row],
    run_suite: list[dict[str, str]],
    run_tc: list[dict[str, str]],
) -> list[str]:
    lines = ["## Вердикт", ""]
    if not runs:
        return lines + ["Нет данных по прогонам.", ""]

    current_run = runs[-1]["run_code"]
    if len(runs) == 1:
        return lines + [
            f"Раунд `{current_run}` является первым доступным прогоном, поэтому сравнение с предыдущей версией агента пока невозможно.",
            "Отчет фиксирует базовое состояние качества и будет использоваться как точка сравнения для следующих раундов.",
            "",
        ]

    benchmark_index = benchmark_index_for_current(runs, run_suite, run_tc)
    benchmark_run = runs[benchmark_index]["run_code"]
    benchmark_label = "предыдущим раундом" if len(runs) <= 2 else "TOP benchmark"
    suite_improved, suite_worsened, suite_unchanged = score_delta_summary(
        SUITE_ROWS,
        run_suite[benchmark_index],
        run_suite[-1],
    )
    tc_improved, tc_worsened, tc_unchanged = score_delta_summary(
        TEST_CASE_ROWS,
        run_tc[benchmark_index],
        run_tc[-1],
    )
    improved = suite_improved + tc_improved
    worsened = suite_worsened + tc_worsened
    unchanged = suite_unchanged + tc_unchanged

    lines.extend(
        [
            f"Сравнение текущего раунда `{current_run}` с {benchmark_label} `{benchmark_run}`.",
            "",
            "### Что улучшилось",
            "",
        ]
    )
    if improved:
        lines.extend(f"- {item}" for item in improved)
    else:
        lines.append("- Значимых улучшений по измеряемым критериям не найдено.")

    lines.extend(["", "### Что ухудшилось", ""])
    if worsened:
        lines.extend(f"- {item}" for item in worsened)
    else:
        lines.append("- Значимых ухудшений по измеряемым критериям не найдено.")

    lines.extend(["", "### Без существенных изменений", ""])
    if unchanged:
        lines.extend(f"- {item}" for item in unchanged)
    else:
        lines.append("- Критериев без существенной динамики нет.")

    overall_previous = numeric_score(run_suite[benchmark_index].get("overall_completeness"))
    overall_current = numeric_score(run_suite[-1].get("overall_completeness"))
    cleanliness_previous = numeric_score(run_suite[benchmark_index].get("suite_cleanliness"))
    cleanliness_current = numeric_score(run_suite[-1].get("suite_cleanliness"))
    positive_previous = numeric_score(run_suite[benchmark_index].get("positive_coverage"))
    positive_current = numeric_score(run_suite[-1].get("positive_coverage"))
    required_previous = numeric_score(run_suite[benchmark_index].get("required_checks_coverage"))
    required_current = numeric_score(run_suite[-1].get("required_checks_coverage"))

    conclusion_parts: list[str] = []
    if overall_previous is not None and overall_current is not None:
        conclusion_parts.append(
            f"общая полнота набора изменилась с {overall_previous:.1f} до {overall_current:.1f}"
        )
    if cleanliness_previous is not None and cleanliness_current is not None:
        conclusion_parts.append(
            f"чистота набора изменилась с {cleanliness_previous:.1f} до {cleanliness_current:.1f}"
        )
    if positive_previous is not None and positive_current is not None:
        conclusion_parts.append(
            f"позитивное покрытие изменилось с {positive_previous:.1f} до {positive_current:.1f}"
        )
    if required_previous is not None and required_current is not None:
        conclusion_parts.append(
            f"покрытие обязательных проверок изменилось с {required_previous:.1f} до {required_current:.1f}"
        )

    lines.extend(["", "### Общий вывод", ""])
    if conclusion_parts:
        lines.append(
            "Изменение агента в текущем раунде привело к следующему результату: "
            + "; ".join(conclusion_parts)
            + "."
        )
    else:
        lines.append("Данных недостаточно, чтобы сформировать численный вывод по изменению агента.")

    if overall_previous is not None and overall_current is not None:
        if overall_current > overall_previous:
            improved_names = [item.split(":", 1)[0].lower() for item in improved]
            driver_names = [name for name in improved_names if name != "общая полнота набора"]
            if driver_names:
                driver_text = " Рост обеспечен улучшением критериев: " + ", ".join(driver_names) + "."
            else:
                driver_text = ""
            if worsened:
                worsened_names = ", ".join(item.split(":", 1)[0].lower() for item in worsened)
                caveat = f" При этом есть ограничения: просели критерии {worsened_names}."
            else:
                caveat = " Заметных просадок по измеряемым критериям нет."
            lines.append(
                f"В целом текущая версия выглядит лучше benchmark `{benchmark_run}`, потому что ключевой показатель выбора TOP benchmark "
                f"— общая полнота набора — вырос с {overall_previous:.1f} до {overall_current:.1f}."
                f"{driver_text}{caveat}"
            )
        elif overall_current < overall_previous:
            lines.append(
                f"В целом текущая версия выглядит хуже benchmark `{benchmark_run}`: снижение общей полноты требует анализа причин."
            )
        else:
            lines.append(
                f"В целом текущая версия находится примерно на уровне benchmark `{benchmark_run}`: значимого изменения общей полноты нет."
            )
    lines.append("")
    return lines


def build_report(connection: sqlite3.Connection, up_to_run_code: str | None = None) -> str:
    runs = eval_runs(connection, up_to_run_code)

    decomp_targets = target_map(connection, "requirement_decomposition_quality_criteria")
    suite_targets = target_map(connection, "test_suite_quality_criteria")
    tc_targets = target_map(connection, "test_case_quality_criteria")

    run_decomp = [decomposition_scores(connection, run["id"]) for run in runs]
    run_suite = [suite_scores(connection, run["id"]) for run in runs]
    run_tc = [test_case_average_scores(connection, run["id"]) for run in runs]

    lines = [
        "# Отчет по eval-прогонам",
        "",
        "Формат отчета: цели берутся из БД, колонки раундов строятся нарастающим итогом по таблице `eval_runs`.",
        "Декомпозиция требований в импортированных Excel-раундах не передавалась, поэтому ее критерии пока не измерялись.",
        "",
    ]
    lines.extend(run_summary_table(connection, runs))
    lines.extend(benchmark_block(runs, run_suite, run_tc))
    lines.extend(
        table_block(
            "1. Декомпозиция требований",
            DECOMPOSITION_ROWS,
            decomp_targets,
            run_decomp,
        )
    )
    lines.extend(decomposition_conclusion_block(runs))
    lines.extend(
        table_block(
            "2. Набор ТК",
            SUITE_ROWS,
            suite_targets,
            run_suite,
        )
    )
    lines.extend(suite_conclusion_block(connection, runs))
    lines.extend(
        table_block(
            "3. Отдельные ТК",
            TEST_CASE_ROWS,
            tc_targets,
            run_tc,
        )
    )
    lines.extend(test_case_conclusion_block(connection, runs))
    lines.extend(verdict_block(runs, run_suite, run_tc))
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Build an eval rounds report from SQLite.")
    parser.add_argument("--db", type=Path, default=DEFAULT_DB)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--up-to-run-code")
    args = parser.parse_args()

    with connect(args.db) as connection:
        report = build_report(connection, args.up_to_run_code)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(report, encoding="utf-8")
    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()
