# Промпт для сторонней ИИ-оценки eval-раунда

Ниже текст, который можно передать другой ИИ, чтобы она понимала, как работать с проектом, БД и отчетами.

```text
Ты работаешь с проектом оценки качества AI-агента CPT.

Цель проекта:
оценивать не факт генерации, а качество результата ИИ:
1. как агент декомпозирует входные требования в атомарные требования;
2. как агент генерирует набор тест-кейсов;
3. как агент генерирует отдельные тест-кейсы;
4. как меняется качество между раундами/версиями агента.

Работай в отдельной git-ветке. Не перетирай существующие оценки и историю раундов без явного указания.

Основная БД:
data/cpt_eval.sqlite

Основные документы:
Документация/Доки по проекту + критерии/scoring-methodology.md
Документация/Доки по проекту + критерии/reporting-rules.md
Документация/Доки по проекту + критерии/new-round-workflow.md

PDF-методология:
exports/pdf/methodology/scoring_methodology.pdf

Актуальный PDF-отчет:
exports/pdf/eval_rounds_report_latest.pdf

История PDF-отчетов:
exports/pdf/history/<run_code>/eval_rounds_report_<run_code>.pdf

Каноническая папка датасетов:
datasets/

Структура входов/выходов по раундам:
imports/rounds/<run_code>/source/
imports/rounds/<run_code>/extracted/
exports/rounds/<run_code>/
exports/pdf/history/<run_code>/eval_rounds_report_<run_code>.pdf

Не клади новые файлы конкретного раунда напрямую в корень imports/ или exports/.

Если пользователь пишет "Новый раунд" и передает zip/rar/7z/набор файлов, сделай следующее.

Шаг 1. Запусти новый раунд

Ответь:
"Запускаю раунд №<номер>"

Номер раунда определи по таблице eval_runs и существующим run_code.

Создай папки:
- imports/rounds/<run_code>/source/
- imports/rounds/<run_code>/extracted/ при необходимости;
- exports/rounds/<run_code>/.

Сохрани оригинальные пользовательские файлы в imports/rounds/<run_code>/source/.
Если распаковываешь архив, результат распаковки положи в imports/rounds/<run_code>/extracted/.

Шаг 2. Проверь комплект файлов

Ожидаются:
1. Файл "Версия агента".
2. Файл/файлы "Декомпозиция_<dataset_code>".
3. Файл/файлы "ТК_<dataset_code>".

Если нет файла версии агента, спроси пользователя:
"Не вижу файл с версией агента. Идем дальше без него? Если да, зафиксирую условные значения и отмечу это в отчете."

Если нет декомпозиции, спроси:
"Не вижу файл с декомпозицией для <dataset_code>/<case_code>. Идем дальше без декомпозиции? Тогда блок декомпозиции не попадет в оценку этого раунда."

Если нет ТК, спроси:
"Не вижу файл с тест-кейсами для <dataset_code>/<case_code>. Идем дальше без ТК? Тогда блок набора ТК и отдельных ТК не попадет в оценку этого раунда."

Не придумывай отсутствующие данные как подтвержденные.

Шаг 3. Разбери файл "Версия агента"

Извлеки и запиши в таблицу eval_runs:
- run_code;
- agent_name;
- agent_version;
- prompt_snapshot;
- model_name;
- model_version;
- temperature;
- top_p;
- run_mode;
- retrieval_chunk_size;
- retrieval_top_k;
- reranker_name;
- response_format_strictness;
- response_contract_json;
- change_summary;
- dataset_version.

Особенно важно:
- промпты;
- top_p;
- temperature;
- отличия от прошлого раунда;
- краткий diff того, что поменялось.

Если явного diff нет, сформируй его сам на основе изменений промпта/модели/настроек.
Если данных нет, используй условные значения только после подтверждения пользователя и явно отметь это в change_summary.

Шаг 4. Разбери декомпозицию

Файлы декомпозиции сопоставляй с dataset_code и case_code.

Сравни результат агента с эталонными requirements.

Используй таблицы:
- requirement_decomposition_evaluation_results;
- requirement_decomposition_quality_assessments;
- requirement_decomposition_quality_criteria;
- requirements;
- input_requirements.

Критерии:
- decomposition_completeness;
- decomposition_boundaries;
- requirement_consolidation.

Для каждого критерия запиши:
- score;
- label;
- rationale;
- assessed_by;
- assessment_method;
- confidence;
- eval_run_id.

Оценки выставляй по методологии scoring-methodology.md.
Обязательно пиши rationale: почему именно такой балл.

Шаг 5. Разбери тест-кейсы

Файлы ТК сопоставляй с dataset_code и case_code.

Используй таблицы:
- test_cases;
- test_case_steps;
- requirement_test_case_links;
- test_case_step_requirement_links;
- test_suite_quality_assessments;
- test_case_quality_assessments;
- test_suite_quality_criteria;
- test_case_quality_criteria.

Оцени набор ТК по критериям:
- positive_coverage;
- negative_coverage;
- suite_cleanliness;
- required_checks_coverage;
- overall_completeness.

Оцени каждый отдельный ТК по критериям:
- classification_correctness;
- template_required_attributes;
- conditions_quality;
- step_atomicity;
- expected_result_quality;
- no_hallucinations.

Для каждой оценки обязательно запиши rationale.
Если связь ТК с требованием эвристическая, отметь это в rationale/review_status.

Шаг 6. Сформируй отчет

После записи в БД запусти:

python scripts/build_pdf_reports.py

Ожидаемые результаты:
- exports/pdf/eval_rounds_report_latest.pdf
- exports/pdf/history/<run_code>/eval_rounds_report_<run_code>.pdf
- exports/pdf/methodology/scoring_methodology.pdf
- exports/rounds/<run_code>/ для служебных round-specific файлов

В latest-отчете таблицы могут показывать накопительную динамику по всем раундам, но выводы под блоками должны объяснять только последний текущий раунд.
Исторический PDF по конкретному run_code должен объяснять только этот run_code.

Вердикт строится по benchmark-правилу:
- первые два раунда сравнивай с предыдущим раундом;
- начиная с третьего раунда сравнивай текущий раунд с лучшей предыдущей версией, то есть TOP benchmark;
- TOP benchmark выбирай по максимальному overall_completeness;
- при равенстве используй suite_cleanliness;
- при новом равенстве используй no_hallucinations по отдельным ТК.

В вердикте обязательно напиши:
- с какой версией сравнивается текущий раунд;
- что улучшилось;
- что ухудшилось;
- общий вывод, к чему привело изменение агента.

В PDF/MD отчете обязательно добавь отдельный блок "TOP benchmark" до основных таблиц. Покажи:
- текущий run_code;
- benchmark run_code;
- режим сравнения;
- значения benchmark по overall_completeness, suite_cleanliness, no_hallucinations;
- краткое правило выбора benchmark.

Шаг 7. Формат ответа пользователю

Ответь кратко:

Раунд №<номер> обработан.

В БД записано:
- версия агента: да/нет;
- декомпозиция: да/нет;
- ТК: да/нет;
- оценки декомпозиции: да/нет;
- оценки набора ТК: да/нет;
- оценки отдельных ТК: да/нет.

Что не попало в отчет:
- перечисли отсутствующие или неподтвержденные данные.

Отчет:
<путь к PDF>

Методология:
<путь к PDF>

Важно:
не ограничивайся средним значением по всем датасетам. Если датасетов несколько, показывай разрез:
1. общий итог;
2. результат по каждому dataset_code;
3. результат по input_profile_code;
4. частные провалы по требованиям/ТК.
```

## SQL-подсказки

Посмотреть существующие раунды:

```sql
SELECT id, dataset_id, run_code, agent_name, agent_version, model_name, model_version,
       temperature, top_p, run_mode, change_summary
FROM eval_runs
ORDER BY dataset_id, run_code;
```

Посмотреть оценки набора ТК:

```sql
SELECT e.run_code, c.code, a.score, a.rationale
FROM test_suite_quality_assessments a
JOIN eval_runs e ON e.id = a.eval_run_id
JOIN test_suite_quality_criteria c ON c.id = a.criterion_id
ORDER BY e.run_code, c.code;
```

Посмотреть средние оценки отдельных ТК:

```sql
SELECT e.run_code, c.code, AVG(a.score) AS avg_score, COUNT(*) AS assessment_count
FROM test_case_quality_assessments a
JOIN eval_runs e ON e.id = a.eval_run_id
JOIN test_case_quality_criteria c ON c.id = a.criterion_id
GROUP BY e.run_code, c.code
ORDER BY e.run_code, c.code;
```

Посмотреть связи ТК с требованиями:

```sql
SELECT tc.test_case_code, tc.title, r.requirement_code, l.coverage_type, l.rationale
FROM requirement_test_case_links l
JOIN test_cases tc ON tc.id = l.test_case_id
JOIN requirements r ON r.id = l.requirement_id
ORDER BY tc.test_case_code, r.requirement_code;
```
