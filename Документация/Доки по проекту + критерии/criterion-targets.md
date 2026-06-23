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
| `decomposition_completeness` | 10 / 100% |
| `decomposition_boundaries` | 10 / корректные границы |
| `requirement_consolidation` | 10 / без дублей и потери смысла |

## Набор ТК

| Код в БД | Цель |
|---|---|
| `positive_coverage` | 10 / 100% |
| `negative_coverage` | 10 / 100% где применимо |
| `suite_cleanliness` | 10 / 0 лишних |
| `required_checks_coverage` | 10 / 100% |
| `overall_completeness` | 10 / достаточно для scope |

## Отдельные ТК

| Код в БД | Цель |
|---|---|
| `classification_correctness` | 10 / вид ТК корректен |
| `template_required_attributes` | 10 / 100% атрибутов |
| `conditions_quality` | 10 / условия корректны |
| `step_atomicity` | 10 / шаги атомарны |
| `expected_result_quality` | 10 / ожидаемый результат у каждого шага |
| `no_hallucinations` | 10 / 0 галлюцинаций |
