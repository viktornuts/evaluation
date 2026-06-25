# Заметки по customer_gold_v1

Статус: эталонные требования импортированы в БД.

Приоритет: super high.

Источник требований: `source/source_requirements.pdf`.

Импортный файл: `imports/datasets/customer_gold_v1/customer_gold_v1_requirements.json`.

На текущем этапе 30 требований заведены как `expected`-требования золотого датасета. По договоренности для этого эталона всем требованиям выставлен score `10.0` по всем 10 критериям качества требований:

- `source_quality`
- `completeness`
- `consistency`
- `correctness`
- `unambiguity`
- `testability`
- `traceability`
- `modifiability`
- `atomicity`
- `feasibility`

Эталонные тест-кейсы импортированы из `test-cases/source/gold_test_cases.xlsx`.

Импортный файл ТК: `imports/datasets/customer_gold_v1/customer_gold_v1_test_cases.json`.

Заведено:

- 14 эталонных тест-кейсов;
- 30 шагов;
- 37 связей `требование -> тест-кейс`;
- 94 связи `шаг тест-кейса -> требование`.

По листу покрытия `REQ-27` и `REQ-30` имеют статус `insufficient_detail` и не имеют эталонных ТК.
