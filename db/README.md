# Database MVP

This folder contains the local database schema for the CPT eval dataset store.

## Files

- `schema.sql` - SQLite schema for datasets, source fragments, requirements, requirement quality assessments, test cases, traceability links, unsupported details, and future eval runs.
- `seed.sql` - initial quality criteria used to assess input requirements.

## Requirement Quality Criteria

The MVP seeds seven criteria:

- `source_quality` - source reliability and suitability.
- `completeness` - whether the requirement has enough information for generation without guessing.
- `consistency` - whether the requirement conflicts with itself or related sources.
- `correctness` - whether the requirement is valid for the domain/system.
- `ambiguity` - whether the wording is unambiguous.
- `testability` - whether test actions and expected results can be derived.
- `traceability` - whether the requirement can be linked to a concrete source fragment.

## Core Model

```text
datasets
  -> dataset_cases
    -> input_profile_code / input_profile_name
    -> source_materials
      -> source_fragments
    -> requirements
      -> requirement_source_links
      -> requirement_quality_assessments
    -> test_cases
      -> test_case_steps
      -> test_case_quality_assessments
    -> requirement_test_case_links
    -> test_case_step_requirement_links
    -> unsupported_details
    -> test_case_evaluation_results
    -> test_suite_quality_assessments
    -> external_reviews
      -> external_requirement_assessment_reviews
      -> external_test_case_reviews
```

External reviews never overwrite the primary human/project assessments. They store an independent second opinion and disagreement comments.

`test_cases` stores the test case artifact itself. `test_case_evaluation_results` stores the result of checking a generated test case against the expected dataset, including match, structure, classification, hallucination, unsupported detail count, score, and rationale.

`dataset_cases.input_profile_code` and `dataset_cases.input_profile_name` store the input-set profile from the criteria documents, for example full technical documentation, incomplete documentation, business-oriented documentation, noisy/conflicting documentation, or abstract documentation. This is intentionally a simple column, not a separate criteria table.

`test_case_quality_criteria` and `test_case_quality_assessments` describe the quality of an individual test case.

`test_suite_quality_criteria` and `test_suite_quality_assessments` describe the quality of a set of test cases for a scope such as a requirement, dataset case, dataset, or eval run.

## PostgreSQL Later

The SQLite database is the local MVP storage. PostgreSQL migration should be done from the explicit schema and exported data, not by manually recreating tables.
