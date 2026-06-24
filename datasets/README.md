# Datasets

Canonical project folder for dataset-specific materials.

Each dataset should live in a separate folder with a stable technical code:

```text
datasets/
  <dataset_code>/
    README.md
    source/
    requirements/
    test_cases/
    runs/
```

Recommended `dataset_code` examples:

- `customer_gold_v1`
- `incomplete_requirements_v1`
- `conflicting_requirements_v1`
- `multi_source_requirements_v1`
- `noisy_requirements_v1`

## Required Dataset Metadata

Every dataset folder should document:

- `dataset_code` - stable technical identifier;
- `dataset_name` - human-readable name;
- `input_profile_code` - profile of input requirements;
- `case_code` values inside the dataset;
- source files used to create requirements;
- expected requirements and expected test cases, if available;
- generated run artifacts, if stored outside the database.

## Import Rule

Generated test-case exports should not rely on test-case titles to identify a dataset.
Use explicit fields when possible:

```text
dataset_code
case_code
run_code
```

If exports are delivered as separate files, use a stable filename convention:

```text
run_<run_code>__<dataset_code>__<case_code>.xlsx
```

The database remains the source of truth for assessments.
This folder stores source artifacts, readable copies, and run history files.

