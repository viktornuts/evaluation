from __future__ import annotations

import argparse
import json
import sqlite3
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DB = ROOT / "data" / "cpt_eval.sqlite"


def connect(db_path: Path) -> sqlite3.Connection:
    connection = sqlite3.connect(db_path)
    connection.execute("PRAGMA foreign_keys = ON")
    connection.row_factory = sqlite3.Row
    return connection


def criterion_row(connection: sqlite3.Connection, code: str) -> sqlite3.Row:
    row = connection.execute("SELECT id FROM quality_criteria WHERE code = ?", (code,)).fetchone()
    if row is None:
        raise ValueError(f"Unknown quality criterion: {code}")
    return row


def original_assessment(
    connection: sqlite3.Connection,
    requirement_id: str,
    criterion_id: str,
    original_assessment_id: str | None,
) -> sqlite3.Row | None:
    if original_assessment_id:
        row = connection.execute(
            """
            SELECT id, score
            FROM requirement_quality_assessments
            WHERE id = ? AND requirement_id = ? AND criterion_id = ?
            """,
            (original_assessment_id, requirement_id, criterion_id),
        ).fetchone()
        if row is not None:
            return row

    return connection.execute(
        """
        SELECT id, score
        FROM requirement_quality_assessments
        WHERE requirement_id = ? AND criterion_id = ?
        ORDER BY created_at DESC
        LIMIT 1
        """,
        (requirement_id, criterion_id),
    ).fetchone()


def import_review(db_path: Path, input_path: Path) -> None:
    payload = json.loads(input_path.read_text(encoding="utf-8"))
    review = payload["external_review"]

    with connect(db_path) as connection:
        connection.execute(
            """
            INSERT INTO external_reviews (
                id, dataset_id, dataset_case_id, reviewer_name, reviewer_type,
                model_name, prompt_version, review_status, summary, metadata_json
            )
            VALUES (
                :id, :dataset_id, :dataset_case_id, :reviewer_name, :reviewer_type,
                :model_name, :prompt_version, :review_status, :summary, :metadata_json
            )
            ON CONFLICT(id) DO UPDATE SET
                dataset_id = excluded.dataset_id,
                dataset_case_id = excluded.dataset_case_id,
                reviewer_name = excluded.reviewer_name,
                reviewer_type = excluded.reviewer_type,
                model_name = excluded.model_name,
                prompt_version = excluded.prompt_version,
                review_status = excluded.review_status,
                summary = excluded.summary,
                metadata_json = excluded.metadata_json
            """,
            {
                "id": review["id"],
                "dataset_id": review["dataset_id"],
                "dataset_case_id": review.get("dataset_case_id"),
                "reviewer_name": review["reviewer_name"],
                "reviewer_type": review.get("reviewer_type", "llm"),
                "model_name": review.get("model_name"),
                "prompt_version": review.get("prompt_version"),
                "review_status": review.get("review_status", "completed"),
                "summary": review.get("summary"),
                "metadata_json": json.dumps(review.get("metadata", {}), ensure_ascii=False),
            },
        )

        for item in payload.get("requirement_assessment_reviews", []):
            criterion = criterion_row(connection, item["criterion"])
            original = original_assessment(
                connection,
                item["requirement_id"],
                criterion["id"],
                item.get("original_assessment_id"),
            )
            connection.execute(
                """
                INSERT INTO external_requirement_assessment_reviews (
                    id, external_review_id, requirement_id, criterion_id, original_assessment_id,
                    original_score, reviewer_score, reviewer_label, agreement_status,
                    reviewer_comment, severity
                )
                VALUES (
                    :id, :external_review_id, :requirement_id, :criterion_id, :original_assessment_id,
                    :original_score, :reviewer_score, :reviewer_label, :agreement_status,
                    :reviewer_comment, :severity
                )
                ON CONFLICT(external_review_id, requirement_id, criterion_id) DO UPDATE SET
                    original_assessment_id = excluded.original_assessment_id,
                    original_score = excluded.original_score,
                    reviewer_score = excluded.reviewer_score,
                    reviewer_label = excluded.reviewer_label,
                    agreement_status = excluded.agreement_status,
                    reviewer_comment = excluded.reviewer_comment,
                    severity = excluded.severity
                """,
                {
                    "id": item["id"],
                    "external_review_id": review["id"],
                    "requirement_id": item["requirement_id"],
                    "criterion_id": criterion["id"],
                    "original_assessment_id": original["id"] if original else item.get("original_assessment_id"),
                    "original_score": original["score"] if original else item.get("original_score"),
                    "reviewer_score": item.get("reviewer_score"),
                    "reviewer_label": item.get("reviewer_label"),
                    "agreement_status": item["agreement_status"],
                    "reviewer_comment": item.get("reviewer_comment"),
                    "severity": item.get("severity", "info"),
                },
            )

        for item in payload.get("test_case_reviews", []):
            connection.execute(
                """
                INSERT OR REPLACE INTO external_test_case_reviews (
                    id, external_review_id, test_case_id, requirement_id,
                    agreement_status, reviewer_comment, severity
                )
                VALUES (
                    :id, :external_review_id, :test_case_id, :requirement_id,
                    :agreement_status, :reviewer_comment, :severity
                )
                """,
                {
                    "id": item["id"],
                    "external_review_id": review["id"],
                    "test_case_id": item["test_case_id"],
                    "requirement_id": item.get("requirement_id"),
                    "agreement_status": item["agreement_status"],
                    "reviewer_comment": item.get("reviewer_comment"),
                    "severity": item.get("severity", "info"),
                },
            )

        connection.commit()


def main() -> None:
    parser = argparse.ArgumentParser(description="Import an external AI review without overwriting project assessments.")
    parser.add_argument("input", type=Path, help="Path to external review JSON.")
    parser.add_argument("--db", type=Path, default=DEFAULT_DB, help="Path to SQLite database file.")
    args = parser.parse_args()

    import_review(args.db, args.input)
    print(f"Imported external review from {args.input}")


if __name__ == "__main__":
    main()
