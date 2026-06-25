INSERT OR IGNORE INTO dataset_input_profiles (code, name, description, expected_behavior)
VALUES
    (
        'customer_gold_requirements',
        'Эталонные требования заказчика',
        'Полный эталонный датасет заказчика: требования и эталонные тест-кейсы считаются целевым результатом.',
        'Агент должен максимально воспроизвести эталонную декомпозицию и покрытие без лишних сценариев и галлюцинаций.'
    ),
    (
        'complete_technical_docs',
        'Полная техническая документация',
        'Вход содержит достаточные технические требования, ограничения и ожидаемое поведение.',
        'Ожидается полное покрытие требований и обязательных проверок.'
    ),
    (
        'incomplete_fragmented_docs',
        'Неполная или фрагментированная документация',
        'Вход содержит неполные требования, пропуски, фрагменты или недостаточный контекст.',
        'Ожидается безопасное частичное покрытие: агент покрывает только выводимое из источников и явно фиксирует пробелы без додумывания.'
    ),
    (
        'business_user_story_docs',
        'Бизнес-документация / user story',
        'Вход описывает бизнес-ожидание без полной технической детализации.',
        'Ожидается корректное извлечение проверяемых сценариев с осторожной детализацией и без выдуманных технических условий.'
    ),
    (
        'conflicting_noisy_docs',
        'Шумная или противоречивая документация',
        'Вход содержит дубли, противоречия, нерелевантные фрагменты или шум.',
        'Ожидается фильтрация шума, явное сохранение спорных мест и отсутствие ложной консолидации противоречий.'
    ),
    (
        'abstract_high_level_docs',
        'Абстрактная верхнеуровневая документация',
        'Вход содержит высокоуровневые формулировки без детальных правил и проверок.',
        'Ожидается покрытие проверяемого ядра, маркировка недостающих деталей и отказ от неподтвержденных частностей.'
    );

INSERT OR IGNORE INTO dataset_profile_criterion_targets (
    id, input_profile_code, criterion_group, criterion_code, target_score, target_display, target_description
)
SELECT
    'profile_target_' || profile.code || '_requirement_' || criterion.code,
    profile.code,
    'requirement',
    criterion.code,
    criterion.target_score,
    criterion.target_display,
    criterion.target_description
FROM dataset_input_profiles profile
CROSS JOIN requirement_quality_criteria criterion;

INSERT OR IGNORE INTO dataset_profile_criterion_targets (
    id, input_profile_code, criterion_group, criterion_code, target_score, target_display, target_description
)
SELECT
    'profile_target_' || profile.code || '_decomposition_' || criterion.code,
    profile.code,
    'requirement_decomposition',
    criterion.code,
    criterion.target_score,
    criterion.target_display,
    criterion.target_description
FROM dataset_input_profiles profile
CROSS JOIN requirement_decomposition_quality_criteria criterion;

INSERT OR IGNORE INTO dataset_profile_criterion_targets (
    id, input_profile_code, criterion_group, criterion_code, target_score, target_display, target_description
)
SELECT
    'profile_target_' || profile.code || '_suite_' || criterion.code,
    profile.code,
    'test_suite',
    criterion.code,
    criterion.target_score,
    criterion.target_display,
    criterion.target_description
FROM dataset_input_profiles profile
CROSS JOIN test_suite_quality_criteria criterion;

INSERT OR IGNORE INTO dataset_profile_criterion_targets (
    id, input_profile_code, criterion_group, criterion_code, target_score, target_display, target_description
)
SELECT
    'profile_target_' || profile.code || '_test_case_' || criterion.code,
    profile.code,
    'test_case',
    criterion.code,
    criterion.target_score,
    criterion.target_display,
    criterion.target_description
FROM dataset_input_profiles profile
CROSS JOIN test_case_quality_criteria criterion;

UPDATE dataset_profile_criterion_targets
SET
    target_display = 'проверяемое ядро без додумывания',
    target_description = 'Цель для неполных требований: покрыть только явно выводимые сценарии, отметить пробелы и не добавлять неподтвержденные детали.'
WHERE input_profile_code = 'incomplete_fragmented_docs'
  AND criterion_group = 'test_suite'
  AND criterion_code IN ('positive_coverage', 'negative_coverage', 'required_checks_coverage', 'overall_completeness');

UPDATE dataset_profile_criterion_targets
SET
    target_display = 'галлюцинаций 0',
    target_description = 'Для неполных требований критически важно не компенсировать пробелы выдуманными условиями, ролями, статусами, API или UI.'
WHERE input_profile_code = 'incomplete_fragmented_docs'
  AND criterion_group = 'test_case'
  AND criterion_code = 'no_hallucinations';

UPDATE dataset_profile_criterion_targets
SET
    target_display = 'шум отфильтрован',
    target_description = 'Цель для шумной документации: лишние и нерелевантные фрагменты не должны превращаться в лишние тест-кейсы.'
WHERE input_profile_code = 'conflicting_noisy_docs'
  AND criterion_group = 'test_suite'
  AND criterion_code = 'suite_cleanliness';

UPDATE dataset_profile_criterion_targets
SET
    target_display = 'конфликты не склеены',
    target_description = 'Противоречивые источники нельзя молча объединять в одно уверенное требование; конфликт должен быть сохранен или явно отмечен.'
WHERE input_profile_code = 'conflicting_noisy_docs'
  AND criterion_group = 'requirement_decomposition'
  AND criterion_code = 'requirement_consolidation';

UPDATE dataset_profile_criterion_targets
SET
    target_display = 'проверяемое бизнес-ядро',
    target_description = 'Цель для бизнес-документации: покрыть проверяемые пользовательские сценарии без неподтвержденной технической детализации.'
WHERE input_profile_code = 'business_user_story_docs'
  AND criterion_group = 'test_suite'
  AND criterion_code IN ('positive_coverage', 'negative_coverage', 'required_checks_coverage', 'overall_completeness');

UPDATE dataset_profile_criterion_targets
SET
    target_display = 'ядро + явные пробелы',
    target_description = 'Цель для абстрактной документации: покрыть проверяемое ядро и не выдавать предположения за подтвержденные требования.'
WHERE input_profile_code = 'abstract_high_level_docs'
  AND criterion_group = 'test_suite'
  AND criterion_code IN ('positive_coverage', 'negative_coverage', 'required_checks_coverage', 'overall_completeness');
