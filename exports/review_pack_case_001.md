# External Review Pack: CASE-001 - Password recovery requirements

## Task

Review the existing requirement quality assessments. Do not overwrite them.
Point out where you disagree, what score/label you would assign, and why.

Return a structured JSON object matching `expected_external_review_shape` from the companion JSON file.

## Dataset Case

- Dataset: `cpt_smoke` `v1`
- Case ID: `case_password_recovery`
- Case code: `CASE-001`
- Title: Password recovery requirements
- Description: Example case with one complete requirement and one intentionally incomplete requirement.

## Source Fragments

### `frag_password_recovery_email` - FR-1

- Source: Документы / Password recovery specification

Пользователь должен иметь возможность восстановить пароль по email. Система отправляет ссылку восстановления на подтвержденный email.

### `frag_fast_processing` - FR-2

- Source: Документы / Password recovery specification

Система должна быстро обрабатывать заявки.

## Requirements And Project Assessments

### `req_password_recovery_email` / REQ-001

Пользователь должен иметь возможность восстановить пароль по email, получив ссылку восстановления на подтвержденный email.

- Expected status: `ready_for_generation`
- Quality profile: `good_input`
- Risk level: `low`

Assessments:

- `ambiguity`: score `5`, label `unambiguous`
  - assessment_id: `rqa_req001_ambiguity`
  - rationale: Трактовка требования однозначна.
- `completeness`: score `5`, label `complete`
  - assessment_id: `rqa_req001_completeness`
  - rationale: Есть субъект, действие, канал и ожидаемый результат.
- `consistency`: score `5`, label `consistent`
  - assessment_id: `rqa_req001_consistency`
  - rationale: Противоречий не обнаружено.
- `correctness`: score `5`, label `correct`
  - assessment_id: `rqa_req001_correctness`
  - rationale: Формулировка соответствует типичному сценарию восстановления пароля.
- `source_quality`: score `5`, label `primary_source`
  - assessment_id: `rqa_req001_source_quality`
  - rationale: Требование взято из явного фрагмента спецификации.
- `testability`: score `5`, label `testable`
  - assessment_id: `rqa_req001_testability`
  - rationale: Можно проверить отправку ссылки на подтвержденный email.
- `traceability`: score `5`, label `traceable`
  - assessment_id: `rqa_req001_traceability`
  - rationale: Есть связь с конкретным фрагментом FR-1.

### `req_fast_processing` / REQ-002

Система должна быстро обрабатывать заявки.

- Expected status: `insufficient_detail`
- Quality profile: `poor_input`
- Risk level: `high`

Assessments:

- `ambiguity`: score `1`, label `ambiguous`
  - assessment_id: `rqa_req002_ambiguity`
  - rationale: Слово 'быстро' допускает разные трактовки.
- `completeness`: score `1`, label `incomplete`
  - assessment_id: `rqa_req002_completeness`
  - rationale: Не указан тип заявок, объем, SLA или ожидаемый порог скорости.
- `consistency`: score `3`, label `unknown`
  - assessment_id: `rqa_req002_consistency`
  - rationale: Противоречий нет, но контекста недостаточно.
- `correctness`: score `3`, label `unknown`
  - assessment_id: `rqa_req002_correctness`
  - rationale: Корректность нельзя подтвердить без бизнес-контекста.
- `source_quality`: score `5`, label `primary_source`
  - assessment_id: `rqa_req002_source_quality`
  - rationale: Требование взято из явного фрагмента спецификации.
- `testability`: score `1`, label `not_testable`
  - assessment_id: `rqa_req002_testability`
  - rationale: Нет измеримого ожидаемого результата.
- `traceability`: score `5`, label `traceable`
  - assessment_id: `rqa_req002_traceability`
  - rationale: Есть связь с конкретным фрагментом FR-2.

## Expected Test Cases

### `tc_password_recovery_positive` / TC-001

- Title: Successful password recovery by confirmed email
- Type: `WEB`
- Direction: `positive`

Requirement links:

- `req_password_recovery_email` / REQ-001: ТК проверяет успешное восстановление пароля по подтвержденному email.

Steps:

1. Action: Инициировать восстановление пароля для подтвержденного email.
   Expected result: Система принимает запрос на восстановление пароля.
2. Action: Проверить получение ссылки восстановления на подтвержденный email.
   Expected result: На подтвержденный email отправлена ссылка восстановления пароля.
