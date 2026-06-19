from __future__ import annotations

import argparse
import sqlite3
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DB = ROOT / "data" / "cpt_eval.sqlite"


def print_rows(title: str, rows: list[sqlite3.Row]) -> None:
    print(f"\n{title}")
    if not rows:
        print("  no data")
        return
    for row in rows:
        print("  " + " | ".join(f"{key}: {row[key]}" for key in row.keys()))


def report(db_path: Path) -> None:
    with sqlite3.connect(db_path) as connection:
        connection.row_factory = sqlite3.Row

        overview = connection.execute(
            """
            SELECT
                d.name AS dataset,
                d.version,
                COUNT(DISTINCT dc.id) AS cases,
                COUNT(DISTINCT r.id) AS requirements,
                COUNT(DISTINCT tc.id) AS test_cases,
                COUNT(DISTINCT tcs.id) AS test_case_steps
            FROM datasets d
            LEFT JOIN dataset_cases dc ON dc.dataset_id = d.id
            LEFT JOIN requirements r ON r.dataset_case_id = dc.id
            LEFT JOIN test_cases tc ON tc.dataset_case_id = dc.id
            LEFT JOIN test_case_steps tcs ON tcs.test_case_id = tc.id
            GROUP BY d.id
            ORDER BY d.name, d.version
            """
        ).fetchall()
        print_rows("Dataset overview", overview)

        statuses = connection.execute(
            """
            SELECT expected_status, COUNT(*) AS count
            FROM requirements
            WHERE origin = 'expected'
            GROUP BY expected_status
            ORDER BY count DESC, expected_status
            """
        ).fetchall()
        print_rows("Requirement statuses", statuses)

        risk = connection.execute(
            """
            SELECT COALESCE(risk_level, 'not_set') AS risk_level, COUNT(*) AS count
            FROM requirements
            WHERE origin = 'expected'
            GROUP BY COALESCE(risk_level, 'not_set')
            ORDER BY count DESC, risk_level
            """
        ).fetchall()
        print_rows("Requirement risk levels", risk)

        quality = connection.execute(
            """
            SELECT qc.code AS criterion, rqa.label, COUNT(*) AS count, ROUND(AVG(rqa.score), 2) AS avg_score
            FROM requirement_quality_assessments rqa
            JOIN quality_criteria qc ON qc.id = rqa.criterion_id
            JOIN requirements r ON r.id = rqa.requirement_id
            WHERE r.origin = 'expected'
            GROUP BY qc.code, rqa.label
            ORDER BY qc.code, count DESC, rqa.label
            """
        ).fetchall()
        print_rows("Requirement quality profile", quality)

        coverage = connection.execute(
            """
            SELECT rtcl.coverage_status, rtcl.coverage_type, COUNT(*) AS count
            FROM requirement_test_case_links rtcl
            GROUP BY rtcl.coverage_status, rtcl.coverage_type
            ORDER BY count DESC
            """
        ).fetchall()
        print_rows("Requirement to test case links", coverage)

        unsupported = connection.execute(
            """
            SELECT severity, detail_type, COUNT(*) AS count
            FROM unsupported_details
            GROUP BY severity, detail_type
            ORDER BY count DESC
            """
        ).fetchall()
        print_rows("Unsupported details", unsupported)

        test_case_evaluation = connection.execute(
            """
            SELECT
                match_status,
                structure_status,
                classification_status,
                hallucination_status,
                COUNT(*) AS count,
                ROUND(AVG(score), 2) AS avg_score
            FROM test_case_evaluation_results
            GROUP BY match_status, structure_status, classification_status, hallucination_status
            ORDER BY count DESC
            """
        ).fetchall()
        print_rows("Test case evaluation results", test_case_evaluation)


def main() -> None:
    parser = argparse.ArgumentParser(description="Print a profile report for the CPT eval dataset.")
    parser.add_argument("--db", type=Path, default=DEFAULT_DB, help="Path to SQLite database file.")
    args = parser.parse_args()

    report(args.db)


if __name__ == "__main__":
    main()
