# Демо-оценка прогона v2

Источник: `round_v2_output.xlsx`.
Импортировано ТК: 35.

## Оценка набора

| Критерий | Score | Комментарий |
|---|---:|---|
| `positive_coverage` | 8.2 | Позитивные ТК покрывают 23 из 28 эталонных требований MVP. |
| `negative_coverage` | 9.0 | Негативные ТК покрывают 9 из 10 требований, где негативные проверки применимы. |
| `suite_cleanliness` | 7.0 | В наборе 35 ТК; 2 ТК имеют заметный риск неподтвержденных деталей. |
| `required_checks_coverage` | 9.6 | Эвристическая трассировка нашла покрытие 27 из 28 обязательных требований. |
| `overall_completeness` | 8.5 | Итог учитывает позитивное/негативное покрытие, обязательные проверки и чистоту набора. |

## Сгенерированные ТК

| ТК | Вид | Направление | Требования | Средняя оценка | Название |
|---|---|---|---|---:|---|
| `GEN-V2-TC-001` | UI | positive | REQ-01, REQ-02, REQ-08, REQ-10, REQ-16, REQ-17, REQ-18, REQ-19 | 9.1 | UI-001 - Привязка релиза к Тест-плану на этапе создания |
| `GEN-V2-TC-002` | UI | positive | REQ-14 | 9.3 | UI-002 - Формат отображения релиза «номер наименование» |
| `GEN-V2-TC-003` | UI | positive | REQ-03, REQ-17 | 9.1 | UI-003 - Вывод поля Релиз в блоке Атрибуты |
| `GEN-V2-TC-004` | UI | negative | REQ-07, REQ-09, REQ-10 | 9.3 | UI-004 - Запрос подтверждения при завершении Тест-плана без релиза |
| `GEN-V2-TC-005` | E2E | positive | REQ-22, REQ-23, REQ-24, REQ-25 | 9.2 | E2E-001 - Публикация события в Kafka при создании тест-плана с релизом |
| `GEN-V2-TC-006` | API | positive | REQ-08, REQ-10, REQ-11 | 8.8 | API-001 - Дубль тест-плана не копирует поле Релиз |
| `GEN-V2-TC-007` | E2E | negative | REQ-07, REQ-08, REQ-09, REQ-10 | 9.2 | E2E-002 - Завершение тест-плана без привязки релиза |
| `GEN-V2-TC-008` | API | positive | REQ-20, REQ-21 | 8.8 | API-002 - Отвязка ТП от релиза через DELETE /api/v0.1/entity-relations/{relationId} |
| `GEN-V2-TC-009` | API | positive | REQ-16, REQ-17, REQ-18, REQ-19, REQ-26 | 8.9 | API-003 - Привязка ТП к релизу через POST /api/v0.1/entities с валидным payload |
| `GEN-V2-TC-010` | E2E | negative | REQ-13 | 9.1 | E2E-003 - Релиз в статусе Завершен отсутствует среди доступных для выбора |
| `GEN-V2-TC-011` | E2E | negative | REQ-04, REQ-06, REQ-08, REQ-10 | 8.1 | E2E-004 - Ролевая модель: роль Тестировщик лишена прав на редактирование поля Релиз |
| `GEN-V2-TC-012` | UI | negative | REQ-16, REQ-17, REQ-18, REQ-19 | 8.9 | UI-005 - Вывод ошибки при сбое добавления в релиз |
| `GEN-V2-TC-013` | UI | positive | REQ-13 | 9.1 | UI-006 - Перечень релизов ограничен только доступными статусами |
| `GEN-V2-TC-014` | API | positive | REQ-12, REQ-13, REQ-14, REQ-15 | 8.8 | API-004 - Получение релизов в статусах Зарегистрирован (REGISTERED), Формирование состава (FORMING), Фиксация состава (FIXATION), ИФТ (IFT), ПСИ/Проверка ХФ (UAT) |
| `GEN-V2-TC-015` | E2E | positive | REQ-01, REQ-02, REQ-03, REQ-08, REQ-10, REQ-12, REQ-13, REQ-14, REQ-15, REQ-16, REQ-17, REQ-18, REQ-19 | 9.1 | E2E-005 - Связывание тест-плана с релизом в С.Релизы посредством поля Релиз |
| `GEN-V2-TC-016` | UI | negative | REQ-07, REQ-09, REQ-10 | 8.7 | UI-007 - Отказ от завершения Тест-плана без релиза |
| `GEN-V2-TC-017` | UI | positive | REQ-03, REQ-16, REQ-17, REQ-18, REQ-19 | 8.9 | UI-008 - Фиксация relationId при добавлении в релиз |
| `GEN-V2-TC-018` | UI | positive | REQ-03, REQ-16, REQ-17, REQ-18, REQ-19 | 8.9 | UI-009 - Правка поля Релиз в незавершённом Тест-плане |
| `GEN-V2-TC-019` | E2E | negative | REQ-08, REQ-10 | 9.1 | E2E-006 - Недоступность правки тест-плана в статусе Завершен |
| `GEN-V2-TC-020` | API | positive | REQ-22, REQ-23, REQ-24, REQ-25 | 8.4 | API-005 - Публикация события CREATE TEST_PLAN_CASE в Kafka-топик PPTM_OUTGOING_EVENTS_TOPIC |
| `GEN-V2-TC-021` | API | positive | REQ-07, REQ-09, REQ-10 | 8.8 | API-006 - Завершение тест-плана без поля Релиз из статуса Зарегистрирован (REGISTERED) |
| `GEN-V2-TC-022` | API | positive | REQ-22, REQ-23, REQ-24, REQ-25 | 8.4 | API-007 - Публикация события CREATE TEST_PLAN в Kafka-топик PPTM_OUTGOING_EVENTS_TOPIC |
| `GEN-V2-TC-023` | UI | negative | REQ-01 | 9.3 | UI-010 - Поле Релиз закрыто для правки под ролью Тестировщик |
| `GEN-V2-TC-024` | E2E | negative | REQ-08, REQ-10, REQ-17, REQ-20, REQ-21 | 9.2 | E2E-007 - Очистка поля Релиз снимает связь в С.Релизы |
| `GEN-V2-TC-025` | API | positive | REQ-22, REQ-23, REQ-24, REQ-25 | 8.4 | API-008 - Публикация события UPDATE TEST_PLAN в Kafka-топик PPTM_OUTGOING_EVENTS_TOPIC |
| `GEN-V2-TC-026` | UI | positive | REQ-03, REQ-08, REQ-10, REQ-17, REQ-20, REQ-21 | 9.1 | UI-011 - Очистка поля Релиз с разрывом связи |
| `GEN-V2-TC-027` | E2E | negative | REQ-16, REQ-17, REQ-18, REQ-19, REQ-28, REQ-29 | 9.1 | E2E-008 - Ручное добавление тест-плана в С.Релизы недопустимо |
| `GEN-V2-TC-028` | UI | negative | REQ-08, REQ-10, REQ-11 | 9.1 | UI-012 - Копия Тест-плана не наследует поле Релиз |
| `GEN-V2-TC-029` | UI | negative | REQ-08, REQ-10 | 9.1 | UI-013 - Вывод ошибки при сбое удаления из релиза |
| `GEN-V2-TC-030` | UI | negative | REQ-01 | 9.1 | UI-014 - Блокировка правки поля Релиз в статусе Завершен |
| `GEN-V2-TC-031` | API | positive | REQ-22, REQ-23, REQ-24, REQ-25 | 8.4 | API-009 - Публикация события UPDATE TEST_PLAN_CASE в Kafka-топик PPTM_OUTGOING_EVENTS_TOPIC |
| `GEN-V2-TC-032` | E2E | negative | REQ-03, REQ-08, REQ-10, REQ-11, REQ-17 | 9.2 | E2E-009 - Копия тест-плана не переносит поле Релиз |
| `GEN-V2-TC-033` | UI | positive | REQ-03, REQ-08, REQ-10, REQ-17, REQ-20, REQ-21 | 8.9 | UI-015 - Сброс relationId при удалении из релиза |
| `GEN-V2-TC-034` | E2E | positive | REQ-16, REQ-17, REQ-18, REQ-19, REQ-26 | 9.1 | E2E-010 - Интеграция в пределах одного контура inno.local |
| `GEN-V2-TC-035` | API | positive | REQ-01 | 8.8 | API-010 - Завершение тест-плана с полем Релиз из статуса Зарегистрирован (REGISTERED) |
