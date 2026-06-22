from __future__ import annotations

import argparse
import sqlite3
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DB = ROOT / "data" / "cpt_eval.sqlite"


def scalar(connection: sqlite3.Connection, query: str) -> int:
    return int(connection.execute(query).fetchone()[0])


def validate(db_path: Path) -> list[str]:
    issues: list[str] = []
    with sqlite3.connect(db_path) as connection:
        connection.execute("PRAGMA foreign_keys = ON")
        connection.row_factory = sqlite3.Row

        criteria_count = scalar(connection, "SELECT COUNT(*) FROM requirement_quality_criteria WHERE is_active = 1")

        rows = connection.execute(
            """
            SELECT r.requirement_code, dc.case_code, COUNT(DISTINCT rqa.criterion_id) AS assessed_criteria
            FROM requirements r
            JOIN dataset_cases dc ON dc.id = r.dataset_case_id
            LEFT JOIN requirement_quality_assessments rqa ON rqa.requirement_id = r.id
            WHERE r.origin = 'expected'
            GROUP BY r.id
            HAVING assessed_criteria < ?
            ORDER BY dc.case_code, r.requirement_code
            """,
            (criteria_count,),
        ).fetchall()
        for row in rows:
            issues.append(
                f"{row['case_code']} / {row['requirement_code']}: has "
                f"{row['assessed_criteria']} of {criteria_count} quality assessments"
            )

        rows = connection.execute(
            """
            SELECT r.requirement_code, dc.case_code
            FROM requirements r
            JOIN dataset_cases dc ON dc.id = r.dataset_case_id
            LEFT JOIN requirement_source_links rsl ON rsl.requirement_id = r.id
            WHERE r.origin = 'expected'
            GROUP BY r.id
            HAVING COUNT(rsl.id) = 0
            ORDER BY dc.case_code, r.requirement_code
            """
        ).fetchall()
        for row in rows:
            issues.append(f"{row['case_code']} / {row['requirement_code']}: has no source fragment link")

        rows = connection.execute(
            """
            SELECT tc.test_case_code, dc.case_code
            FROM test_cases tc
            JOIN dataset_cases dc ON dc.id = tc.dataset_case_id
            LEFT JOIN requirement_test_case_links rtcl ON rtcl.test_case_id = tc.id
            WHERE tc.origin = 'expected'
            GROUP BY tc.id
            HAVING COUNT(rtcl.id) = 0
            ORDER BY dc.case_code, tc.test_case_code
            """
        ).fetchall()
        for row in rows:
            issues.append(f"{row['case_code']} / {row['test_case_code']}: has no requirement link")

        rows = connection.execute(
            """
            SELECT tc.test_case_code, dc.case_code
            FROM test_cases tc
            JOIN dataset_cases dc ON dc.id = tc.dataset_case_id
            LEFT JOIN test_case_steps tcs ON tcs.test_case_id = tc.id
            WHERE tc.origin = 'expected'
            GROUP BY tc.id
            HAVING COUNT(tcs.id) = 0
            ORDER BY dc.case_code, tc.test_case_code
            """
        ).fetchall()
        for row in rows:
            issues.append(f"{row['case_code']} / {row['test_case_code']}: has no steps")

        rows = connection.execute(
            """
            SELECT tcs.id, tc.test_case_code, dc.case_code
            FROM test_case_steps tcs
            JOIN test_cases tc ON tc.id = tcs.test_case_id
            JOIN dataset_cases dc ON dc.id = tc.dataset_case_id
            LEFT JOIN test_case_step_requirement_links link ON link.test_case_step_id = tcs.id
            LEFT JOIN unsupported_details detail ON detail.test_case_step_id = tcs.id
            WHERE tc.origin = 'expected'
            GROUP BY tcs.id
            HAVING COUNT(link.id) = 0 AND COUNT(detail.id) = 0
            ORDER BY dc.case_code, tc.test_case_code, tcs.step_number
            """
        ).fetchall()
        for row in rows:
            issues.append(
                f"{row['case_code']} / {row['test_case_code']} / step {row['id']}: "
                "has no requirement link and no unsupported detail marker"
            )

    return issues


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate the CPT eval dataset database.")
    parser.add_argument("--db", type=Path, default=DEFAULT_DB, help="Path to SQLite database file.")
    args = parser.parse_args()

    issues = validate(args.db)
    if issues:
        print("Validation failed:")
        for issue in issues:
            print(f"- {issue}")
        raise SystemExit(1)

    print("Validation passed.")


if __name__ == "__main__":
    main()
