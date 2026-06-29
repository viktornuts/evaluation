# Database MVP

This folder contains the local database schema for the CPT eval dataset store.

## Files

- `schema.sql` - SQLite schema for datasets, source fragments, requirements, requirement quality assessments, test cases, traceability links, unsupported details, and future eval runs.
- `seed.sql` - initial quality criteria and scoring rubrics used to assess input requirements.
- `profile_targets.sql` - input profiles and profile-specific target values for criteria.
- `corner_cases.sql` - corner-case catalog `CC-01`..`CC-18`.

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
dataset_input_profiles
  -> dataset_profile_criterion_targets
corner_cases
datasets
  -> eval_runs
  -> dataset_cases
    -> input_profile_code / input_profile_name
    -> dataset_case_criterion_targets
    -> dataset_case_corner_case_links
    -> source_materials
      -> source_fragments
    -> input_requirements
      -> input_requirement_corner_case_links
      -> input_requirement_decomposition_links
    -> requirements
      -> requirement_source_links
      -> requirement_quality_assessments
    -> requirement_decomposition_evaluation_results
      -> requirement_decomposition_quality_assessments
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

`eval_runs` stores an agent run against a dataset. It fixes the factors we can tune between runs: agent name/version, prompt text with examples, model name/version, `temperature`, `top_p`, run mode, retrieval parameters, reranker, response format strictness, and dataset version snapshot. Generated requirements, generated test cases, suite assessments, and evaluation results can link back to the exact run through `eval_run_id`.

Required run fields are `agent_name`, `agent_version`, `prompt_snapshot`, `model_name`, `model_version`, `temperature`, `top_p`, `run_mode`, and `response_format_strictness`. `retrieval_chunk_size`, `retrieval_top_k`, and `reranker_name` are used when `run_mode` is `rag_search` or `hybrid`.

`input_requirements` stores large source requirements before agent decomposition. `input_requirement_decomposition_links` connects each large input requirement to expected or generated atomic requirements in `requirements`. `requirement_decomposition_evaluation_results` stores comparison results between generated atomic requirements and the expected decomposition.

`requirement_decomposition_quality_criteria` and `requirement_decomposition_quality_assessments` describe the quality of the agent decomposition result. The initial customer criteria are `decomposition_completeness`, `decomposition_boundaries`, and `requirement_consolidation`.

`test_cases` stores the test case artifact itself. `test_case_evaluation_results` stores the result of checking a generated test case against the expected dataset, including match, structure, classification, hallucination, unsupported detail count, score, and rationale.

`dataset_cases.input_profile_code` and `dataset_cases.input_profile_name` store the input-set profile from the criteria documents, for example full technical documentation, incomplete documentation, business-oriented documentation, noisy/conflicting documentation, or abstract documentation.

`dataset_input_profiles` stores the allowed profile catalog. `dataset_profile_criterion_targets` stores default target values for each profile and criterion. This lets the same criterion mean different expected behavior for different inputs. For example, for `customer_gold_requirements` the target is full gold coverage, while for `incomplete_fragmented_docs` the target is safe partial coverage without hallucinations.

`dataset_case_criterion_targets` stores overrides for one concrete dataset case. Target lookup order is:

1. `dataset_case_criterion_targets` for the exact `dataset_case_id`;
2. `dataset_profile_criterion_targets` for `dataset_cases.input_profile_code`;
3. global `target_score` / `target_display` / `target_description` in the criterion table.

This means a poor-requirements dataset can still receive `10/10` when the agent behaves correctly for that profile: covers the derivable part, marks gaps, and does not invent missing details.

`corner_cases` stores the catalog of corner cases from the dataset collection plan, for example `CC-05` for contradictory requirements or `CC-18` for E2E classification.

`dataset_case_corner_case_links` connects a dataset case to one or more corner cases. A link has:

- `link_role` - `primary` or `secondary`;
- `example_count` - how many input examples in this dataset case cover the corner case;
- `coverage_status` - `planned`, `collected`, `imported`, `reference_ready`, or `ready_for_run`;
- `rationale`.

`input_requirement_corner_case_links` connects a concrete input requirement to one or more corner cases. Use it when one requirement/example covers several `CC-xx` values.

Useful views:

- `corner_case_dataset_coverage` - shows which dataset cases cover each corner case;
- `corner_case_coverage_summary` - summarizes linked example counts and whether `min_examples` is reached.

`requirement_source_summary` is a view that shows how many source fragments and source materials are linked to each requirement.

`dataset_case_requirement_source_profile` is a view that summarizes source complexity for each dataset case: average source materials per requirement, max source materials per requirement, and counts of requirements with zero, one, or multiple sources.

`test_case_quality_criteria` and `test_case_quality_assessments` describe the quality of an individual test case.

`test_case_quality_criterion_score_levels` stores the scoring rubric for individual test-case criteria on the same `0..10` scale.

`test_suite_quality_criteria` and `test_suite_quality_assessments` describe the quality of a set of test cases for a scope such as a requirement, dataset case, dataset, or eval run.

`test_suite_quality_criterion_score_levels` stores the scoring rubric for test-suite criteria on the same `0..10` scale.

## PostgreSQL Later

The SQLite database is the local MVP storage. PostgreSQL migration should be done from the explicit schema and exported data, not by manually recreating tables.
