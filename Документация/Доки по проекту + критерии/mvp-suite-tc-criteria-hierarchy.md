# MVP-критерии качества набора ТК и отдельного ТК

Документ фиксирует сокращенный набор критериев для первых прогонов. Расширенные критерии можно вернуть позже, если MVP-разметка покажет, что детализации недостаточно.

## Иерархия

```text
Входящие требования
  -> Декомпозиция требований
    -> Набор ТК
      -> Отдельный ТК
```

## Критерии

| ID | Уровень | Название в БД | Что проверяет | Порог | Как меряем |
| --- | --- | --- | --- | --- | --- |
| S1 | Набор ТК | `positive_coverage` | По требованиям есть необходимые позитивные тест-кейсы. | 100% для эталонного набора / >=95% для расширенного | авто + ревью |
| S2 | Набор ТК | `negative_coverage` | По требованиям есть негативные тест-кейсы там, где они нужны. | 100% для эталонного набора / >=95% для расширенного | авто + ревью |
| S3 | Набор ТК | `suite_cleanliness` | Нет лишних, нерелевантных и дублирующих тест-кейсов. | дублей 0, лишних 0 | авто + LLM-оценщик |
| S4 | Набор ТК | `required_checks_coverage` | Покрыты обязательные проверки из требований или эталона. | 100% | авто + ревью |
| S5 | Набор ТК | `overall_completeness` | Набор достаточен для проверяемого скоупа. | >=0.9 | LLM-оценщик + ревью |
| TC1 | Отдельный ТК | `classification_correctness` | Корректный вид ТК: UI / API / интеграционный. | >=0.9 | авто |
| TC2 | Отдельный ТК | `template_required_attributes` | ТК соответствует шаблону, есть обязательные атрибуты, ссылка на задачу и ссылка на требования. | 100% | авто |
| TC3 | Отдельный ТК | `conditions_quality` | У ТК есть корректные предусловия и постусловия; постусловия не содержат шаги. | >=0.9 | авто + LLM-оценщик |
| TC4 | Отдельный ТК | `step_atomicity` | Один шаг содержит одно действие. | >=0.9 | LLM-оценщик |
| TC5 | Отдельный ТК | `expected_result_quality` | У каждого шага есть ожидаемый результат, и он соответствует шагу. | >=0.9 | авто + LLM-оценщик |
| TC6 | Отдельный ТК | `no_hallucinations` | ТК не содержит фактов, деталей, UI/API/ролей, отсутствующих в требованиях и источниках. | галлюцинаций 0 | авто + LLM-оценщик |

## Что убрали из первых прогонов

Из набора ТК убраны отдельные критерии:

- `requirement_coverage`;
- `duplicate_rate`;
- `extra_relevant_test_case_rate`;
- `irrelevant_test_case_rate`;
- `coverage_balance`;
- `no_suite_level_hallucinations`;
- `insufficient_detail_handling`;
- `multi_requirement_traceability`.

Их смысл частично покрыт MVP-критериями `positive_coverage`, `negative_coverage`, `suite_cleanliness`, `required_checks_coverage` и `overall_completeness`.

Из отдельного ТК убраны отдельные критерии:

- `direction_correctness`;
- `template_compliance`;
- `required_fields_completeness`;
- `preconditions_quality`;
- `postconditions_quality`;
- `traceability_to_requirement`;
- `no_unsupported_specificity`;
- `step_action_quality`;
- `scenario_logic`.

Их смысл частично объединен в MVP-критерии `template_required_attributes`, `conditions_quality`, `step_atomicity`, `expected_result_quality` и `no_hallucinations`.
