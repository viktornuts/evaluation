INSERT OR IGNORE INTO requirement_quality_criteria (id, code, name, description, scale_min, scale_max)
VALUES
    ('crit_source_quality', 'source_quality', 'Источник требований', 'Надежность и пригодность источника требования: первичный источник, вторичный источник, устное уточнение, неясный источник.', 0, 10),
    ('crit_correctness', 'correctness', 'Корректность', 'Требование точно отражает реальную потребность, соответствует бизнес-цели и описывает именно то, что нужно системе делать.', 0, 10),
    ('crit_unambiguity', 'unambiguity', 'Однозначность', 'Требование допускает только одну интерпретацию и не содержит размытых маркеров вроде быстро, удобно, надежно, по возможности.', 0, 10),
    ('crit_completeness', 'completeness', 'Полнота требований', 'Требование содержит необходимую информацию: функции, входные и выходные данные, happy path, негативные сценарии, ошибки и граничные условия.', 0, 10),
    ('crit_consistency', 'consistency', 'Непротиворечивость требований', 'Требование не конфликтует само с собой, с другими требованиями и с нефункциональными ограничениями.', 0, 10),
    ('crit_testability', 'testability', 'Тестируемость', 'Требование содержит измеримые критерии приемки или четкие условия pass/fail.', 0, 10),
    ('crit_traceability', 'traceability', 'Прослеживаемость', 'Для требования явно указан источник, бизнес-цель, user story или другой фрагмент, который его обосновывает.', 0, 10),
    ('crit_modifiability', 'modifiability', 'Модифицируемость', 'Требование описано в одном месте без дублирования, а его изменение не вызывает неконтролируемых изменений в других требованиях.', 0, 10),
    ('crit_atomicity', 'atomicity', 'Атомарность', 'Требование описывает ровно одну функцию или поведение; если можно реализовать только половину требования, оно не атомарно.', 0, 10),
    ('crit_feasibility', 'feasibility', 'Выполнимость', 'Требование технологически реализуемо на основе общедоступных знаний и не содержит физических или технических противоречий.', 0, 10);

INSERT OR IGNORE INTO requirement_quality_criterion_score_levels (id, criterion_id, score_min, score_max, label, description)
VALUES
    ('qsl_source_quality_10', 'crit_source_quality', 10, 10, 'primary_confirmed_source', 'Требование полностью подтверждено первичным источником или явно указанным фрагментом документации.'),
    ('qsl_source_quality_8_9', 'crit_source_quality', 8, 9, 'strong_source', 'Источник понятен и надежен, но есть небольшие пробелы в версии, ссылке или детализации происхождения.'),
    ('qsl_source_quality_6_7', 'crit_source_quality', 6, 7, 'usable_source', 'Источник в целом пригоден, но часть контекста восстановлена косвенно или требует проверки.'),
    ('qsl_source_quality_4_5', 'crit_source_quality', 4, 5, 'weak_source', 'Источник неполный, вторичный или недостаточно конкретный; требование можно использовать только с оговорками.'),
    ('qsl_source_quality_1_3', 'crit_source_quality', 1, 3, 'unclear_source', 'Источник почти не прослеживается, основание требования сомнительно.'),
    ('qsl_source_quality_0', 'crit_source_quality', 0, 0, 'no_source', 'Источник отсутствует или требование противоречит доступным источникам.'),

    ('qsl_correctness_10', 'crit_correctness', 10, 10, 'correct', 'Требование точно отражает реальную потребность и соответствует назначению системы.'),
    ('qsl_correctness_8_9', 'crit_correctness', 8, 9, 'mostly_correct', 'Требование в целом корректно, есть minor-уточнения по формулировке или контексту.'),
    ('qsl_correctness_6_7', 'crit_correctness', 6, 7, 'partially_confirmed', 'Корректность вероятна, но часть бизнес-контекста или ограничений не подтверждена.'),
    ('qsl_correctness_4_5', 'crit_correctness', 4, 5, 'doubtful', 'Есть заметные сомнения: требование может описывать не ту потребность или не тот системный результат.'),
    ('qsl_correctness_1_3', 'crit_correctness', 1, 3, 'likely_incorrect', 'Требование скорее некорректно или искажает исходную потребность.'),
    ('qsl_correctness_0', 'crit_correctness', 0, 0, 'incorrect', 'Требование явно неверно, противоречит цели или не относится к системе.'),

    ('qsl_unambiguity_10', 'crit_unambiguity', 10, 10, 'unambiguous', 'Требование допускает одну интерпретацию, термины и условия понятны.'),
    ('qsl_unambiguity_8_9', 'crit_unambiguity', 8, 9, 'mostly_unambiguous', 'Требование почти однозначно, но есть minor-слова или контекст, который лучше уточнить.'),
    ('qsl_unambiguity_6_7', 'crit_unambiguity', 6, 7, 'somewhat_ambiguous', 'Есть неоднозначные слова или условия, но общий смысл можно восстановить.'),
    ('qsl_unambiguity_4_5', 'crit_unambiguity', 4, 5, 'ambiguous', 'Несколько существенных трактовок влияют на реализацию или тестирование.'),
    ('qsl_unambiguity_1_3', 'crit_unambiguity', 1, 3, 'highly_ambiguous', 'Требование сильно размыто: быстрый, удобный, надежный, по возможности и подобные маркеры без уточнений.'),
    ('qsl_unambiguity_0', 'crit_unambiguity', 0, 0, 'unusable_ambiguity', 'Смысл требования невозможно определить.'),

    ('qsl_completeness_10', 'crit_completeness', 10, 10, 'complete', 'Есть вся необходимая информация: действие, объект, условия, результат, ошибки и границы применимости.'),
    ('qsl_completeness_8_9', 'crit_completeness', 8, 9, 'mostly_complete', 'Основная информация есть, отсутствуют только некритичные уточнения.'),
    ('qsl_completeness_6_7', 'crit_completeness', 6, 7, 'partially_complete', 'Happy path понятен, но не хватает части входных данных, ограничений, ошибок или граничных условий.'),
    ('qsl_completeness_4_5', 'crit_completeness', 4, 5, 'incomplete', 'Недостающие детали заметно мешают генерации надежных тест-кейсов.'),
    ('qsl_completeness_1_3', 'crit_completeness', 1, 3, 'severely_incomplete', 'Есть только общий намек на функцию без достаточного контекста.'),
    ('qsl_completeness_0', 'crit_completeness', 0, 0, 'empty_or_missing', 'Требование фактически отсутствует или не содержит проверяемой информации.'),

    ('qsl_consistency_10', 'crit_consistency', 10, 10, 'consistent', 'Противоречий внутри требования, между требованиями и с ограничениями не обнаружено.'),
    ('qsl_consistency_8_9', 'crit_consistency', 8, 9, 'mostly_consistent', 'Есть minor-расхождения формулировок, не влияющие на смысл.'),
    ('qsl_consistency_6_7', 'crit_consistency', 6, 7, 'needs_check', 'Возможны противоречия или расхождения, но они не доказаны без дополнительного контекста.'),
    ('qsl_consistency_4_5', 'crit_consistency', 4, 5, 'partly_conflicting', 'Есть заметные конфликты значений, условий или ограничений.'),
    ('qsl_consistency_1_3', 'crit_consistency', 1, 3, 'conflicting', 'Требование конфликтует с другими требованиями или само с собой.'),
    ('qsl_consistency_0', 'crit_consistency', 0, 0, 'contradictory', 'Требование невозможно использовать из-за явного критического противоречия.'),

    ('qsl_testability_10', 'crit_testability', 10, 10, 'testable', 'Есть четкие pass/fail условия, измеримые критерии или наблюдаемый результат.'),
    ('qsl_testability_8_9', 'crit_testability', 8, 9, 'mostly_testable', 'Требование тестируемо, но часть проверок требует небольшого уточнения.'),
    ('qsl_testability_6_7', 'crit_testability', 6, 7, 'partially_testable', 'Можно проверить основную часть, но нет части чисел, порогов, условий или ожидаемых результатов.'),
    ('qsl_testability_4_5', 'crit_testability', 4, 5, 'hard_to_test', 'Тестирование возможно только через предположения или дополнительную договоренность.'),
    ('qsl_testability_1_3', 'crit_testability', 1, 3, 'not_testable', 'Нет измеримых критериев или четких условий pass/fail.'),
    ('qsl_testability_0', 'crit_testability', 0, 0, 'untestable', 'Требование невозможно проверить как сформулированное.'),

    ('qsl_traceability_10', 'crit_traceability', 10, 10, 'traceable', 'Требование явно связано с конкретным источником, фрагментом, бизнес-целью или user story.'),
    ('qsl_traceability_8_9', 'crit_traceability', 8, 9, 'mostly_traceable', 'Связь с источником понятна, но не хватает minor-деталей ссылки или обоснования.'),
    ('qsl_traceability_6_7', 'crit_traceability', 6, 7, 'indirectly_traceable', 'Связь восстановима косвенно, но не зафиксирована явно.'),
    ('qsl_traceability_4_5', 'crit_traceability', 4, 5, 'weak_traceability', 'Источник или бизнес-обоснование указаны слишком общо.'),
    ('qsl_traceability_1_3', 'crit_traceability', 1, 3, 'barely_traceable', 'Требование почти висит в воздухе, связь с источником сомнительна.'),
    ('qsl_traceability_0', 'crit_traceability', 0, 0, 'not_traceable', 'Нет прослеживаемости к источнику или обоснованию.'),

    ('qsl_modifiability_10', 'crit_modifiability', 10, 10, 'modifiable', 'Требование описано в одном месте, не дублируется и может изменяться локально.'),
    ('qsl_modifiability_8_9', 'crit_modifiability', 8, 9, 'mostly_modifiable', 'Есть небольшая связность с другими требованиями, но изменение остается контролируемым.'),
    ('qsl_modifiability_6_7', 'crit_modifiability', 6, 7, 'somewhat_modifiable', 'Есть зависимость или частичное дублирование, изменение потребует проверки соседних требований.'),
    ('qsl_modifiability_4_5', 'crit_modifiability', 4, 5, 'hard_to_modify', 'Требование заметно дублирует другие или сильно связано с несколькими местами.'),
    ('qsl_modifiability_1_3', 'crit_modifiability', 1, 3, 'unsafe_to_modify', 'Изменение требования почти наверняка приведет к неконтролируемым правкам в других требованиях.'),
    ('qsl_modifiability_0', 'crit_modifiability', 0, 0, 'not_modifiable', 'Невозможно изменить требование без пересборки значительной части набора.'),

    ('qsl_atomicity_10', 'crit_atomicity', 10, 10, 'atomic', 'Требование описывает ровно одну функцию, правило или поведение.'),
    ('qsl_atomicity_8_9', 'crit_atomicity', 8, 9, 'mostly_atomic', 'Почти атомарно, но есть minor-связанные уточнения в той же формулировке.'),
    ('qsl_atomicity_6_7', 'crit_atomicity', 6, 7, 'partly_atomic', 'В требовании есть 2 близких аспекта, которые лучше разделить, но они относятся к одному сценарию.'),
    ('qsl_atomicity_4_5', 'crit_atomicity', 4, 5, 'non_atomic', 'Склеены несколько самостоятельных действий, условий или результатов.'),
    ('qsl_atomicity_1_3', 'crit_atomicity', 1, 3, 'strongly_non_atomic', 'Требование состоит из набора разных требований; можно реализовать только часть.'),
    ('qsl_atomicity_0', 'crit_atomicity', 0, 0, 'not_a_requirement', 'Формулировка не является отдельным требованием.'),

    ('qsl_feasibility_10', 'crit_feasibility', 10, 10, 'feasible', 'Требование технологически реализуемо и не содержит физических или технических противоречий.'),
    ('qsl_feasibility_8_9', 'crit_feasibility', 8, 9, 'mostly_feasible', 'Выполнимо, есть только minor-технические уточнения.'),
    ('qsl_feasibility_6_7', 'crit_feasibility', 6, 7, 'likely_feasible', 'Вероятно выполнимо, но не хватает технического контекста или ограничений.'),
    ('qsl_feasibility_4_5', 'crit_feasibility', 4, 5, 'questionable_feasibility', 'Выполнимость сомнительна без существенных допущений.'),
    ('qsl_feasibility_1_3', 'crit_feasibility', 1, 3, 'likely_infeasible', 'Требование выглядит технически нереалистичным или противоречивым.'),
    ('qsl_feasibility_0', 'crit_feasibility', 0, 0, 'infeasible', 'Требование явно невыполнимо или физически/технически противоречиво.');

INSERT OR IGNORE INTO test_case_quality_criteria (id, code, name, description, scale_min, scale_max)
VALUES
    ('tc_crit_template_compliance', 'template_compliance', 'Соответствие шаблону', 'Насколько тест-кейс соответствует утвержденному шаблону и ожидаемой структуре.', 0, 10),
    ('tc_crit_required_fields_completeness', 'required_fields_completeness', 'Полнота обязательных полей', 'Насколько заполнены обязательные атрибуты тест-кейса.', 0, 10),
    ('tc_crit_step_atomicity', 'step_atomicity', 'Атомарность шагов', 'Насколько каждый шаг содержит одно действие и не смешивает несколько проверок.', 0, 10),
    ('tc_crit_expected_result_quality', 'expected_result_quality', 'Качество ожидаемых результатов', 'Насколько ожидаемые результаты конкретны, проверяемы и соответствуют действиям.', 0, 10),
    ('tc_crit_preconditions_quality', 'preconditions_quality', 'Качество предусловий', 'Насколько предусловия описывают состояние системы до начала сценария.', 0, 10),
    ('tc_crit_postconditions_quality', 'postconditions_quality', 'Качество постусловий', 'Насколько постусловия описывают состояние после выполнения сценария и не содержат шаги.', 0, 10),
    ('tc_crit_classification_correctness', 'classification_correctness', 'Корректность вида ТК', 'Насколько вид тест-кейса соответствует содержанию сценария.', 0, 10),
    ('tc_crit_direction_correctness', 'direction_correctness', 'Корректность направления', 'Насколько направление positive/negative соответствует входным данным и ожидаемому результату.', 0, 10),
    ('tc_crit_traceability_to_requirement', 'traceability_to_requirement', 'Трассируемость к требованию', 'Насколько тест-кейс и его шаги связаны с требованиями.', 0, 10),
    ('tc_crit_no_hallucinations', 'no_hallucinations', 'Отсутствие галлюцинаций', 'Насколько тест-кейс не содержит фактов, отсутствующих в требованиях и источниках.', 0, 10),
    ('tc_crit_no_unsupported_specificity', 'no_unsupported_specificity', 'Отсутствие неподтвержденной конкретизации', 'Насколько тест-кейс избегает неподтвержденных UI-элементов, endpoint, кодов, ролей и иных деталей.', 0, 10);

INSERT OR IGNORE INTO test_suite_quality_criteria (id, code, name, description, scale_min, scale_max)
VALUES
    ('suite_crit_requirement_coverage', 'requirement_coverage', 'Покрытие требований', 'Насколько набор тест-кейсов покрывает пригодные требования.', 0, 10),
    ('suite_crit_positive_coverage', 'positive_coverage', 'Позитивное покрытие', 'Насколько набор содержит необходимые позитивные сценарии.', 0, 10),
    ('suite_crit_negative_coverage', 'negative_coverage', 'Негативное покрытие', 'Насколько набор содержит необходимые негативные сценарии.', 0, 10),
    ('suite_crit_required_checks_coverage', 'required_checks_coverage', 'Покрытие обязательных проверок', 'Насколько набор покрывает обязательные проверки из эталона.', 0, 10),
    ('suite_crit_duplicate_rate', 'duplicate_rate', 'Уровень дублей', 'Насколько набор свободен от дублирующих тест-кейсов.', 0, 10),
    ('suite_crit_extra_relevant_test_case_rate', 'extra_relevant_test_case_rate', 'Релевантность дополнительных ТК', 'Насколько дополнительные тест-кейсы релевантны и не искажают требования.', 0, 10),
    ('suite_crit_irrelevant_test_case_rate', 'irrelevant_test_case_rate', 'Отсутствие нерелевантных ТК', 'Насколько набор свободен от тест-кейсов, не связанных с требованиями.', 0, 10),
    ('suite_crit_coverage_balance', 'coverage_balance', 'Сбалансированность покрытия', 'Насколько покрытие распределено по требованиям без перекоса в один участок.', 0, 10),
    ('suite_crit_overall_completeness', 'overall_completeness', 'Общая полнота набора', 'Насколько набор тест-кейсов достаточен для проверяемого скоупа.', 0, 10),
    ('suite_crit_no_suite_level_hallucinations', 'no_suite_level_hallucinations', 'Отсутствие галлюцинаций на уровне набора', 'Насколько весь набор не добавляет неподтвержденные сущности, сценарии и детали.', 0, 10);
