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


def criterion_id(connection: sqlite3.Connection, code: str) -> str:
    row = connection.execute("SELECT id FROM requirement_quality_criteria WHERE code = ?", (code,)).fetchone()
    if row is None:
        raise ValueError(f"Unknown quality criterion: {code}")
    return str(row["id"])


def upsert_dataset(connection: sqlite3.Connection, dataset: dict[str, Any]) -> None:
    connection.execute(
        """
        INSERT INTO datasets (id, name, version, description, status)
        VALUES (:id, :name, :version, :description, :status)
        ON CONFLICT(id) DO UPDATE SET
            name = excluded.name,
            version = excluded.version,
            description = excluded.description,
            status = excluded.status
        """,
        {
            "id": dataset["id"],
            "name": dataset["name"],
            "version": dataset["version"],
            "description": dataset.get("description"),
            "status": dataset.get("status", "draft"),
        },
    )


def upsert_case(connection: sqlite3.Connection, dataset_id: str, case: dict[str, Any]) -> None:
    connection.execute(
        """
        INSERT INTO dataset_cases (
            id, dataset_id, case_code, title, description, case_type,
            input_profile_code, input_profile_name
        )
        VALUES (
            :id, :dataset_id, :case_code, :title, :description, :case_type,
            :input_profile_code, :input_profile_name
        )
        ON CONFLICT(id) DO UPDATE SET
            dataset_id = excluded.dataset_id,
            case_code = excluded.case_code,
            title = excluded.title,
            description = excluded.description,
            case_type = excluded.case_type,
            input_profile_code = excluded.input_profile_code,
            input_profile_name = excluded.input_profile_name
        """,
        {
            "id": case["id"],
            "dataset_id": dataset_id,
            "case_code": case["case_code"],
            "title": case["title"],
            "description": case.get("description"),
            "case_type": case.get("case_type", "manual"),
            "input_profile_code": case.get("input_profile_code"),
            "input_profile_name": case.get("input_profile_name"),
        },
    )


def upsert_sources(connection: sqlite3.Connection, case_id: str, sources: list[dict[str, Any]]) -> None:
    for source in sources:
        connection.execute(
            """
            INSERT INTO source_materials (
                id, dataset_case_id, source_type, source_name, source_version, raw_text, metadata_json
            )
            VALUES (:id, :dataset_case_id, :source_type, :source_name, :source_version, :raw_text, :metadata_json)
            ON CONFLICT(id) DO UPDATE SET
                dataset_case_id = excluded.dataset_case_id,
                source_type = excluded.source_type,
                source_name = excluded.source_name,
                source_version = excluded.source_version,
                raw_text = excluded.raw_text,
                metadata_json = excluded.metadata_json
            """,
            {
                "id": source["id"],
                "dataset_case_id": case_id,
                "source_type": source["source_type"],
                "source_name": source.get("source_name"),
                "source_version": source.get("source_version"),
                "raw_text": source.get("raw_text"),
                "metadata_json": json.dumps(source.get("metadata", {}), ensure_ascii=False),
            },
        )
        for fragment in source.get("fragments", []):
            connection.execute(
                """
                INSERT INTO source_fragments (id, source_material_id, fragment_ref, fragment_text)
                VALUES (:id, :source_material_id, :fragment_ref, :fragment_text)
                ON CONFLICT(id) DO UPDATE SET
                    source_material_id = excluded.source_material_id,
                    fragment_ref = excluded.fragment_ref,
                    fragment_text = excluded.fragment_text
                """,
                {
                    "id": fragment["id"],
                    "source_material_id": source["id"],
                    "fragment_ref": fragment["fragment_ref"],
                    "fragment_text": fragment["fragment_text"],
                },
            )


def upsert_input_requirements(
    connection: sqlite3.Connection, case_id: str, input_requirements: list[dict[str, Any]]
) -> None:
    for requirement in input_requirements:
        connection.execute(
            """
            INSERT INTO input_requirements (
                id, dataset_case_id, input_requirement_code, title, requirement_text,
                source_fragment_id, requirement_order
            )
            VALUES (
                :id, :dataset_case_id, :input_requirement_code, :title, :requirement_text,
                :source_fragment_id, :requirement_order
            )
            ON CONFLICT(id) DO UPDATE SET
                dataset_case_id = excluded.dataset_case_id,
                input_requirement_code = excluded.input_requirement_code,
                title = excluded.title,
                requirement_text = excluded.requirement_text,
                source_fragment_id = excluded.source_fragment_id,
                requirement_order = excluded.requirement_order
            """,
            {
                "id": requirement["id"],
                "dataset_case_id": case_id,
                "input_requirement_code": requirement["input_requirement_code"],
                "title": requirement.get("title"),
                "requirement_text": requirement["requirement_text"],
                "source_fragment_id": requirement.get("source_fragment_id"),
                "requirement_order": requirement.get("requirement_order"),
            },
        )


def upsert_requirements(connection: sqlite3.Connection, case_id: str, requirements: list[dict[str, Any]]) -> None:
    for requirement in requirements:
        connection.execute(
            """
            INSERT INTO requirements (
                id, dataset_case_id, requirement_code, requirement_text, origin, expected_status,
                quality_profile_status, risk_level, is_ready_for_generation, comment
            )
            VALUES (
                :id, :dataset_case_id, :requirement_code, :requirement_text, :origin, :expected_status,
                :quality_profile_status, :risk_level, :is_ready_for_generation, :comment
            )
            ON CONFLICT(id) DO UPDATE SET
                dataset_case_id = excluded.dataset_case_id,
                requirement_code = excluded.requirement_code,
                requirement_text = excluded.requirement_text,
                origin = excluded.origin,
                expected_status = excluded.expected_status,
                quality_profile_status = excluded.quality_profile_status,
                risk_level = excluded.risk_level,
                is_ready_for_generation = excluded.is_ready_for_generation,
                comment = excluded.comment
            """,
            {
                "id": requirement["id"],
                "dataset_case_id": case_id,
                "requirement_code": requirement["requirement_code"],
                "requirement_text": requirement["requirement_text"],
                "origin": requirement.get("origin", "expected"),
                "expected_status": requirement.get("expected_status", "ready_for_generation"),
                "quality_profile_status": requirement.get("quality_profile_status"),
                "risk_level": requirement.get("risk_level"),
                "is_ready_for_generation": 1 if requirement.get("is_ready_for_generation", True) else 0,
                "comment": requirement.get("comment"),
            },
        )
        for link in requirement.get("source_links", []):
            connection.execute(
                """
                INSERT OR REPLACE INTO requirement_source_links (
                    id, requirement_id, source_fragment_id, link_type, rationale
                )
                VALUES (:id, :requirement_id, :source_fragment_id, :link_type, :rationale)
                """,
                {
                    "id": link["id"],
                    "requirement_id": requirement["id"],
                    "source_fragment_id": link["source_fragment_id"],
                    "link_type": link.get("link_type", "derived_from"),
                    "rationale": link.get("rationale"),
                },
            )
        for assessment in requirement.get("quality_assessments", []):
            connection.execute(
                """
                INSERT OR REPLACE INTO requirement_quality_assessments (
                    id, requirement_id, criterion_id, score, label, rationale,
                    assessed_by, assessment_method, confidence
                )
                VALUES (
                    :id, :requirement_id, :criterion_id, :score, :label, :rationale,
                    :assessed_by, :assessment_method, :confidence
                )
                """,
                {
                    "id": assessment["id"],
                    "requirement_id": requirement["id"],
                    "criterion_id": criterion_id(connection, assessment["criterion"]),
                    "score": assessment["score"],
                    "label": assessment["label"],
                    "rationale": assessment.get("rationale"),
                    "assessed_by": assessment.get("assessed_by", "unknown"),
                    "assessment_method": assessment.get("assessment_method", "human"),
                    "confidence": assessment.get("confidence"),
                },
            )


def upsert_input_requirement_decomposition_links(
    connection: sqlite3.Connection, links: list[dict[str, Any]]
) -> None:
    for link in links:
        connection.execute(
            """
            INSERT OR REPLACE INTO input_requirement_decomposition_links (
                id, input_requirement_id, requirement_id, link_type, rationale
            )
            VALUES (:id, :input_requirement_id, :requirement_id, :link_type, :rationale)
            """,
            {
                "id": link["id"],
                "input_requirement_id": link["input_requirement_id"],
                "requirement_id": link["requirement_id"],
                "link_type": link.get("link_type", "expected_atomic_requirement"),
                "rationale": link.get("rationale"),
            },
        )


def upsert_test_cases(connection: sqlite3.Connection, case_id: str, test_cases: list[dict[str, Any]]) -> None:
    for test_case in test_cases:
        connection.execute(
            """
            INSERT INTO test_cases (
                id, dataset_case_id, test_case_code, title, test_case_type, direction,
                origin, preconditions, postconditions
            )
            VALUES (
                :id, :dataset_case_id, :test_case_code, :title, :test_case_type, :direction,
                :origin, :preconditions, :postconditions
            )
            ON CONFLICT(id) DO UPDATE SET
                dataset_case_id = excluded.dataset_case_id,
                test_case_code = excluded.test_case_code,
                title = excluded.title,
                test_case_type = excluded.test_case_type,
                direction = excluded.direction,
                origin = excluded.origin,
                preconditions = excluded.preconditions,
                postconditions = excluded.postconditions
            """,
            {
                "id": test_case["id"],
                "dataset_case_id": case_id,
                "test_case_code": test_case["test_case_code"],
                "title": test_case["title"],
                "test_case_type": test_case.get("test_case_type"),
                "direction": test_case.get("direction"),
                "origin": test_case.get("origin", "expected"),
                "preconditions": test_case.get("preconditions"),
                "postconditions": test_case.get("postconditions"),
            },
        )
        for step in test_case.get("steps", []):
            connection.execute(
                """
                INSERT INTO test_case_steps (id, test_case_id, step_number, action, expected_result)
                VALUES (:id, :test_case_id, :step_number, :action, :expected_result)
                ON CONFLICT(id) DO UPDATE SET
                    test_case_id = excluded.test_case_id,
                    step_number = excluded.step_number,
                    action = excluded.action,
                    expected_result = excluded.expected_result
                """,
                {
                    "id": step["id"],
                    "test_case_id": test_case["id"],
                    "step_number": step["step_number"],
                    "action": step["action"],
                    "expected_result": step["expected_result"],
                },
            )
            for requirement_id in step.get("linked_requirement_ids", []):
                connection.execute(
                    """
                    INSERT OR REPLACE INTO test_case_step_requirement_links (
                        id, test_case_step_id, requirement_id, source_fragment_id, rationale, linked_by, review_status
                    )
                    VALUES (:id, :test_case_step_id, :requirement_id, :source_fragment_id, :rationale, :linked_by, :review_status)
                    """,
                    {
                        "id": f"step_link_{step['id']}_{requirement_id}",
                        "test_case_step_id": step["id"],
                        "requirement_id": requirement_id,
                        "source_fragment_id": step.get("source_fragment_id"),
                        "rationale": step.get("link_rationale"),
                        "linked_by": step.get("linked_by", "unknown"),
                        "review_status": step.get("review_status", "draft"),
                    },
                )


def upsert_requirement_test_case_links(
    connection: sqlite3.Connection, links: list[dict[str, Any]]
) -> None:
    for link in links:
        connection.execute(
            """
            INSERT OR REPLACE INTO requirement_test_case_links (
                id, requirement_id, test_case_id, coverage_status, coverage_type,
                is_primary, rationale, linked_by, review_status
            )
            VALUES (
                :id, :requirement_id, :test_case_id, :coverage_status, :coverage_type,
                :is_primary, :rationale, :linked_by, :review_status
            )
            """,
            {
                "id": link["id"],
                "requirement_id": link["requirement_id"],
                "test_case_id": link["test_case_id"],
                "coverage_status": link.get("coverage_status", "covered"),
                "coverage_type": link.get("coverage_type"),
                "is_primary": 1 if link.get("is_primary", False) else 0,
                "rationale": link.get("rationale"),
                "linked_by": link.get("linked_by", "unknown"),
                "review_status": link.get("review_status", "draft"),
            },
        )


def upsert_unsupported_details(connection: sqlite3.Connection, details: list[dict[str, Any]]) -> None:
    for detail in details:
        connection.execute(
            """
            INSERT OR REPLACE INTO unsupported_details (
                id, test_case_id, test_case_step_id, detail_text, detail_type,
                reason, severity, review_status
            )
            VALUES (
                :id, :test_case_id, :test_case_step_id, :detail_text, :detail_type,
                :reason, :severity, :review_status
            )
            """,
            {
                "id": detail["id"],
                "test_case_id": detail["test_case_id"],
                "test_case_step_id": detail.get("test_case_step_id"),
                "detail_text": detail["detail_text"],
                "detail_type": detail.get("detail_type"),
                "reason": detail.get("reason"),
                "severity": detail.get("severity", "minor"),
                "review_status": detail.get("review_status", "draft"),
            },
        )


def import_dataset(db_path: Path, input_path: Path) -> None:
    payload = json.loads(input_path.read_text(encoding="utf-8"))
    with connect(db_path) as connection:
        upsert_dataset(connection, payload["dataset"])
        for case in payload.get("cases", []):
            upsert_case(connection, payload["dataset"]["id"], case)
            upsert_sources(connection, case["id"], case.get("source_materials", []))
            upsert_input_requirements(connection, case["id"], case.get("input_requirements", []))
            upsert_requirements(connection, case["id"], case.get("requirements", []))
            upsert_input_requirement_decomposition_links(
                connection, case.get("input_requirement_decomposition_links", [])
            )
            upsert_test_cases(connection, case["id"], case.get("test_cases", []))
            upsert_requirement_test_case_links(connection, case.get("requirement_test_case_links", []))
            upsert_unsupported_details(connection, case.get("unsupported_details", []))
        connection.commit()


def main() -> None:
    parser = argparse.ArgumentParser(description="Import a JSON CPT eval dataset into SQLite.")
    parser.add_argument("input", type=Path, help="Path to JSON dataset file.")
    parser.add_argument("--db", type=Path, default=DEFAULT_DB, help="Path to SQLite database file.")
    args = parser.parse_args()

    import_dataset(args.db, args.input)
    print(f"Imported dataset from {args.input} into {args.db}")


if __name__ == "__main__":
    main()
