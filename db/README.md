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
    -> source_materials
      -> source_fragments
    -> requirements
      -> requirement_source_links
      -> requirement_quality_assessments
    -> test_cases
      -> test_case_steps
    -> requirement_test_case_links
    -> test_case_step_requirement_links
    -> unsupported_details
    -> external_reviews
      -> external_requirement_assessment_reviews
      -> external_test_case_reviews
```

External reviews never overwrite the primary human/project assessments. They store an independent second opinion and disagreement comments.

## PostgreSQL Later

The SQLite database is the local MVP storage. PostgreSQL migration should be done from the explicit schema and exported data, not by manually recreating tables.
