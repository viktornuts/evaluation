# Демо-оценка прогона v5

Источник: `tc-export-b5517cb2.txt`.
Импортировано ТК: 86.
Файл версии агента, промпты и декомпозиция требований не переданы; в `eval_runs` проставлены заглушки `v5`.
Вид и направление ТК определены по меткам экспорта и содержанию шагов.

## Оценка набора

| Критерий | Score | Комментарий |
|---|---:|---|
| `positive_coverage` | 8.2 | Позитивные ТК покрывают 23 из 28 эталонных требований MVP. |
| `negative_coverage` | 3.0 | Негативные ТК покрывают 3 из 10 требований, где негативные проверки применимы. |
| `suite_cleanliness` | 4.0 | В наборе 86 ТК; 1 ТК имеет заметный риск неподтвержденных деталей; размер набора выше 45 ТК создает высокий риск дублей и лишних проверок. |
| `required_checks_coverage` | 8.6 | Эвристическая трассировка нашла покрытие 24 из 28 обязательных требований. |
| `overall_completeness` | 6.2 | Итог учитывает позитивное/негативное покрытие, обязательные проверки и чистоту набора. |

## Сгенерированные ТК

| ТК | Исходный ключ | Вид | Направление | Требования | Средняя оценка | Название |
|---|---|---|---|---|---:|---|
| `GEN-V5-TC-001` | `2a24a693-b32f-4d43-a061-c97273633599` | INT | positive | REQ-22, REQ-23, REQ-24, REQ-25 | 8.6 | Отправка событий в Kafka-топик PPTM_OUTGOING_EVENTS_TOPIC при обновлении Тест-кейса |
| `GEN-V5-TC-002` | `268253ed-65e1-427f-9bb5-da748cc8ec4f` | INT | positive | REQ-22, REQ-23, REQ-24, REQ-25 | 8.6 | Отправка событий в Kafka-топик PPTM_OUTGOING_EVENTS_TOPIC при создании Тест-кейса |
| `GEN-V5-TC-003` | `eda8b3e5-6970-41b5-b37d-b856c58045c6` | INT | positive | REQ-22, REQ-23, REQ-24, REQ-25 | 8.6 | Отправка событий в Kafka-топик PPTM_OUTGOING_EVENTS_TOPIC при обновлении Тест-плана |
| `GEN-V5-TC-004` | `1c0e8ea9-96df-4abe-a562-9dec6f0330da` | INT | positive | REQ-08, REQ-10, REQ-22, REQ-23, REQ-24, REQ-25 | 8.6 | Отправка событий в Kafka-топик PPTM_OUTGOING_EVENTS_TOPIC при создании Тест-плана |
| `GEN-V5-TC-005` | `03816fd0-f8c1-46ff-a505-9277145784d7` | API | positive | REQ-03, REQ-17 | 8.7 | Сохранение атрибута релиза в Тест-плане через POST |
| `GEN-V5-TC-006` | `643e1760-44a7-4c12-b864-30e0c78f9f2f` | API | positive | REQ-01 | 8.7 | Удаление Тест-плана из релиза через DELETE entity-relations/{id} |
| `GEN-V5-TC-007` | `f5e2f3fa-5de0-4a16-9be9-2c1d9e27c64a` | API | positive | REQ-16, REQ-17, REQ-18, REQ-19 | 8.7 | Добавление Тест-плана в релиз через POST /api/v0.1/entities |
| `GEN-V5-TC-008` | `6a74c619-3fb3-4486-bf44-cbe0d2fe47f7` | API | positive | REQ-12, REQ-13, REQ-14, REQ-15 | 8.7 | Получение списка релизов с регулируемым параметром page |
| `GEN-V5-TC-009` | `c58ecd04-d805-4f3f-8f27-b3c02ae79b78` | API | positive | REQ-12, REQ-13, REQ-14, REQ-15 | 8.7 | Получение списка релизов с регулируемым параметром size |
| `GEN-V5-TC-010` | `8796c24f-edcc-4cbc-aac2-e0f30bd52e85` | API | positive | REQ-12, REQ-13, REQ-14, REQ-15 | 8.7 | Получение списка релизов в статусах Формирование состава (FORMING), Фиксация состава (FIXATION), ИФТ (IFT), ПСИ/Проверка ХФ (UAT) |
| `GEN-V5-TC-011` | `6c84aeae-cb94-40c1-97bf-b173997fb584` | API | positive | REQ-12, REQ-13, REQ-14, REQ-15 | 8.7 | Получение списка релизов в статусе Зарегистрирован (REGISTERED) |
| `GEN-V5-TC-012` | `5c375f55-88f1-454d-ad1a-f6165ffd5a52` | INT | positive | REQ-22, REQ-23, REQ-24, REQ-25 | 8.6 | Отправка событий в Kafka-топик при обновлении Тест-кейса |
| `GEN-V5-TC-013` | `24002138-7d4d-4680-8414-e2c3601fc38d` | INT | positive | REQ-22, REQ-23, REQ-24, REQ-25 | 8.6 | Отправка событий в Kafka-топик при создании Тест-кейса |
| `GEN-V5-TC-014` | `e07fd2bf-2b27-4dd0-87e4-5f9783eb58a9` | INT | positive | REQ-22, REQ-23, REQ-24, REQ-25 | 8.6 | Отправка событий в Kafka-топик при обновлении Тест-плана |
| `GEN-V5-TC-015` | `1c35cfe6-ed2d-4eb4-bfee-6340c5caa06f` | INT | positive | REQ-08, REQ-10, REQ-22, REQ-23, REQ-24, REQ-25 | 8.6 | Отправка событий в Kafka-топик при создании Тест-плана |
| `GEN-V5-TC-016` | `97e0c81c-0258-4c7f-adfe-0aceba3d4854` | API | positive | REQ-21 | 8.7 | Удаление Тест-плана из релиза через DELETE entity-relations/{id} |
| `GEN-V5-TC-017` | `377500f0-6f15-4b4c-b48c-1c0b48863f9f` | API | positive | REQ-14, REQ-16, REQ-17, REQ-18, REQ-19 | 8.7 | Добавление Тест-плана в релиз через POST /api/v0.1/entities |
| `GEN-V5-TC-018` | `e593b14f-b754-4424-b133-43da4843f7e0` | API | positive | REQ-12, REQ-13, REQ-14, REQ-15 | 8.7 | Получение списка релизов с регулируемым параметром size |
| `GEN-V5-TC-019` | `db6569e3-dbec-42be-a7cc-67b6eddb81ef` | API | positive | REQ-12, REQ-13, REQ-14, REQ-15 | 8.7 | Получение списка релизов в разрешенных статусах |
| `GEN-V5-TC-020` | `124dff3a-f664-47a7-b7d6-58cde755afbd` | INT | positive | REQ-16, REQ-17, REQ-18, REQ-19, REQ-22, REQ-23, REQ-24, REQ-25 | 8.3 | Отправка событий в Kafka-топик PPTM_OUTGOING_EVENTS_TOPIC при обновлении случая ТП |
| `GEN-V5-TC-021` | `e9f31e9a-c30b-42e0-be20-020a794f29da` | INT | positive | REQ-16, REQ-17, REQ-18, REQ-19, REQ-22, REQ-23, REQ-24, REQ-25 | 8.3 | Отправка событий в Kafka-топик PPTM_OUTGOING_EVENTS_TOPIC при создании случая ТП |
| `GEN-V5-TC-022` | `2b49a3a3-fa1d-42f2-9d84-0484338c04e5` | INT | positive | REQ-16, REQ-17, REQ-18, REQ-19, REQ-22, REQ-23, REQ-24, REQ-25 | 8.3 | Отправка событий в Kafka-топик PPTM_OUTGOING_EVENTS_TOPIC при обновлении ТП |
| `GEN-V5-TC-023` | `6d1f23fd-e21a-4a1f-af3f-6035f800d053` | INT | positive | REQ-08, REQ-10, REQ-16, REQ-17, REQ-18, REQ-19, REQ-22, REQ-23, REQ-24, REQ-25 | 8.3 | Отправка событий в Kafka-топик PPTM_OUTGOING_EVENTS_TOPIC при создании ТП |
| `GEN-V5-TC-024` | `4bbe2a8e-ea48-4b59-83cd-d65fc68e9826` | API | positive | REQ-01 | 8.7 | Удаление Тест-плана из релиза через DELETE entity-relations/{id} |
| `GEN-V5-TC-025` | `4c52c6b3-bb7f-498d-bb6b-412e18717481` | API | positive | REQ-16, REQ-17, REQ-18, REQ-19 | 8.7 | Добавление Тест-плана в релиз через POST /api/v0.1/entities |
| `GEN-V5-TC-026` | `5e709f3f-cb5d-4c6b-a68b-16fa5039a05a` | API | positive | REQ-12, REQ-13, REQ-14, REQ-15 | 8.5 | Получение списка релизов с регулируемым параметром page |
| `GEN-V5-TC-027` | `8cb3edcc-4274-4e69-a65f-9967ff9cb977` | API | positive | REQ-12, REQ-13, REQ-14, REQ-15 | 8.5 | Получение списка релизов с регулируемым параметром size |
| `GEN-V5-TC-028` | `cacc7ed3-e05a-4554-8105-03fb6d5bd554` | API | positive | REQ-12, REQ-13, REQ-14, REQ-15 | 8.7 | Получение списка релизов в статусах REGISTERED, FORMING, FIXATION, IFT, UAT |
| `GEN-V5-TC-029` | `57366285-056e-4fb2-b637-0f7e84b9a367` | INT | positive | REQ-22, REQ-23, REQ-24, REQ-25 | 8.6 | Отправка событий в Kafka-топик PPTM_OUTGOING_EVENTS_TOPIC при обновлении случая ТП |
| `GEN-V5-TC-030` | `57417302-a56e-406f-b3b5-e633c6cb869b` | INT | positive | REQ-22, REQ-23, REQ-24, REQ-25 | 8.6 | Отправка событий в Kafka-топик PPTM_OUTGOING_EVENTS_TOPIC при создании случая ТП |
| `GEN-V5-TC-031` | `cea8881d-8a03-4cee-8250-295c06f8a879` | INT | positive | REQ-22, REQ-23, REQ-24, REQ-25 | 8.6 | Отправка событий в Kafka-топик PPTM_OUTGOING_EVENTS_TOPIC при обновлении ТП |
| `GEN-V5-TC-032` | `1e8703ce-c58d-45cf-99c5-8fcb4fd7637e` | INT | positive | REQ-08, REQ-10, REQ-22, REQ-23, REQ-24, REQ-25 | 8.6 | Отправка событий в Kafka-топик PPTM_OUTGOING_EVENTS_TOPIC при создании ТП |
| `GEN-V5-TC-033` | `87fd6a8d-4373-4c1a-8f11-d9248d6b27bd` | API | positive | REQ-21 | 8.7 | Удаление Тест-плана из релиза через DELETE entity-relations/{id} |
| `GEN-V5-TC-034` | `1f71bba0-d4ce-45e9-aa6e-19ae3eadc3a4` | API | positive | REQ-16, REQ-17, REQ-18, REQ-19 | 8.7 | Добавление Тест-плана в релиз через POST /api/v0.1/entities |
| `GEN-V5-TC-035` | `8daefb71-4659-45d2-b31a-8b0fd8678579` | API | positive | REQ-12, REQ-13, REQ-14, REQ-15 | 8.7 | Получение списка релизов с регулируемым параметром page |
| `GEN-V5-TC-036` | `0ef95814-9b11-43f7-ad2f-2c272425101a` | API | positive | REQ-12, REQ-13, REQ-14, REQ-15 | 8.7 | Получение списка релизов с регулируемым параметром size |
| `GEN-V5-TC-037` | `51e229a8-c585-4a43-9d34-bc7ef5447d5e` | API | positive | REQ-12, REQ-13, REQ-14, REQ-15 | 8.7 | Получение списка релизов в статусах REGISTERED, FORMING, FIXATION, IFT, UAT |
| `GEN-V5-TC-038` | `3d855645-d576-4d11-aa37-ba5180c5be5d` | INT | positive | REQ-22, REQ-23, REQ-24, REQ-25 | 8.6 | Событие UPDATE TEST_PLAN_CASE в Kafka-топик PPTM_OUTGOING_EVENTS_TOPIC |
| `GEN-V5-TC-039` | `d44a3be5-3b09-4408-8138-09b2f0ed8748` | INT | positive | REQ-22, REQ-23, REQ-24, REQ-25 | 8.6 | Событие CREATE TEST_PLAN_CASE в Kafka-топик PPTM_OUTGOING_EVENTS_TOPIC |
| `GEN-V5-TC-040` | `e85e2205-9e5c-463a-bfd7-9d9e1d5b206d` | INT | positive | REQ-22, REQ-23, REQ-24, REQ-25 | 8.6 | Событие UPDATE TEST_PLAN в Kafka-топик PPTM_OUTGOING_EVENTS_TOPIC |
| `GEN-V5-TC-041` | `f17847a2-9e62-46cc-b5d9-9a1a143ddcbe` | INT | positive | REQ-08, REQ-10, REQ-22, REQ-23, REQ-24, REQ-25 | 8.6 | Событие CREATE TEST_PLAN в Kafka-топик PPTM_OUTGOING_EVENTS_TOPIC |
| `GEN-V5-TC-042` | `09af2759-2d4c-4a26-9b23-a1c77dbb2df8` | API | positive | REQ-03, REQ-17 | 8.7 | Сохранение атрибута релиза в ТП через POST |
| `GEN-V5-TC-043` | `3b169e36-8dce-49cf-b9de-f1bba6f1a073` | API | positive | REQ-21 | 8.7 | Удаление Тест-плана из релиза через DELETE entity-relations/{id} |
| `GEN-V5-TC-044` | `f53d8d3d-6093-4525-b672-0f7aa05a5694` | API | positive | REQ-16, REQ-17, REQ-18, REQ-19 | 8.7 | Добавление Тест-плана в релиз через POST /api/v0.1/entities |
| `GEN-V5-TC-045` | `1295ab6b-5921-4852-955b-72d11489bcf4` | API | positive | REQ-12, REQ-13, REQ-14, REQ-15 | 8.7 | Получение списка релизов с регулируемым параметром page |
| `GEN-V5-TC-046` | `892834e4-92b6-4425-9146-c63ee30e3d01` | API | positive | REQ-12, REQ-13, REQ-14, REQ-15 | 8.7 | Получение списка релизов с регулируемым параметром size |
| `GEN-V5-TC-047` | `cfa6c241-b9b3-418e-b5c3-cf369f73c757` | API | positive | REQ-12, REQ-13, REQ-14, REQ-15 | 8.7 | Получение списка релизов в статусах Формирование состава, Фиксация состава, ИФТ, ПСИ/Проверка ХФ |
| `GEN-V5-TC-048` | `8bf55c68-1c3c-49d8-869e-add9a5943b07` | API | positive | REQ-12, REQ-13, REQ-14, REQ-15 | 8.7 | Получение списка релизов в разрешенных статусах |
| `GEN-V5-TC-049` | `d71fe10b-5fd7-4271-ad7c-d2b797ee3700` | INT | positive | REQ-22, REQ-23, REQ-24, REQ-25 | 8.6 | Отправка событий UPDATE TEST_PLAN_CASE в Kafka при изменении поля Релиз |
| `GEN-V5-TC-050` | `0c980909-a6f1-4cc6-9fc3-a5ac513fd84b` | INT | positive | REQ-08, REQ-10, REQ-22, REQ-23, REQ-24, REQ-25 | 8.6 | Отправка событий CREATE TEST_PLAN_CASE в Kafka при заполнении поля Релиз |
| `GEN-V5-TC-051` | `d60cb4fe-00e6-4581-91a9-7f8fe8316358` | INT | positive | REQ-22, REQ-23, REQ-24, REQ-25 | 8.6 | Отправка событий UPDATE TEST_PLAN в Kafka при изменении поля Релиз |
| `GEN-V5-TC-052` | `d358daf6-374e-4186-9738-5f78af454e84` | INT | positive | REQ-08, REQ-10, REQ-22, REQ-23, REQ-24, REQ-25 | 8.6 | Отправка событий CREATE TEST_PLAN в Kafka при заполнении поля Релиз |
| `GEN-V5-TC-053` | `118e670c-592f-4ae9-a580-6b0f752b0ad9` | API | positive | REQ-21 | 8.7 | Удаление Тест-плана из релиза через DELETE entity-relations/{id} |
| `GEN-V5-TC-054` | `81e815f2-fb18-498d-8ac2-a9bd8456963e` | API | positive | REQ-03, REQ-17 | 8.7 | Сохранение атрибута релиза в ТП возвращает 200 OK |
| `GEN-V5-TC-055` | `0b28d1b6-947a-4c91-ad27-589bb44c7e23` | API | positive | REQ-16, REQ-17, REQ-18, REQ-19 | 8.7 | Добавление Тест-плана в релиз через POST /api/v0.1/entities |
| `GEN-V5-TC-056` | `8ec4dbc5-d84d-464e-90cf-9f404a8d8c5c` | API | positive | REQ-12, REQ-13, REQ-14, REQ-15 | 8.5 | Получение списка релизов с регулируемым параметром page |
| `GEN-V5-TC-057` | `ca7de337-6d8d-4fda-b6a1-2273425296fd` | API | positive | REQ-12, REQ-13, REQ-14, REQ-15 | 8.5 | Получение списка релизов с регулируемым параметром size |
| `GEN-V5-TC-058` | `682f67a3-999c-4d9c-9e75-e8ffde2a9f5c` | API | positive | REQ-12, REQ-13, REQ-14, REQ-15 | 8.7 | Получение списка релизов в доступных статусах |
| `GEN-V5-TC-059` | `8901f39c-7a64-4c80-831e-5352f78f30ec` | INT | positive | REQ-16, REQ-17, REQ-18, REQ-19, REQ-22, REQ-23, REQ-24, REQ-25 | 8.3 | Отправка событий в Kafka-топик PPTM_OUTGOING_EVENTS_TOPIC при обновлении Тест-кейса |
| `GEN-V5-TC-060` | `7ece1f1c-f9f3-4c49-9b0a-3b831259de37` | INT | positive | REQ-16, REQ-17, REQ-18, REQ-19, REQ-22, REQ-23, REQ-24, REQ-25 | 8.3 | Отправка событий в Kafka-топик PPTM_OUTGOING_EVENTS_TOPIC при создании Тест-кейса |
| `GEN-V5-TC-061` | `2ccdb841-44da-42c9-bd0c-bcffb047bfd5` | INT | positive | REQ-16, REQ-17, REQ-18, REQ-19, REQ-22, REQ-23, REQ-24, REQ-25 | 8.3 | Отправка событий в Kafka-топик PPTM_OUTGOING_EVENTS_TOPIC при обновлении Тест-плана |
| `GEN-V5-TC-062` | `3faecaa4-056d-456c-87ce-01f7f3ed3289` | INT | positive | REQ-16, REQ-17, REQ-18, REQ-19, REQ-22, REQ-23, REQ-24, REQ-25 | 8.3 | Отправка событий в Kafka-топик PPTM_OUTGOING_EVENTS_TOPIC при создании Тест-плана |
| `GEN-V5-TC-063` | `e799dcfe-c34d-4d20-8471-1c412eb7f1b7` | API | positive | REQ-21 | 8.7 | Удаление Тест-плана из релиза через DELETE entity-relations/{id} |
| `GEN-V5-TC-064` | `36109008-4a78-444c-8aeb-5fb3e6ea8a98` | API | positive | REQ-16, REQ-17, REQ-18, REQ-19 | 8.7 | Добавление Тест-плана в релиз через POST /api/v0.1/entities |
| `GEN-V5-TC-065` | `f5627eef-c60c-4989-96f6-93bd5c70da85` | API | positive | REQ-12, REQ-13, REQ-14, REQ-15 | 8.7 | Получение списка релизов с регулируемым параметром page |
| `GEN-V5-TC-066` | `f742432d-d0e2-493f-b6ca-923152d2db1a` | API | positive | REQ-12, REQ-13, REQ-14, REQ-15 | 8.7 | Получение списка релизов с регулируемым параметром size |
| `GEN-V5-TC-067` | `2f3eff55-1f0b-49c9-83db-63a44be055e5` | API | positive | REQ-12, REQ-13, REQ-14, REQ-15 | 8.7 | Получение списка релизов в статусах Формирование состава (FORMING), Фиксация состава (FIXATION), ИФТ (IFT), ПСИ/Проверка ХФ (UAT) |
| `GEN-V5-TC-068` | `080fe009-362e-4e30-980f-539e01a9a161` | API | positive | REQ-12, REQ-13, REQ-14, REQ-15 | 8.7 | Получение списка релизов в статусе Зарегистрирован (REGISTERED) |
| `GEN-V5-TC-069` | `14cfffb9-2f69-488f-bb40-54d342e6b522` | UI | positive | REQ-05, REQ-08, REQ-10 | 8.7 | Очистка поля Релиз при редактировании |
| `GEN-V5-TC-070` | `66215de1-3623-461c-b2d0-5e7211ce1285` | UI | negative | REQ-08, REQ-10, REQ-11 | 8.9 | Дублирование тест-плана без наследования поля Релиз |
| `GEN-V5-TC-071` | `2f9026c3-04e3-44c1-b1e2-5e098df75aae` | UI | negative | REQ-07, REQ-09, REQ-10 | 8.2 | Отмена завершения тест-плана без заполнения поля Релиз |
| `GEN-V5-TC-072` | `59f6c3ca-4c63-4965-871f-b3c33ba14c01` | UI | positive | REQ-07, REQ-09, REQ-10 | 8.7 | Завершение тест-плана без заполнения поля Релиз с подтверждением |
| `GEN-V5-TC-073` | `400f6bd5-3b65-4069-9c41-2bba55a9692c` | UI | positive | REQ-08, REQ-10 | 8.9 | Завершение тест-плана с заполненным полем Релиз |
| `GEN-V5-TC-074` | `c29deb51-77a3-40a5-b19d-4c8f328906fb` | UI | positive | REQ-06, REQ-13, REQ-16, REQ-17, REQ-18, REQ-19 | 8.7 | Редактирование поля Релиз пользователем с ролью Тестировщик |
| `GEN-V5-TC-075` | `114ba5ac-e67a-46f7-b03b-01435e7a7139` | UI | positive | REQ-04, REQ-05, REQ-13, REQ-16, REQ-17, REQ-18, REQ-19 | 8.7 | Редактирование поля Релиз в статусах отличных от Завершен |
| `GEN-V5-TC-076` | `37a64181-895c-4d65-98d1-ffccbee01001` | UI | positive | REQ-03, REQ-17 | 8.9 | Открытие страницы тест-плана с разделом Атрибуты |
| `GEN-V5-TC-077` | `f4e3c1c0-d2c2-43c8-b3ce-1c8eeb008173` | UI | positive | REQ-01, REQ-02 | 8.9 | Открытие формы создания тест-плана с полем Релиз |
| `GEN-V5-TC-078` | `46974815-1da3-4c8f-960e-6d5bceeedf6a` | INT | positive | REQ-22, REQ-23, REQ-24, REQ-25 | 8.6 | События UPDATE TEST_PLAN_CASE в Kafka-топик PPTM_OUTGOING_EVENTS_TOPIC |
| `GEN-V5-TC-079` | `6b416a4e-5706-430c-a310-3f226699a33d` | INT | positive | REQ-22, REQ-23, REQ-24, REQ-25 | 8.6 | События CREATE TEST_PLAN_CASE в Kafka-топик PPTM_OUTGOING_EVENTS_TOPIC |
| `GEN-V5-TC-080` | `673fc3ec-7e72-49da-8083-08cf2ab91552` | INT | positive | REQ-22, REQ-23, REQ-24, REQ-25 | 8.6 | События UPDATE TEST_PLAN в Kafka-топик PPTM_OUTGOING_EVENTS_TOPIC |
| `GEN-V5-TC-081` | `6bad31eb-ff4f-4ef8-91bf-60c648fbb8d6` | INT | positive | REQ-08, REQ-10, REQ-22, REQ-23, REQ-24, REQ-25 | 8.6 | События CREATE TEST_PLAN в Kafka-топик PPTM_OUTGOING_EVENTS_TOPIC |
| `GEN-V5-TC-082` | `419bef75-a3f3-4d33-bff0-c3f675031ba7` | API | positive | REQ-01 | 8.7 | Удаление Тест-плана из релиза через DELETE entity-relations/{id} |
| `GEN-V5-TC-083` | `00e1325d-9d52-4379-800a-0dac6ec1eadb` | API | positive | REQ-16, REQ-17, REQ-18, REQ-19 | 8.7 | Добавление Тест-плана в релиз через POST /api/v0.1/entities |
| `GEN-V5-TC-084` | `d87130f1-d77e-4b62-82ee-ea1941413242` | API | positive | REQ-12, REQ-13, REQ-14, REQ-15 | 8.5 | Получение списка релизов с регулируемым параметром page |
| `GEN-V5-TC-085` | `9e146e2a-7b3d-49b6-a684-f4b0ea3a8114` | API | positive | REQ-12, REQ-13, REQ-14, REQ-15 | 8.5 | Получение списка релизов с регулируемым параметром size |
| `GEN-V5-TC-086` | `df3ec11e-f5f0-49cd-bdf9-6e966e0e0e2b` | API | positive | REQ-12, REQ-13, REQ-14, REQ-15 | 8.7 | Получение списка релизов в разрешенных статусах |
