# Dataset Imports

This folder stores dataset-level import artifacts.

Use it for source files and generated import JSON that describe a dataset itself:

- gold requirements;
- gold test cases;
- normalized import JSON;
- intermediate parsing files used to build the dataset import.

Do not use this folder for generated AI outputs from eval rounds. Round files must go to:

```text
imports/rounds/<run_code>/source/
imports/rounds/<run_code>/extracted/
```

## Naming Convention

Dataset folder name:

```text
<dataset_code>_<version>
```

Examples:

```text
customer_gold_v1/
cpt_smoke_v1/
release_integration_bad_requirements_v1/
release_integration_multi_source_v1/
```

`dataset_code` must be stable and must not include the eval round number. The same dataset can be used in many rounds.

Recommended dataset codes:

- short;
- lowercase;
- words separated by `_`;
- include the business area or feature;
- include the requirement profile when it matters, for example `bad_requirements`, `multi_source`, `abstract_docs`;
- end with a version suffix such as `_v1`, `_v2`.

The folder name should match or clearly map to:

- `datasets.id` in the DB;
- `datasets.name`;
- `datasets.version`;
- `dataset_cases.case_code`;
- filenames used in eval rounds.

## Input Profiles

Every dataset case must have an `input_profile_code`. The profile defines what result is considered the target for this dataset.

Current profile codes:

- `customer_gold_requirements` - customer gold dataset with expected full match to gold requirements and gold test cases;
- `complete_technical_docs` - complete technical documentation, expected full coverage;
- `incomplete_fragmented_docs` - incomplete/fragmented documentation, expected safe partial coverage without invented details;
- `business_user_story_docs` - business or user-story documentation, expected coverage of the checkable business core;
- `conflicting_noisy_docs` - noisy or contradictory documentation, expected filtering of noise and explicit handling of conflicts;
- `abstract_high_level_docs` - high-level abstract documentation, expected coverage of the checkable core and explicit gap marking.

Targets are stored in DB:

```text
dataset_input_profiles
dataset_profile_criterion_targets
dataset_case_criterion_targets
```

Use `dataset_case_criterion_targets` only when one concrete dataset case has special targets that differ from the profile template.

## Dataset Case Naming

Inside a dataset use stable `case_code` values:

```text
GOLD-REQ-001
BADREQ-001
MULTISRC-001
NOISY-001
ABSTRACT-001
```

Round files must include both `dataset_code` and `case_code` when a round contains more than one case:

```text
Декомпозиция_<dataset_code>__<case_code>.*
ТК_<dataset_code>__<case_code>.*
```

Example:

```text
Декомпозиция_release_integration_bad_requirements_v1__BADREQ-001.xlsx
ТК_release_integration_bad_requirements_v1__BADREQ-001.xlsx
```

## Recommended Folder Shape

```text
imports/datasets/<dataset_code>_<version>/
  README.md
  source/
  normalized/
  import/
```

For the current MVP, keeping files directly in the dataset folder is allowed when the dataset is small. For larger datasets, prefer the structure above.

Suggested meaning:

- `source/` - original user/customer files;
- `normalized/` - cleaned intermediate files;
- `import/` - final JSON files that can be passed to import scripts.

## Current Dataset Imports

```text
imports/datasets/customer_gold_v1/
```

This is the high-priority customer gold dataset used as the current reference baseline.

It currently contains:

- `customer_gold_v1_requirement_rows.json` - intermediate requirement rows;
- `customer_gold_v1_requirements.json` - normalized/importable gold requirements;
- `customer_gold_v1_test_cases.xlsx` - source gold test cases;
- `customer_gold_v1_test_cases.json` - normalized/importable gold test cases.

The readable dataset documentation lives separately:

```text
Документация/Датасеты/customer_gold_v1/
```

## Instruction For External AI

When another AI or another tester adds a new dataset, tell them:

```text
Add the dataset under `imports/datasets/<dataset_code>_<version>/`.

Do not put dataset files directly into the root `imports/` folder.
Do not mix dataset source files with eval-round files.

Use a clear dataset code that matches the DB and future round files.
For example:
- `customer_gold_v1`
- `release_integration_multi_source_v1`
- `release_integration_bad_requirements_v1`

For every dataset case, choose and write `input_profile_code`.
This profile controls what `10/10` means for the dataset.
Do not assume that poor/incomplete requirements require the same full-coverage target as a gold dataset.

Put original dataset files under `source/` when possible.
Put cleaned intermediate files under `normalized/`.
Put final JSON import files under `import/`.

After adding the dataset, update:
- `imports/datasets/README.md`;
- `Документация/Датасеты/<dataset_code>_<version>/README.md`;
- any import script paths that reference the dataset.
```
