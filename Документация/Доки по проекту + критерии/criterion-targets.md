# Целевые показатели критериев

Файл фиксирует целевые значения для отчетов по прогонам. Эти же цели хранятся в БД в полях:

- `target_score`
- `target_display`
- `target_description`

## Входные требования

| Код в БД | Цель |
|---|---|
| `source_quality` | 10 / подтвержденный источник |
| `completeness` | 10 / полное требование |
| `consistency` | 10 / без противоречий |
| `correctness` | 10 / корректно |
| `unambiguity` | 10 / однозначно |
| `testability` | 10 / проверяемо |
| `traceability` | 10 / трассируемо |
| `modifiability` | 10 / поддерживаемо |
| `atomicity` | 10 / атомарно |
| `feasibility` | 10 / выполнимо |

## Декомпозиция требований

| Код в БД | Цель |
|---|---|
| `decomposition_completeness` | 100% |
| `decomposition_boundaries` | 100% |
| `requirement_consolidation` | 100% |

## Набор ТК

| Код в БД | Цель |
|---|---|
| `positive_coverage` | 100% |
| `negative_coverage` | 100% |
| `suite_cleanliness` | 0 лишних |
| `required_checks_coverage` | 100% |
| `overall_completeness` | 100% |

## Отдельные ТК

| Код в БД | Цель |
|---|---|
| `classification_correctness` | ≥0,9 |
| `template_required_attributes` | 100% |
| `conditions_quality` | ≥0,9 |
| `step_atomicity` | ≥0,9 |
| `expected_result_quality` | ≥0,9 |
| `no_hallucinations` | галлюцинаций 0 |
