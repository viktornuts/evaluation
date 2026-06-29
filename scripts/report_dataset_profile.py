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
                COUNT(DISTINCT ir.id) AS input_requirements,
                COUNT(DISTINCT r.id) AS requirements,
                COUNT(DISTINCT tc.id) AS test_cases,
                COUNT(DISTINCT tcs.id) AS test_case_steps
            FROM datasets d
            LEFT JOIN dataset_cases dc ON dc.dataset_id = d.id
            LEFT JOIN input_requirements ir ON ir.dataset_case_id = dc.id
            LEFT JOIN requirements r ON r.dataset_case_id = dc.id
            LEFT JOIN test_cases tc ON tc.dataset_case_id = dc.id
            LEFT JOIN test_case_steps tcs ON tcs.test_case_id = tc.id
            GROUP BY d.id
            ORDER BY d.name, d.version
            """
        ).fetchall()
        print_rows("Dataset overview", overview)

        input_profiles = connection.execute(
            """
            SELECT
                COALESCE(input_profile_code, 'not_set') AS input_profile_code,
                COALESCE(input_profile_name, 'not_set') AS input_profile_name,
                COUNT(*) AS cases
            FROM dataset_cases
            GROUP BY COALESCE(input_profile_code, 'not_set'), COALESCE(input_profile_name, 'not_set')
            ORDER BY cases DESC, input_profile_code
            """
        ).fetchall()
        print_rows("Dataset case input profiles", input_profiles)

        corner_case_summary = connection.execute(
            """
            SELECT
                corner_case_code,
                class_name,
                min_examples,
                linked_example_count,
                linked_dataset_case_count,
                primary_link_count,
                secondary_link_count,
                min_examples_status
            FROM corner_case_coverage_summary
            ORDER BY corner_case_code
            """
        ).fetchall()
        print_rows("Corner case coverage summary", corner_case_summary)

        corner_case_links = connection.execute(
            """
            SELECT
                corner_case_code,
                dataset_name,
                dataset_version,
                case_code,
                link_role,
                example_count,
                coverage_status
            FROM corner_case_dataset_coverage
            ORDER BY corner_case_code, dataset_name, dataset_version, case_code, link_role
            """
        ).fetchall()
        print_rows("Corner case links by dataset case", corner_case_links)

        decomposition_profile = connection.execute(
            """
            SELECT
                dc.case_code,
                COUNT(DISTINCT ir.id) AS input_requirements,
                COUNT(DISTINCT irdl.id) AS decomposition_links,
                COUNT(DISTINCT CASE WHEN irdl.link_type = 'expected_atomic_requirement' THEN irdl.id END)
                    AS expected_decomposition_links,
                COUNT(DISTINCT CASE WHEN irdl.link_type = 'generated_atomic_requirement' THEN irdl.id END)
                    AS generated_decomposition_links
            FROM dataset_cases dc
            LEFT JOIN input_requirements ir ON ir.dataset_case_id = dc.id
            LEFT JOIN input_requirement_decomposition_links irdl ON irdl.input_requirement_id = ir.id
            GROUP BY dc.id
            ORDER BY dc.case_code
            """
        ).fetchall()
        print_rows("Requirement decomposition profile", decomposition_profile)

        decomposition_quality = connection.execute(
            """
            SELECT
                rdqc.code AS criterion,
                rdqa.label,
                COUNT(*) AS count,
                ROUND(AVG(rdqa.score), 2) AS avg_score
            FROM requirement_decomposition_quality_assessments rdqa
            JOIN requirement_decomposition_quality_criteria rdqc ON rdqc.id = rdqa.criterion_id
            GROUP BY rdqc.code, rdqa.label
            ORDER BY rdqc.code, count DESC, rdqa.label
            """
        ).fetchall()
        print_rows("Requirement decomposition quality assessments", decomposition_quality)

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

        source_profile = connection.execute(
            """
            SELECT
                case_code,
                requirement_count,
                avg_source_materials_per_requirement,
                max_source_materials_per_requirement,
                no_source_requirements,
                single_source_requirements,
                multi_source_requirements
            FROM dataset_case_requirement_source_profile
            ORDER BY case_code
            """
        ).fetchall()
        print_rows("Requirement source profile by dataset case", source_profile)

        source_distribution = connection.execute(
            """
            SELECT
                case_code,
                source_material_count,
                COUNT(*) AS requirements
            FROM requirement_source_summary
            GROUP BY case_code, source_material_count
            ORDER BY case_code, source_material_count
            """
        ).fetchall()
        print_rows("Requirement source count distribution", source_distribution)

        quality = connection.execute(
            """
            SELECT qc.code AS criterion, rqa.label, COUNT(*) AS count, ROUND(AVG(rqa.score), 2) AS avg_score
            FROM requirement_quality_assessments rqa
            JOIN requirement_quality_criteria qc ON qc.id = rqa.criterion_id
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

        test_case_quality = connection.execute(
            """
            SELECT
                tcqc.code AS criterion,
                tcqa.label,
                COUNT(*) AS count,
                ROUND(AVG(tcqa.score), 2) AS avg_score
            FROM test_case_quality_assessments tcqa
            JOIN test_case_quality_criteria tcqc ON tcqc.id = tcqa.criterion_id
            GROUP BY tcqc.code, tcqa.label
            ORDER BY tcqc.code, count DESC, tcqa.label
            """
        ).fetchall()
        print_rows("Test case quality assessments", test_case_quality)

        test_suite_quality = connection.execute(
            """
            SELECT
                tsqa.scope_type,
                tsqc.code AS criterion,
                tsqa.label,
                COUNT(*) AS count,
                ROUND(AVG(tsqa.score), 2) AS avg_score
            FROM test_suite_quality_assessments tsqa
            JOIN test_suite_quality_criteria tsqc ON tsqc.id = tsqa.criterion_id
            GROUP BY tsqa.scope_type, tsqc.code, tsqa.label
            ORDER BY tsqa.scope_type, tsqc.code, count DESC, tsqa.label
            """
        ).fetchall()
        print_rows("Test suite quality assessments", test_suite_quality)


def main() -> None:
    parser = argparse.ArgumentParser(description="Print a profile report for the CPT eval dataset.")
    parser.add_argument("--db", type=Path, default=DEFAULT_DB, help="Path to SQLite database file.")
    args = parser.parse_args()

    report(args.db)


if __name__ == "__main__":
    main()
