# Dataset Import Format

This folder is for input files that should be imported into the local eval database.

The current MVP importer accepts one JSON file with this shape:

```json
{
  "dataset": {
    "id": "dataset_cpt_smoke_v1",
    "name": "cpt_smoke",
    "version": "v1",
    "description": "Small smoke dataset for CPT eval",
    "status": "draft"
  },
  "cases": [
    {
      "id": "case_password_recovery",
      "case_code": "CASE-001",
      "title": "Password recovery requirements",
      "input_profile_code": "complete_technical_docs",
      "input_profile_name": "Structured and complete technical documentation",
      "source_materials": [],
      "requirements": [],
      "test_cases": [],
      "requirement_test_case_links": [],
      "unsupported_details": []
    }
  ]
}
```

Each expected requirement should have:

- source links to one or more `source_fragments`;
- ten quality assessments: `source_quality`, `correctness`, `unambiguity`, `completeness`, `consistency`, `testability`, `traceability`, `modifiability`, `atomicity`, `feasibility`;
- an `expected_status`, for example `ready_for_generation` or `insufficient_detail`.

`input_profile_code` / `input_profile_name` describe the source-input profile for the case. Use these for the five input-set types from the criteria documents, for example:

- `complete_technical_docs`
- `incomplete_fragmented_docs`
- `business_user_story_docs`
- `conflicting_noisy_docs`
- `abstract_high_level_docs`

Each expected test case should be linked to requirements through `requirement_test_case_links`.
For better traceability, each step should also either link to requirements or be marked through `unsupported_details`.

## External Review Format

External AI reviews should not overwrite project assessments. They are imported as a second opinion.

Minimal shape:

```json
{
  "external_review": {
    "id": "external_review_CASE-001_deepseek_001",
    "dataset_id": "dataset_cpt_smoke_v1",
    "dataset_case_id": "case_password_recovery",
    "reviewer_name": "deepseek",
    "reviewer_type": "llm",
    "model_name": "deepseek-model",
    "prompt_version": "v1",
    "review_status": "completed",
    "summary": "Short summary"
  },
  "requirement_assessment_reviews": [
    {
      "id": "external_review_item_001",
      "requirement_id": "req_fast_processing",
      "criterion": "correctness",
      "original_assessment_id": "rqa_req002_correctness",
      "reviewer_score": 2,
      "reviewer_label": "likely_not_assessable",
      "agreement_status": "disagree",
      "reviewer_comment": "Why the reviewer disagrees.",
      "severity": "minor"
    }
  ],
  "test_case_reviews": []
}
```

Use `scripts/export_review_pack.py CASE-001` to generate JSON and Markdown context files for an external reviewer.
