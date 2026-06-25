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

Put original dataset files under `source/` when possible.
Put cleaned intermediate files under `normalized/`.
Put final JSON import files under `import/`.

After adding the dataset, update:
- `imports/datasets/README.md`;
- `Документация/Датасеты/<dataset_code>_<version>/README.md`;
- any import script paths that reference the dataset.
```
