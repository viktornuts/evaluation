from __future__ import annotations

import argparse
import sqlite3
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DB = ROOT / "data" / "cpt_eval.sqlite"


def report(db_path: Path) -> None:
    with sqlite3.connect(db_path) as connection:
        connection.row_factory = sqlite3.Row

        reviews = connection.execute(
            """
            SELECT er.id, er.reviewer_name, er.model_name, er.review_status, er.summary,
                   d.name AS dataset, dc.case_code
            FROM external_reviews er
            JOIN datasets d ON d.id = er.dataset_id
            LEFT JOIN dataset_cases dc ON dc.id = er.dataset_case_id
            ORDER BY er.created_at DESC
            """
        ).fetchall()

        if not reviews:
            print("No external reviews.")
            return

        print("External reviews")
        for review in reviews:
            print(
                f"- {review['id']} | reviewer: {review['reviewer_name']} | "
                f"model: {review['model_name']} | dataset: {review['dataset']} | "
                f"case: {review['case_code']} | status: {review['review_status']}"
            )
            if review["summary"]:
                print(f"  summary: {review['summary']}")

        disagreements = connection.execute(
            """
            SELECT er.reviewer_name, dc.case_code, r.requirement_code, qc.code AS criterion,
                   err.original_score, err.reviewer_score, err.reviewer_label,
                   err.agreement_status, err.severity, err.reviewer_comment
            FROM external_requirement_assessment_reviews err
            JOIN external_reviews er ON er.id = err.external_review_id
            LEFT JOIN dataset_cases dc ON dc.id = er.dataset_case_id
            JOIN requirements r ON r.id = err.requirement_id
            JOIN requirement_quality_criteria qc ON qc.id = err.criterion_id
            WHERE err.agreement_status <> 'agree'
            ORDER BY dc.case_code, r.requirement_code, qc.code
            """
        ).fetchall()

        print("\nRequirement assessment disagreements")
        if not disagreements:
            print("  no disagreements")
        for item in disagreements:
            print(
                f"- {item['case_code']} / {item['requirement_code']} / {item['criterion']}: "
                f"project={item['original_score']} external={item['reviewer_score']} "
                f"label={item['reviewer_label']} severity={item['severity']}"
            )
            if item["reviewer_comment"]:
                print(f"  comment: {item['reviewer_comment']}")

        tc_reviews = connection.execute(
            """
            SELECT er.reviewer_name, tc.test_case_code, r.requirement_code,
                   etcr.agreement_status, etcr.severity, etcr.reviewer_comment
            FROM external_test_case_reviews etcr
            JOIN external_reviews er ON er.id = etcr.external_review_id
            JOIN test_cases tc ON tc.id = etcr.test_case_id
            LEFT JOIN requirements r ON r.id = etcr.requirement_id
            WHERE etcr.agreement_status <> 'agree'
            ORDER BY tc.test_case_code, r.requirement_code
            """
        ).fetchall()

        print("\nTest case review disagreements")
        if not tc_reviews:
            print("  no disagreements")
        for item in tc_reviews:
            print(
                f"- {item['test_case_code']} / {item['requirement_code']}: "
                f"{item['agreement_status']} severity={item['severity']}"
            )
            if item["reviewer_comment"]:
                print(f"  comment: {item['reviewer_comment']}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Report external AI review disagreements.")
    parser.add_argument("--db", type=Path, default=DEFAULT_DB, help="Path to SQLite database file.")
    args = parser.parse_args()
    report(args.db)


if __name__ == "__main__":
    main()
