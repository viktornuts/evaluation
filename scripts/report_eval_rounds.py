from __future__ import annotations

import argparse
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


def run_by_code(connection: sqlite3.Connection, run_code: str) -> sqlite3.Row | None:
    return connection.execute(
        """
        SELECT *
        FROM eval_runs
        WHERE dataset_id = ? AND run_code = ?
        ORDER BY started_at DESC
        LIMIT 1
        """,
        (DATASET_ID, run_code),
    ).fetchone()


def target_map(connection: sqlite3.Connection, table: str) -> dict[str, str]:
    rows = connection.execute(f"SELECT code, target_display FROM {table}").fetchall()
    return {row["code"]: row["target_display"] or "10" for row in rows}


def suite_scores(connection: sqlite3.Connection, eval_run_id: str) -> dict[str, str]:
    rows = connection.execute(
        """
        SELECT c.code, a.score, a.label
        FROM test_suite_quality_assessments a
        JOIN test_suite_quality_criteria c ON c.id = a.criterion_id
        WHERE a.eval_run_id = ?
        """,
        (eval_run_id,),
    ).fetchall()
    return {row["code"]: f"{row['score']:.1f}/10" for row in rows}


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


def table_block(
    title: str,
    rows: list[tuple[str, str]],
    targets: dict[str, str],
    baseline: dict[str, str],
    round_1: dict[str, str],
    round_2: dict[str, str],
) -> list[str]:
    lines = [
        f"## {title}",
        "",
        "| Критерий | Цель | Baseline | Раунд 1 | Раунд 2 |",
        "|---|---:|---:|---:|---:|",
    ]
    for code, name in rows:
        lines.append(
            "| "
            f"{name} | "
            f"{targets.get(code, '—')} | "
            f"{baseline.get(code, '—')} | "
            f"{round_1.get(code, '—')} | "
            f"{round_2.get(code, '—')} |"
        )
    lines.append("")
    return lines


def compact_name_version(name: str | None, version: str | None) -> str:
    values = [value for value in (name, version) if value]
    if not values:
        return "—"
    if len(values) == 2 and values[0] == values[1]:
        return values[0]
    return " ".join(values)


def run_summary_table(run: sqlite3.Row | None) -> list[str]:
    if run is None:
        return [
            "## Параметры прогона",
            "",
            "| Прогон | Что изменили | Агент | Модель | Temperature | Top P | Режим |",
            "|---|---|---|---|---:|---:|---|",
            "| Раунд 1 | — | — | — | — | — | — |",
            "",
        ]

    return [
        "## Параметры прогона",
        "",
        "| Прогон | Что изменили | Агент | Модель | Temperature | Top P | Режим |",
        "|---|---|---|---|---:|---:|---|",
        "| "
        f"Раунд 1 (`{run['run_code']}`) | "
        f"{run['change_summary'] or '—'} | "
        f"{compact_name_version(run['agent_name'], run['agent_version'])} | "
        f"{compact_name_version(run['model_name'], run['model_version'])} | "
        f"{run['temperature']} | "
        f"{run['top_p']} | "
        f"{run['run_mode']} |",
        "",
    ]


def build_report(connection: sqlite3.Connection, round_1_code: str) -> str:
    round_1 = run_by_code(connection, round_1_code)
    round_1_id = str(round_1["id"]) if round_1 else ""

    decomp_targets = target_map(connection, "requirement_decomposition_quality_criteria")
    suite_targets = target_map(connection, "test_suite_quality_criteria")
    tc_targets = target_map(connection, "test_case_quality_criteria")

    baseline_empty: dict[str, str] = {}
    round_2_empty: dict[str, str] = {}
    round_1_decomp = decomposition_scores(connection, round_1_id) if round_1_id else {}
    round_1_suite = suite_scores(connection, round_1_id) if round_1_id else {}
    round_1_tc = test_case_average_scores(connection, round_1_id) if round_1_id else {}

    lines = [
        "# Отчет по eval-прогонам",
        "",
        "Формат отчета: цели берутся из БД, `Раунд 1` сейчас соответствует демо-прогону `v1`.",
        "Декомпозиция в `v1` не передавалась, поэтому ее критерии пока не измерялись.",
        "",
    ]
    lines.extend(run_summary_table(round_1))
    lines.extend(
        table_block(
            "1. Декомпозиция требований",
            DECOMPOSITION_ROWS,
            decomp_targets,
            baseline_empty,
            round_1_decomp,
            round_2_empty,
        )
    )
    lines.extend(
        table_block(
            "2. Набор ТК",
            SUITE_ROWS,
            suite_targets,
            baseline_empty,
            round_1_suite,
            round_2_empty,
        )
    )
    lines.extend(
        table_block(
            "3. Отдельные ТК",
            TEST_CASE_ROWS,
            tc_targets,
            baseline_empty,
            round_1_tc,
            round_2_empty,
        )
    )
    lines.extend(
        [
            "## Вердикт",
            "",
            "Демо-прогон показывает, что механизм оценки работает: ТК импортированы, связаны с требованиями, оценки по критериям сохранены в БД и собираются в отчет. Для демонстрации достаточно; для приемки нужны ручная проверка спорных оценок, уточнение трассировки и последующий прогон с полной информацией об агенте, промпте и декомпозиции.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Build an eval rounds report from SQLite.")
    parser.add_argument("--db", type=Path, default=DEFAULT_DB)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--round-1", default="v1")
    args = parser.parse_args()

    with connect(args.db) as connection:
        report = build_report(connection, args.round_1)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(report, encoding="utf-8")
    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()
