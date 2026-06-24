# Правила формирования отчетов

## Формат выдачи

Основной формат выдачи для демонстрации и согласования - PDF.

Актуальные файлы:

```text
exports/pdf/eval_rounds_report_latest.pdf
exports/pdf/methodology/scoring_methodology.pdf
```

## История по раундам

Для каждого нового eval-раунда формируется отдельный PDF-снимок с нарастающим итогом:

```text
exports/pdf/history/<run_code>/eval_rounds_report_<run_code>.pdf
```

Пример:

```text
exports/pdf/history/v0/eval_rounds_report_v0.pdf
exports/pdf/history/v1/eval_rounds_report_v1.pdf
exports/pdf/history/v2/eval_rounds_report_v2.pdf
```

Исторические PDF не перетираются вручную. Они нужны, чтобы можно было открыть состояние отчета на момент конкретного раунда.

## Методология оценок

Каждый PDF-отчет должен ссылаться на методологию:

```text
exports/pdf/methodology/scoring_methodology.pdf
```

Методология хранится в Markdown как исходник:

```text
Документация/Доки по проекту + критерии/scoring-methodology.md
```

PDF формируется командой:

```bash
python scripts/build_pdf_reports.py
```

## Пояснения к оценкам

В отчете должны быть пояснения под каждым основным блоком:

- декомпозиция требований;
- набор ТК;
- отдельные ТК.

Пояснение должно отвечать на вопрос: почему по каждому критерию выставлен именно такой балл.

