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


def eval_runs(connection: sqlite3.Connection) -> list[sqlite3.Row]:
    rows = connection.execute(
        """
        SELECT *
        FROM eval_runs
        WHERE dataset_id = ?
        ORDER BY started_at, run_code
        """,
        (DATASET_ID,),
    ).fetchall()
    return sorted(rows, key=natural_run_key)


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


def suite_rationale_block(connection: sqlite3.Connection, runs: list[sqlite3.Row]) -> list[str]:
    lines = [
        "## Пояснения по оценкам набора",
        "",
        "| Раунд | Критерий | Score | Почему такая оценка |",
        "|---:|---|---:|---|",
    ]
    for index, run in enumerate(runs, start=1):
        rationales = suite_rationales(connection, run["id"])
        for code, name in SUITE_ROWS:
            if code not in rationales:
                continue
            score, rationale = rationales[code]
            lines.append(f"| {index} | {name} | {score:.1f}/10 | {rationale} |")
    lines.append("")
    return lines


def build_report(connection: sqlite3.Connection) -> str:
    runs = eval_runs(connection)

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
    lines.extend(
        table_block(
            "1. Декомпозиция требований",
            DECOMPOSITION_ROWS,
            decomp_targets,
            run_decomp,
        )
    )
    lines.extend(
        table_block(
            "2. Набор ТК",
            SUITE_ROWS,
            suite_targets,
            run_suite,
        )
    )
    lines.extend(
        table_block(
            "3. Отдельные ТК",
            TEST_CASE_ROWS,
            tc_targets,
            run_tc,
        )
    )
    lines.extend(suite_rationale_block(connection, runs))
    lines.extend(
        [
            "## Вердикт",
            "",
            "Механизм оценки работает на нескольких раундах: каждый прогон хранится отдельно, сгенерированные ТК связаны с требованиями, оценки сохранены по критериям и собираются в нарастающий отчет. Оценки являются демо-разметкой Codex и требуют ручного ревью перед управленческим решением.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Build an eval rounds report from SQLite.")
    parser.add_argument("--db", type=Path, default=DEFAULT_DB)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    with connect(args.db) as connection:
        report = build_report(connection)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(report, encoding="utf-8")
    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()
