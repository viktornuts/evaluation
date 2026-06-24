# Демо-оценка прогона v1

Источник: `round_v1_output.xlsx`.
Импортировано ТК: 51.

## Оценка набора

| Критерий | Score | Комментарий |
|---|---:|---|
| `positive_coverage` | 9.3 | Позитивные ТК покрывают 26 из 28 эталонных требований MVP. |
| `negative_coverage` | 10.0 | Негативные ТК покрывают 10 из 10 требований, где негативные проверки применимы. |
| `suite_cleanliness` | 3.6 | В наборе 51 ТК; 14 ТК имеют заметный риск неподтвержденных деталей. |
| `required_checks_coverage` | 10.0 | Эвристическая трассировка нашла покрытие 28 из 28 обязательных требований. |
| `overall_completeness` | 7.5 | Итог учитывает позитивное/негативное покрытие, обязательные проверки и чистоту набора. |

## Сгенерированные ТК

| ТК | Вид | Направление | Требования | Средняя оценка | Название |
|---|---|---|---|---:|---|
| `GEN-V1-TC-001` | E2E | positive | REQ-01, REQ-02, REQ-03, REQ-08, REQ-10, REQ-12, REQ-13, REQ-14, REQ-15, REQ-16, REQ-17, REQ-18, REQ-19 | 9.1 | E2E-001 - Привязка тест-плана к релизу в С.Релизы через поле Релиз |
| `GEN-V1-TC-002` | E2E | negative | REQ-07, REQ-09, REQ-10 | 9.2 | E2E-002 - Перевод тест-плана в статус Завершен без указания релиза |
| `GEN-V1-TC-003` | E2E | negative | REQ-05, REQ-08, REQ-10, REQ-17, REQ-20, REQ-21 | 9.2 | E2E-003 - Очистка поля Релиз удаляет связь в С.Релизы |
| `GEN-V1-TC-004` | E2E | negative | REQ-03, REQ-08, REQ-10, REQ-11, REQ-17 | 9.2 | E2E-004 - Дублирование тест-плана не наследует поле Релиз |
| `GEN-V1-TC-005` | E2E | negative | REQ-13 | 9.1 | E2E-005 - Выбор релиза в статусе Завершен недоступен |
| `GEN-V1-TC-006` | E2E | negative | REQ-04, REQ-05, REQ-08, REQ-10 | 9.1 | E2E-006 - Редактирование тест-плана в статусе Завершен недоступно |
| `GEN-V1-TC-007` | E2E | negative | REQ-16, REQ-17, REQ-18, REQ-19, REQ-28, REQ-29 | 9.1 | E2E-007 - Добавление тест-плана вручную в С.Релизы запрещено |
| `GEN-V1-TC-008` | E2E | positive | REQ-04, REQ-06, REQ-08, REQ-10 | 9.1 | E2E-008 - Ролевая модель: Тестировщик может редактировать поле Релиз |
| `GEN-V1-TC-009` | E2E | positive | REQ-16, REQ-17, REQ-18, REQ-19, REQ-26 | 9.1 | E2E-009 - Интеграция в одном контуре inno.local |
| `GEN-V1-TC-010` | E2E | positive | REQ-08, REQ-10, REQ-22, REQ-23, REQ-24, REQ-25 | 9.2 | E2E-010 - Отправка события в Kafka при создании тест-плана с релизом |
| `GEN-V1-TC-011` | UI | positive | REQ-01, REQ-02, REQ-16, REQ-17, REQ-18, REQ-19 | 9.1 | UI-001 - Добавление Релиза в Тест-план при создании |
| `GEN-V1-TC-012` | UI | positive | REQ-13 | 9.1 | UI-002 - Отображение списка релизов только в доступных статусах |
| `GEN-V1-TC-013` | UI | positive | REQ-03, REQ-17 | 9.1 | UI-003 - Отображение поля Релиз в разделе Атрибуты |
| `GEN-V1-TC-014` | UI | positive | REQ-03, REQ-04, REQ-05, REQ-16, REQ-17, REQ-18, REQ-19 | 8.9 | UI-004 - Редактирование поля Релиз в незавершенном Тест-плане |
| `GEN-V1-TC-015` | UI | positive | REQ-03, REQ-08, REQ-10, REQ-17, REQ-20, REQ-21 | 9.1 | UI-005 - Очистка поля Релиз и удаление связи |
| `GEN-V1-TC-016` | UI | negative | REQ-07, REQ-09, REQ-10 | 9.1 | UI-006 - Подтверждение завершения Тест-плана без Релиза |
| `GEN-V1-TC-017` | UI | negative | REQ-07, REQ-09, REQ-10 | 8.7 | UI-007 - Отмена завершения Тест-плана без Релиза |
| `GEN-V1-TC-018` | UI | negative | REQ-08, REQ-10, REQ-11 | 9.1 | UI-008 - Дублирование Тест-плана без наследования Релиза |
| `GEN-V1-TC-019` | UI | negative | REQ-04, REQ-05 | 9.1 | UI-009 - Запрет редактирования поля Релиз в статусе Завершен |
| `GEN-V1-TC-020` | UI | negative | REQ-06 | 8.3 | UI-010 - Запрет редактирования поля Релиз для роли Тестировщик |
| `GEN-V1-TC-021` | UI | negative | REQ-16, REQ-17, REQ-18, REQ-19 | 8.9 | UI-011 - Сообщение об ошибке при неудачном добавлении в релиз |
| `GEN-V1-TC-022` | UI | negative | REQ-08, REQ-10 | 9.1 | UI-012 - Сообщение об ошибке при неудачном удалении из релиза |
| `GEN-V1-TC-023` | UI | positive | REQ-14 | 9.3 | UI-013 - Отображение формата релиза number name |
| `GEN-V1-TC-024` | UI | positive | REQ-03, REQ-16, REQ-17, REQ-18, REQ-19 | 8.9 | UI-014 - Сохранение relationId при добавлении в релиз |
| `GEN-V1-TC-025` | UI | positive | REQ-03, REQ-08, REQ-10, REQ-17, REQ-20, REQ-21 | 8.9 | UI-015 - Очистка relationId при удалении из релиза |
| `GEN-V1-TC-026` | API | positive | REQ-12, REQ-13, REQ-14, REQ-15 | 8.8 | API-001 - Получение списка релизов в статусах Зарегистрирован (REGISTERED), Формирование состава (FORMING), Фиксация состава (FIXATION), ИФТ (IFT), ПСИ/Проверка ХФ (UAT) |
| `GEN-V1-TC-027` | API | positive | REQ-12, REQ-13, REQ-14, REQ-15 | 8.8 | API-002 - Получение списка релизов возвращает пустой массив при отсутствии релизов в доступных статусах |
| `GEN-V1-TC-028` | API | negative | REQ-12, REQ-13, REQ-14, REQ-15 | 8.2 | API-003 - Получение списка релизов возвращает 401 UNAUTHORIZED при отсутствии валидного токена |
| `GEN-V1-TC-029` | API | negative | REQ-12, REQ-13, REQ-14, REQ-15 | 8.8 | API-004 - Получение списка релизов возвращает 400 BAD_REQUEST при некорректном параметре status |
| `GEN-V1-TC-030` | API | positive | REQ-16, REQ-17, REQ-18, REQ-19, REQ-26 | 8.9 | API-005 - Добавление ТП в релиз через POST /api/v0.1/entities с корректным payload |
| `GEN-V1-TC-031` | API | negative | REQ-16, REQ-17, REQ-18, REQ-19 | 8.8 | API-006 - Добавление ТП в релиз возвращает 400 BAD_REQUEST при отсутствии обязательного поля relatedEntities |
| `GEN-V1-TC-032` | API | negative | REQ-16, REQ-17, REQ-18, REQ-19 | 8.8 | API-007 - Добавление ТП в релиз возвращает 400 BAD_REQUEST при некорректном entityNumber в relatedEntities |
| `GEN-V1-TC-033` | API | negative | REQ-16, REQ-17, REQ-18, REQ-19 | 8.2 | API-008 - Добавление ТП в релиз возвращает 403 FORBIDDEN при попытке привязки к релизу в статусе Завершен |
| `GEN-V1-TC-034` | API | positive | REQ-20, REQ-21 | 8.8 | API-009 - Удаление ТП из релиза через DELETE /api/v0.1/entity-relations/{relationId} |
| `GEN-V1-TC-035` | API | negative | REQ-20, REQ-21 | 8.2 | API-010 - Удаление ТП из релиза возвращает 404 NOT_FOUND при несуществующем relationId |
| `GEN-V1-TC-036` | API | negative | REQ-01 | 7.1 | API-011 - Удаление ТП из релиза возвращает 403 FORBIDDEN при недостаточных правах доступа |
| `GEN-V1-TC-037` | API | positive | REQ-04, REQ-05, REQ-07, REQ-09, REQ-10 | 8.8 | API-012 - Создание тест-плана без поля Релиз при переводе в статус Завершен (REGISTERED) |
| `GEN-V1-TC-038` | API | positive | REQ-04, REQ-05 | 8.8 | API-013 - Создание тест-плана с полем Релиз при переводе в статус Завершен (REGISTERED) |
| `GEN-V1-TC-039` | API | positive | REQ-11 | 8.8 | API-014 - Дублирование тест-плана не наследует поле Релиз |
| `GEN-V1-TC-040` | API | positive | REQ-22, REQ-23, REQ-24, REQ-25 | 8.4 | API-015 - Отправка события CREATE TEST_PLAN в Kafka-топик PPTM_OUTGOING_EVENTS_TOPIC |
| `GEN-V1-TC-041` | API | positive | REQ-22, REQ-23, REQ-24, REQ-25 | 8.4 | API-016 - Отправка события UPDATE TEST_PLAN в Kafka-топик PPTM_OUTGOING_EVENTS_TOPIC |
| `GEN-V1-TC-042` | API | positive | REQ-22, REQ-23, REQ-24, REQ-25 | 8.4 | API-017 - Отправка события CREATE TEST_PLAN_CASE в Kafka-топик PPTM_OUTGOING_EVENTS_TOPIC |
| `GEN-V1-TC-043` | API | positive | REQ-22, REQ-23, REQ-24, REQ-25 | 8.4 | API-018 - Отправка события UPDATE TEST_PLAN_CASE в Kafka-топик PPTM_OUTGOING_EVENTS_TOPIC |
| `GEN-V1-TC-044` | API | negative | REQ-16, REQ-17, REQ-18, REQ-19 | 8.2 | API-019 - Добавление ТП в релиз возвращает 401 UNAUTHORIZED при отсутствии валидного токена |
| `GEN-V1-TC-045` | API | negative | REQ-16, REQ-17, REQ-18, REQ-19 | 7.9 | API-020 - Добавление ТП в релиз возвращает 403 FORBIDDEN при попытке привязки к релизу в статусе ИФТ (IFT) |
| `GEN-V1-TC-046` | API | negative | REQ-16, REQ-17, REQ-18, REQ-19 | 7.9 | API-021 - Добавление ТП в релиз возвращает 403 FORBIDDEN при попытке привязки к релизу в статусе ПСИ/Проверка ХФ (UAT) |
| `GEN-V1-TC-047` | API | negative | REQ-01 | 8.2 | API-022 - Удаление ТП из релиза возвращает 401 UNAUTHORIZED при отсутствии валидного токена |
| `GEN-V1-TC-048` | API | negative | REQ-12, REQ-13, REQ-14, REQ-15 | 7.1 | API-023 - Получение списка релизов возвращает 403 FORBIDDEN при недостаточных правах доступа |
| `GEN-V1-TC-049` | API | negative | REQ-12, REQ-13, REQ-14, REQ-15 | 7.8 | API-024 - Получение списка релизов возвращает 500 INTERNAL_SERVER_ERROR при сбое интеграции С.Релизы |
| `GEN-V1-TC-050` | API | negative | REQ-16, REQ-17, REQ-18, REQ-19 | 7.8 | API-025 - Добавление ТП в релиз возвращает 500 INTERNAL_SERVER_ERROR при сбое интеграции С.Релизы |
| `GEN-V1-TC-051` | API | negative | REQ-01 | 7.8 | API-026 - Удаление ТП из релиза возвращает 500 INTERNAL_SERVER_ERROR при сбое интеграции С.Релизы |
