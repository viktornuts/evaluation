# customer_gold_v1

Golden customer dataset for the CPT eval MVP.

## Metadata

| Field | Value |
|---|---|
| `dataset_code` | `customer_gold_v1` |
| `dataset_id` | `dataset_customer_gold_v1` |
| `case_code` | `release_integration` |
| `dataset_case_id` | `case_customer_gold_release_integration` |
| `input_profile_code` | `gold_good` |
| `input_profile_name` | Эталонные требования заказчика |

## Current Source Locations

Readable dataset materials currently also live in:

```text
Документация/Датасеты/customer_gold_v1/
```

The current DB state is stored in:

```text
data/cpt_eval.sqlite
```

Generated round inputs for the current demo live in:

```text
imports/round_v1_generated_test_cases.txt
imports/round_v1_output.xlsx
imports/round_v2_output.xlsx
```

PDF report history is generated into:

```text
exports/pdf/history/
```

## Intended Folder Layout

```text
datasets/customer_gold_v1/
  source/
  requirements/
  test_cases/
  runs/
```

For the next datasets, this top-level `datasets/` structure should be used directly.

