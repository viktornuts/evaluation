from __future__ import annotations

import argparse
import json
import sqlite3
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DB = ROOT / "data" / "cpt_eval.sqlite"
DEFAULT_OUT = ROOT / "exports"


def connect(db_path: Path) -> sqlite3.Connection:
    connection = sqlite3.connect(db_path)
    connection.row_factory = sqlite3.Row
    return connection


def rows(connection: sqlite3.Connection, query: str, params: tuple[Any, ...] = ()) -> list[dict[str, Any]]:
    return [dict(row) for row in connection.execute(query, params).fetchall()]


def one(connection: sqlite3.Connection, query: str, params: tuple[Any, ...] = ()) -> dict[str, Any]:
    row = connection.execute(query, params).fetchone()
    if row is None:
        raise ValueError("No row found for query")
    return dict(row)


def build_pack(connection: sqlite3.Connection, case_code: str) -> dict[str, Any]:
    case = one(
        connection,
        """
        SELECT dc.*, d.id AS dataset_id, d.name AS dataset_name, d.version AS dataset_version
        FROM dataset_cases dc
        JOIN datasets d ON d.id = dc.dataset_id
        WHERE dc.case_code = ?
        """,
        (case_code,),
    )

    sources = rows(
        connection,
        """
        SELECT sm.*, sf.id AS fragment_id, sf.fragment_ref, sf.fragment_text
        FROM source_materials sm
        LEFT JOIN source_fragments sf ON sf.source_material_id = sm.id
        WHERE sm.dataset_case_id = ?
        ORDER BY sm.id, sf.fragment_ref
        """,
        (case["id"],),
    )

    requirements = rows(
        connection,
        """
        SELECT *
        FROM requirements
        WHERE dataset_case_id = ? AND origin = 'expected'
        ORDER BY requirement_code
        """,
        (case["id"],),
    )

    for requirement in requirements:
        requirement["source_links"] = rows(
            connection,
            """
            SELECT rsl.*, sf.fragment_ref, sf.fragment_text, sm.source_type, sm.source_name
            FROM requirement_source_links rsl
            JOIN source_fragments sf ON sf.id = rsl.source_fragment_id
            JOIN source_materials sm ON sm.id = sf.source_material_id
            WHERE rsl.requirement_id = ?
            ORDER BY sm.id, sf.fragment_ref
            """,
            (requirement["id"],),
        )
        requirement["quality_assessments"] = rows(
            connection,
            """
            SELECT
                rqa.id AS assessment_id,
                qc.id AS criterion_id,
                qc.code AS criterion,
                qc.name AS criterion_name,
                rqa.score,
                rqa.label,
                rqa.rationale,
                rqa.assessed_by,
                rqa.assessment_method,
                rqa.confidence
            FROM requirement_quality_assessments rqa
            JOIN quality_criteria qc ON qc.id = rqa.criterion_id
            WHERE rqa.requirement_id = ?
            ORDER BY qc.code
            """,
            (requirement["id"],),
        )

    test_cases = rows(
        connection,
        """
        SELECT *
        FROM test_cases
        WHERE dataset_case_id = ? AND origin = 'expected'
        ORDER BY test_case_code
        """,
        (case["id"],),
    )
    for test_case in test_cases:
        test_case["requirement_links"] = rows(
            connection,
            """
            SELECT rtcl.*, r.requirement_code, r.requirement_text
            FROM requirement_test_case_links rtcl
            JOIN requirements r ON r.id = rtcl.requirement_id
            WHERE rtcl.test_case_id = ?
            ORDER BY r.requirement_code
            """,
            (test_case["id"],),
        )
        test_case["steps"] = rows(
            connection,
            """
            SELECT *
            FROM test_case_steps
            WHERE test_case_id = ?
            ORDER BY step_number
            """,
            (test_case["id"],),
        )
        for step in test_case["steps"]:
            step["requirement_links"] = rows(
                connection,
                """
                SELECT tsrl.*, r.requirement_code, r.requirement_text
                FROM test_case_step_requirement_links tsrl
                JOIN requirements r ON r.id = tsrl.requirement_id
                WHERE tsrl.test_case_step_id = ?
                ORDER BY r.requirement_code
                """,
                (step["id"],),
            )

    unsupported_details = rows(
        connection,
        """
        SELECT ud.*, tc.test_case_code, tcs.step_number
        FROM unsupported_details ud
        JOIN test_cases tc ON tc.id = ud.test_case_id
        LEFT JOIN test_case_steps tcs ON tcs.id = ud.test_case_step_id
        WHERE tc.dataset_case_id = ?
        ORDER BY tc.test_case_code, tcs.step_number
        """,
        (case["id"],),
    )

    return {
        "review_task": {
            "instruction": (
                "Review the project assessments without overwriting them. "
                "For each requirement criterion, decide whether you agree with the original score/label. "
                "Return only disagreements or important confirmations in the external review JSON format."
            ),
            "expected_external_review_shape": {
                "external_review": {
                    "id": "external_review_CASE-001_deepseek_001",
                    "dataset_id": case["dataset_id"],
                    "dataset_case_id": case["id"],
                    "reviewer_name": "deepseek",
                    "reviewer_type": "llm",
                    "model_name": "model-name",
                    "prompt_version": "v1",
                    "review_status": "completed",
                    "summary": "Short summary"
                },
                "requirement_assessment_reviews": [
                    {
                        "id": "ext_req_rev_001",
                        "requirement_id": "requirement id from pack",
                        "criterion": "completeness",
                        "original_assessment_id": "assessment id from pack",
                        "reviewer_score": 3,
                        "reviewer_label": "partially_complete",
                        "agreement_status": "disagree",
                        "reviewer_comment": "Why the external reviewer disagrees.",
                        "severity": "major"
                    }
                ],
                "test_case_reviews": []
            },
        },
        "dataset_case": case,
        "sources": sources,
        "requirements": requirements,
        "test_cases": test_cases,
        "unsupported_details": unsupported_details,
    }


def render_markdown(pack: dict[str, Any]) -> str:
    case = pack["dataset_case"]
    lines = [
        f"# External Review Pack: {case['case_code']} - {case['title']}",
        "",
        "## Task",
        "",
        "Review the existing requirement quality assessments. Do not overwrite them.",
        "Point out where you disagree, what score/label you would assign, and why.",
        "",
        "Return a structured JSON object matching `expected_external_review_shape` from the companion JSON file.",
        "",
        "## Dataset Case",
        "",
        f"- Dataset: `{case['dataset_name']}` `{case['dataset_version']}`",
        f"- Case ID: `{case['id']}`",
        f"- Case code: `{case['case_code']}`",
        f"- Title: {case['title']}",
        f"- Description: {case.get('description') or ''}",
        "",
        "## Source Fragments",
        "",
    ]

    for source in pack["sources"]:
        lines.extend(
            [
                f"### `{source.get('fragment_id')}` - {source.get('fragment_ref')}",
                "",
                f"- Source: {source.get('source_type')} / {source.get('source_name')}",
                "",
                source.get("fragment_text") or "",
                "",
            ]
        )

    lines.append("## Requirements And Project Assessments")
    lines.append("")
    for requirement in pack["requirements"]:
        lines.extend(
            [
                f"### `{requirement['id']}` / {requirement['requirement_code']}",
                "",
                requirement["requirement_text"],
                "",
                f"- Expected status: `{requirement['expected_status']}`",
                f"- Quality profile: `{requirement.get('quality_profile_status')}`",
                f"- Risk level: `{requirement.get('risk_level')}`",
                "",
                "Assessments:",
                "",
            ]
        )
        for assessment in requirement["quality_assessments"]:
            lines.extend(
                [
                    f"- `{assessment['criterion']}`: score `{assessment['score']}`, label `{assessment['label']}`",
                    f"  - assessment_id: `{assessment['assessment_id']}`",
                    f"  - rationale: {assessment.get('rationale') or ''}",
                ]
            )
        lines.append("")

    lines.append("## Expected Test Cases")
    lines.append("")
    for test_case in pack["test_cases"]:
        lines.extend(
            [
                f"### `{test_case['id']}` / {test_case['test_case_code']}",
                "",
                f"- Title: {test_case['title']}",
                f"- Type: `{test_case.get('test_case_type')}`",
                f"- Direction: `{test_case.get('direction')}`",
                "",
                "Requirement links:",
                "",
            ]
        )
        for link in test_case["requirement_links"]:
            lines.append(f"- `{link['requirement_id']}` / {link['requirement_code']}: {link.get('rationale') or ''}")
        lines.append("")
        lines.append("Steps:")
        lines.append("")
        for step in test_case["steps"]:
            lines.extend(
                [
                    f"{step['step_number']}. Action: {step['action']}",
                    f"   Expected result: {step['expected_result']}",
                ]
            )
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def export_pack(db_path: Path, case_code: str, output_dir: Path) -> tuple[Path, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    with connect(db_path) as connection:
        pack = build_pack(connection, case_code)

    safe_case = case_code.lower().replace("-", "_")
    json_path = output_dir / f"review_pack_{safe_case}.json"
    md_path = output_dir / f"review_pack_{safe_case}.md"
    json_path.write_text(json.dumps(pack, ensure_ascii=False, indent=2), encoding="utf-8")
    md_path.write_text(render_markdown(pack), encoding="utf-8")
    return json_path, md_path


def main() -> None:
    parser = argparse.ArgumentParser(description="Export a dataset case review pack for external AI review.")
    parser.add_argument("case_code", help="Dataset case code, for example CASE-001.")
    parser.add_argument("--db", type=Path, default=DEFAULT_DB, help="Path to SQLite database file.")
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT, help="Output directory.")
    args = parser.parse_args()

    json_path, md_path = export_pack(args.db, args.case_code, args.out)
    print(f"Exported JSON review pack: {json_path}")
    print(f"Exported Markdown review pack: {md_path}")


if __name__ == "__main__":
    main()
