# Database MVP

This folder contains the local database schema for the CPT eval dataset store.

## Files

- `schema.sql` - SQLite schema for datasets, source fragments, requirements, requirement quality assessments, test cases, traceability links, unsupported details, and future eval runs.
- `seed.sql` - initial quality criteria and scoring rubrics used to assess input requirements.

## Quality Score Scale

Manual quality assessments use a decimal `0..10` scale:

- `10` - fully satisfies the criterion.
- `8-9` - good, only minor issues.
- `6-7` - acceptable but noticeably imperfect.
- `4-5` - weak or risky.
- `1-3` - severe problems.
- `0` - absent, contradicted, or unusable.

Reports can present this as a percentage directly: `score 8 = 80%`.
For precise assessments, decimal scores are allowed: `score 6.7 = 67%`.

## Requirement Quality Criteria

The MVP seeds ten requirement criteria:

- `source_quality` - source reliability and suitability.
- `correctness` - whether the requirement is valid for the domain/system.
- `unambiguity` - whether the wording is unambiguous.
- `completeness` - whether the requirement has enough information for generation without guessing.
- `consistency` - whether the requirement conflicts with itself or related sources.
- `testability` - whether test actions and expected results can be derived.
- `traceability` - whether the requirement can be linked to a concrete source fragment.
- `modifiability` - whether the requirement can be changed safely without uncontrolled duplication.
- `atomicity` - whether the requirement describes one behavior or function.
- `feasibility` - whether the requirement is technically feasible and not contradictory.

`requirement_quality_criterion_score_levels` stores the scoring rubric for requirement criteria. Each criterion has score bands for `10`, `8-9`, `6-7`, `4-5`, `1-3`, and `0`, so assessors can use the same interpretation of the `0..10` scale.

## Core Model

```text
requirement_quality_criteria
  -> requirement_quality_criterion_score_levels
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

`requirement_source_summary` is a view that shows how many source fragments and source materials are linked to each requirement.

`dataset_case_requirement_source_profile` is a view that summarizes source complexity for each dataset case: average source materials per requirement, max source materials per requirement, and counts of requirements with zero, one, or multiple sources.

`test_case_quality_criteria` and `test_case_quality_assessments` describe the quality of an individual test case.

`test_case_quality_criterion_score_levels` stores the scoring rubric for individual test-case criteria on the same `0..10` scale.

`test_suite_quality_criteria` and `test_suite_quality_assessments` describe the quality of a set of test cases for a scope such as a requirement, dataset case, dataset, or eval run.

`test_suite_quality_criterion_score_levels` stores the scoring rubric for test-suite criteria on the same `0..10` scale.

## PostgreSQL Later

The SQLite database is the local MVP storage. PostgreSQL migration should be done from the explicit schema and exported data, not by manually recreating tables.
