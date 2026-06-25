# Imports

This folder is for input files that should be imported into the local eval database.

## Round Input Structure

Every new eval round must get its own folder:

```text
imports/
  datasets/
    <dataset_code>_<version>/
  rounds/
    <run_code>/
      source/
      extracted/
      notes.md
```

Current example:

```text
imports/datasets/customer_gold_v1/customer_gold_v1_requirements.json
imports/datasets/customer_gold_v1/customer_gold_v1_test_cases.json
imports/rounds/v0/source/round_v1_generated_test_cases.txt
imports/rounds/v1/source/round_v1_output.xlsx
imports/rounds/v2/source/round_v2_output.xlsx
```

Dataset-level imports must go under:

```text
imports/datasets/<dataset_code>_<version>/
```

Do not place dataset imports directly in the root `imports/` folder. See:

```text
imports/datasets/README.md
```

When the user sends "Новый раунд", place the original user-provided archive/files under:

```text
imports/rounds/<run_code>/source/
```

If files are extracted from an archive, keep the original archive in `source/` and put extracted files under:

```text
imports/rounds/<run_code>/extracted/
```

Do not mix files from different rounds in the root `imports/` folder.

## Dataset Import Format

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
      "input_requirements": [],
      "requirements": [],
      "input_requirement_decomposition_links": [],
      "test_cases": [],
      "requirement_test_case_links": [],
      "unsupported_details": []
    }
  ]
}
```

`input_requirements` stores the large source requirements before decomposition. Use it when the agent first splits a source requirement into smaller atomic requirements. Each item should contain:

- `id`;
- `input_requirement_code`;
- `requirement_text`;
- optional `title`;
- optional `source_fragment_id`;
- optional `requirement_order`.

`requirements` stores the expected or generated atomic requirements after decomposition.

`input_requirement_decomposition_links` connects one large input requirement to its atomic requirements. Use `link_type = expected_atomic_requirement` for the gold decomposition and `link_type = generated_atomic_requirement` for agent output.

Each expected requirement should have:

- source links to one or more `source_fragments`;
- ten quality assessments: `source_quality`, `correctness`, `unambiguity`, `completeness`, `consistency`, `testability`, `traceability`, `modifiability`, `atomicity`, `feasibility`;
- an `expected_status`, for example `ready_for_generation` or `insufficient_detail`.

Quality assessment scores use a decimal 0-10 scale:

- `10` - fully satisfies the criterion;
- `8-9` - good, only minor issues;
- `6-7` - acceptable but noticeably imperfect;
- `4-5` - weak or risky;
- `1-3` - severe problems;
- `0` - absent, contradicted, or unusable.

Decimal scores are allowed for more precise percentages, for example `6.7 = 67%`.

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
      "reviewer_score": 4,
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
