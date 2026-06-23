INSERT OR IGNORE INTO requirement_decomposition_quality_criteria (id, code, name, description, scale_min, scale_max)
VALUES
    ('decomp_crit_completeness', 'decomposition_completeness', 'Полнота декомпозиции', 'Насколько все значимые атомарные требования из входного требования выделены в результате декомпозиции.', 0, 10),
    ('decomp_crit_boundaries', 'decomposition_boundaries', 'Границы атомарных требований', 'Насколько корректно определены границы атомарных требований: без склеивания независимых требований и без бессмысленного дробления.', 0, 10),
    ('decomp_crit_consolidation', 'requirement_consolidation', 'Консолидация требований', 'Насколько одинаковая или связанная информация из разных источников объединена корректно, без дублей, потери смысла и противоречий.', 0, 10);

INSERT OR IGNORE INTO requirement_decomposition_quality_criterion_score_levels (id, criterion_id, score_min, score_max, label, description)
VALUES
    ('decomp_qsl_completeness_10', 'decomp_crit_completeness', 10, 10, 'complete_decomposition', 'Все значимые атомарные требования из входного требования выделены, потерь нет.'),
    ('decomp_qsl_completeness_8_9', 'decomp_crit_completeness', 8, 9, 'mostly_complete_decomposition', 'Почти все значимые атомарные требования выделены, есть только minor-пропуски.'),
    ('decomp_qsl_completeness_6_7', 'decomp_crit_completeness', 6, 7, 'partly_complete_decomposition', 'Выделена основная часть атомарных требований, но есть заметные пропуски.'),
    ('decomp_qsl_completeness_4_5', 'decomp_crit_completeness', 4, 5, 'weak_decomposition_completeness', 'Потеряна существенная часть требований или важных ограничений.'),
    ('decomp_qsl_completeness_1_3', 'decomp_crit_completeness', 1, 3, 'poor_decomposition_completeness', 'Выделены единичные требования, большая часть смысла входного требования потеряна.'),
    ('decomp_qsl_completeness_0', 'decomp_crit_completeness', 0, 0, 'no_decomposition', 'Декомпозиция отсутствует или не отражает входное требование.'),

    ('decomp_qsl_boundaries_10', 'decomp_crit_boundaries', 10, 10, 'correct_boundaries', 'Атомарные требования выделены самостоятельными проверяемыми единицами с корректными границами.'),
    ('decomp_qsl_boundaries_8_9', 'decomp_crit_boundaries', 8, 9, 'mostly_correct_boundaries', 'Границы в целом корректны, есть minor-спорные разделения или объединения.'),
    ('decomp_qsl_boundaries_6_7', 'decomp_crit_boundaries', 6, 7, 'partly_correct_boundaries', 'Часть требований нарезана корректно, но есть заметные случаи склейки или избыточного дробления.'),
    ('decomp_qsl_boundaries_4_5', 'decomp_crit_boundaries', 4, 5, 'weak_boundaries', 'Границы часто нарушены: независимые требования склеены или атомарность потеряна.'),
    ('decomp_qsl_boundaries_1_3', 'decomp_crit_boundaries', 1, 3, 'poor_boundaries', 'Декомпозиция в основном состоит из некорректно нарезанных или несамостоятельных фрагментов.'),
    ('decomp_qsl_boundaries_0', 'decomp_crit_boundaries', 0, 0, 'invalid_boundaries', 'Границы требований не определены или декомпозиция непригодна.'),

    ('decomp_qsl_consolidation_10', 'decomp_crit_consolidation', 10, 10, 'correct_consolidation', 'Одинаковая или связанная информация из разных источников объединена корректно, без дублей и противоречий.'),
    ('decomp_qsl_consolidation_8_9', 'decomp_crit_consolidation', 8, 9, 'mostly_correct_consolidation', 'Консолидация в целом корректна, есть minor-дубли или minor-потери контекста.'),
    ('decomp_qsl_consolidation_6_7', 'decomp_crit_consolidation', 6, 7, 'partly_correct_consolidation', 'Часть связанной информации объединена корректно, часть продублирована или требует ревью.'),
    ('decomp_qsl_consolidation_4_5', 'decomp_crit_consolidation', 4, 5, 'weak_consolidation', 'Есть заметные дубли, несогласованные формулировки или потеря связей между источниками.'),
    ('decomp_qsl_consolidation_1_3', 'decomp_crit_consolidation', 1, 3, 'poor_consolidation', 'Модель почти не консолидирует связанные требования и плодит дубли или конфликтующие варианты.'),
    ('decomp_qsl_consolidation_0', 'decomp_crit_consolidation', 0, 0, 'no_consolidation', 'Консолидация отсутствует или результат вводит в заблуждение.');

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
    ('tc_crit_no_unsupported_specificity', 'no_unsupported_specificity', 'Отсутствие неподтвержденной конкретизации', 'Насколько тест-кейс избегает неподтвержденных UI-элементов, endpoint, кодов, ролей и иных деталей.', 0, 10),
    ('tc_crit_step_action_quality', 'step_action_quality', 'Качество формулировки шагов', 'Насколько шаги сформулированы как конкретные, однозначные и выполнимые действия.', 0, 10),
    ('tc_crit_scenario_logic', 'scenario_logic', 'Логика сценария', 'Насколько последовательность шагов сохраняет проверяемую логику сценария и не нарушает смысл требования.', 0, 10);

INSERT OR IGNORE INTO test_case_quality_criterion_score_levels (id, criterion_id, score_min, score_max, label, description)
VALUES
    ('tc_qsl_template_10', 'tc_crit_template_compliance', 10, 10, 'template_compliant', 'ТК полностью соответствует утвержденному шаблону и ожидаемой структуре для своего вида.'),
    ('tc_qsl_template_8_9', 'tc_crit_template_compliance', 8, 9, 'mostly_template_compliant', 'Шаблон в целом соблюден, есть minor-отклонения без влияния на читаемость и проверяемость.'),
    ('tc_qsl_template_6_7', 'tc_crit_template_compliance', 6, 7, 'partly_template_compliant', 'Основная структура есть, но часть блоков или формат заполнены нестабильно.'),
    ('tc_qsl_template_4_5', 'tc_crit_template_compliance', 4, 5, 'weak_template_compliance', 'Шаблон соблюден частично, структура мешает использовать ТК без доработки.'),
    ('tc_qsl_template_1_3', 'tc_crit_template_compliance', 1, 3, 'poor_template_compliance', 'ТК почти не соответствует шаблону.'),
    ('tc_qsl_template_0', 'tc_crit_template_compliance', 0, 0, 'no_template', 'Шаблон отсутствует или ТК невозможно распознать как тест-кейс.'),

    ('tc_qsl_required_fields_10', 'tc_crit_required_fields_completeness', 10, 10, 'required_fields_complete', 'Все обязательные атрибуты ТК заполнены корректно.'),
    ('tc_qsl_required_fields_8_9', 'tc_crit_required_fields_completeness', 8, 9, 'required_fields_mostly_complete', 'Обязательные поля почти все заполнены, есть minor-замечания.'),
    ('tc_qsl_required_fields_6_7', 'tc_crit_required_fields_completeness', 6, 7, 'required_fields_partial', 'Часть обязательных полей заполнена неполно или неоднозначно.'),
    ('tc_qsl_required_fields_4_5', 'tc_crit_required_fields_completeness', 4, 5, 'required_fields_weak', 'Существенная часть обязательных полей отсутствует или заполнена плохо.'),
    ('tc_qsl_required_fields_1_3', 'tc_crit_required_fields_completeness', 1, 3, 'required_fields_poor', 'Заполнены единичные обязательные поля.'),
    ('tc_qsl_required_fields_0', 'tc_crit_required_fields_completeness', 0, 0, 'required_fields_missing', 'Обязательные атрибуты отсутствуют.'),

    ('tc_qsl_step_atomicity_10', 'tc_crit_step_atomicity', 10, 10, 'atomic_steps', 'Каждый шаг содержит одно действие или одну проверяемую операцию.'),
    ('tc_qsl_step_atomicity_8_9', 'tc_crit_step_atomicity', 8, 9, 'mostly_atomic_steps', 'Шаги почти атомарны, есть единичные minor-склейки.'),
    ('tc_qsl_step_atomicity_6_7', 'tc_crit_step_atomicity', 6, 7, 'partly_atomic_steps', 'Часть шагов смешивает несколько действий, но сценарий остается понятным.'),
    ('tc_qsl_step_atomicity_4_5', 'tc_crit_step_atomicity', 4, 5, 'non_atomic_steps', 'Много шагов объединяют разные действия или проверки.'),
    ('tc_qsl_step_atomicity_1_3', 'tc_crit_step_atomicity', 1, 3, 'strongly_non_atomic_steps', 'Шаги в основном неатомарны и требуют переразбиения.'),
    ('tc_qsl_step_atomicity_0', 'tc_crit_step_atomicity', 0, 0, 'no_steps', 'Шаги отсутствуют или не являются шагами тестового сценария.'),

    ('tc_qsl_expected_result_10', 'tc_crit_expected_result_quality', 10, 10, 'expected_results_complete', 'У каждого шага есть конкретный, проверяемый и логически соответствующий ожидаемый результат.'),
    ('tc_qsl_expected_result_8_9', 'tc_crit_expected_result_quality', 8, 9, 'expected_results_mostly_complete', 'Ожидаемые результаты почти все корректны, есть minor-неточности.'),
    ('tc_qsl_expected_result_6_7', 'tc_crit_expected_result_quality', 6, 7, 'expected_results_partial', 'Часть ожидаемых результатов неполная, но основной сценарий проверяем.'),
    ('tc_qsl_expected_result_4_5', 'tc_crit_expected_result_quality', 4, 5, 'expected_results_weak', 'Ожидаемые результаты часто общие, непроверяемые или плохо связаны с шагами.'),
    ('tc_qsl_expected_result_1_3', 'tc_crit_expected_result_quality', 1, 3, 'expected_results_poor', 'Ожидаемые результаты почти отсутствуют или не соответствуют действиям.'),
    ('tc_qsl_expected_result_0', 'tc_crit_expected_result_quality', 0, 0, 'expected_results_missing', 'Ожидаемые результаты отсутствуют.'),

    ('tc_qsl_preconditions_10', 'tc_crit_preconditions_quality', 10, 10, 'preconditions_clear', 'Предусловия полно и корректно описывают состояние системы до начала сценария.'),
    ('tc_qsl_preconditions_8_9', 'tc_crit_preconditions_quality', 8, 9, 'preconditions_mostly_clear', 'Предусловия в целом корректны, есть minor-пробелы.'),
    ('tc_qsl_preconditions_6_7', 'tc_crit_preconditions_quality', 6, 7, 'preconditions_partial', 'Предусловия частично описаны, часть контекста нужно уточнить.'),
    ('tc_qsl_preconditions_4_5', 'tc_crit_preconditions_quality', 4, 5, 'preconditions_weak', 'Предусловия неполные или плохо связаны со сценарием.'),
    ('tc_qsl_preconditions_1_3', 'tc_crit_preconditions_quality', 1, 3, 'preconditions_poor', 'Предусловия почти потеряны или сформулированы как шаги.'),
    ('tc_qsl_preconditions_0', 'tc_crit_preconditions_quality', 0, 0, 'preconditions_missing', 'Необходимые предусловия отсутствуют.'),

    ('tc_qsl_postconditions_10', 'tc_crit_postconditions_quality', 10, 10, 'postconditions_clear', 'Постусловия корректно описывают состояние после выполнения сценария и не содержат шаги.'),
    ('tc_qsl_postconditions_8_9', 'tc_crit_postconditions_quality', 8, 9, 'postconditions_mostly_clear', 'Постусловия в целом корректны, есть minor-замечания.'),
    ('tc_qsl_postconditions_6_7', 'tc_crit_postconditions_quality', 6, 7, 'postconditions_partial', 'Постусловия частично полезны, но требуют уточнений.'),
    ('tc_qsl_postconditions_4_5', 'tc_crit_postconditions_quality', 4, 5, 'postconditions_weak', 'Постусловия неполные, спорные или частично содержат действия.'),
    ('tc_qsl_postconditions_1_3', 'tc_crit_postconditions_quality', 1, 3, 'postconditions_poor', 'Постусловия почти не описывают итоговое состояние или состоят из шагов.'),
    ('tc_qsl_postconditions_0', 'tc_crit_postconditions_quality', 0, 0, 'postconditions_invalid', 'Постусловия отсутствуют там, где нужны, или полностью некорректны.'),

    ('tc_qsl_classification_10', 'tc_crit_classification_correctness', 10, 10, 'classification_correct', 'Вид ТК полностью соответствует содержанию сценария.'),
    ('tc_qsl_classification_8_9', 'tc_crit_classification_correctness', 8, 9, 'classification_mostly_correct', 'Вид ТК в целом корректен, есть minor-спорность.'),
    ('tc_qsl_classification_6_7', 'tc_crit_classification_correctness', 6, 7, 'classification_partly_correct', 'Вид ТК вероятно корректен, но требует проверки.'),
    ('tc_qsl_classification_4_5', 'tc_crit_classification_correctness', 4, 5, 'classification_doubtful', 'Вид ТК слабо соответствует сценарию.'),
    ('tc_qsl_classification_1_3', 'tc_crit_classification_correctness', 1, 3, 'classification_wrong', 'Вид ТК скорее неверный.'),
    ('tc_qsl_classification_0', 'tc_crit_classification_correctness', 0, 0, 'classification_invalid', 'Вид ТК отсутствует или полностью неверен.'),

    ('tc_qsl_direction_10', 'tc_crit_direction_correctness', 10, 10, 'direction_correct', 'Направление positive/negative полностью соответствует входным данным и ожидаемому результату.'),
    ('tc_qsl_direction_8_9', 'tc_crit_direction_correctness', 8, 9, 'direction_mostly_correct', 'Направление в целом корректно, есть minor-спорность.'),
    ('tc_qsl_direction_6_7', 'tc_crit_direction_correctness', 6, 7, 'direction_partly_correct', 'Направление вероятно корректно, но часть условий спорна.'),
    ('tc_qsl_direction_4_5', 'tc_crit_direction_correctness', 4, 5, 'direction_doubtful', 'Направление плохо соответствует сценарию.'),
    ('tc_qsl_direction_1_3', 'tc_crit_direction_correctness', 1, 3, 'direction_wrong', 'Направление скорее неверное.'),
    ('tc_qsl_direction_0', 'tc_crit_direction_correctness', 0, 0, 'direction_invalid', 'Направление отсутствует или полностью неверно.'),

    ('tc_qsl_traceability_10', 'tc_crit_traceability_to_requirement', 10, 10, 'traceable_to_requirement', 'ТК и его шаги явно связаны с требованием или требованиями, которые проверяют.'),
    ('tc_qsl_traceability_8_9', 'tc_crit_traceability_to_requirement', 8, 9, 'mostly_traceable_to_requirement', 'Связь с требованиями понятна, есть minor-пробелы в детализации.'),
    ('tc_qsl_traceability_6_7', 'tc_crit_traceability_to_requirement', 6, 7, 'partly_traceable_to_requirement', 'Связь с требованиями частичная или восстановима косвенно.'),
    ('tc_qsl_traceability_4_5', 'tc_crit_traceability_to_requirement', 4, 5, 'weak_traceability_to_requirement', 'Связь с требованиями слабая, часть шагов не обоснована.'),
    ('tc_qsl_traceability_1_3', 'tc_crit_traceability_to_requirement', 1, 3, 'poor_traceability_to_requirement', 'ТК почти не трассируется к проверяемым требованиям.'),
    ('tc_qsl_traceability_0', 'tc_crit_traceability_to_requirement', 0, 0, 'not_traceable_to_requirement', 'Связь с требованиями отсутствует.'),

    ('tc_qsl_no_hallucinations_10', 'tc_crit_no_hallucinations', 10, 10, 'no_hallucinations', 'ТК не содержит фактов, отсутствующих в требованиях и источниках.'),
    ('tc_qsl_no_hallucinations_8_9', 'tc_crit_no_hallucinations', 8, 9, 'minor_unsupported_fact_risk', 'Есть minor-детали с низким риском неподтвержденности.'),
    ('tc_qsl_no_hallucinations_6_7', 'tc_crit_no_hallucinations', 6, 7, 'some_unsupported_facts', 'Есть отдельные неподтвержденные факты, требуется ревью.'),
    ('tc_qsl_no_hallucinations_4_5', 'tc_crit_no_hallucinations', 4, 5, 'many_unsupported_facts', 'Неподтвержденные факты заметно влияют на корректность ТК.'),
    ('tc_qsl_no_hallucinations_1_3', 'tc_crit_no_hallucinations', 1, 3, 'hallucinated_test_case', 'ТК в основном построен на выдуманных фактах.'),
    ('tc_qsl_no_hallucinations_0', 'tc_crit_no_hallucinations', 0, 0, 'invalid_hallucinated_test_case', 'ТК непригоден из-за галлюцинаций.'),

    ('tc_qsl_no_unsupported_specificity_10', 'tc_crit_no_unsupported_specificity', 10, 10, 'no_unsupported_specificity', 'ТК не добавляет неподтвержденные UI-элементы, endpoint, роли, коды или тексты ошибок.'),
    ('tc_qsl_no_unsupported_specificity_8_9', 'tc_crit_no_unsupported_specificity', 8, 9, 'minor_specificity_risk', 'Есть minor-конкретизация, которая почти однозначно следует из контекста.'),
    ('tc_qsl_no_unsupported_specificity_6_7', 'tc_crit_no_unsupported_specificity', 6, 7, 'some_unsupported_specificity', 'Есть отдельные неподтвержденные конкретные детали.'),
    ('tc_qsl_no_unsupported_specificity_4_5', 'tc_crit_no_unsupported_specificity', 4, 5, 'many_unsupported_specificity', 'Неподтвержденная конкретизация заметно влияет на проверку.'),
    ('tc_qsl_no_unsupported_specificity_1_3', 'tc_crit_no_unsupported_specificity', 1, 3, 'mostly_unsupported_specificity', 'ТК в основном содержит неподтвержденные детали.'),
    ('tc_qsl_no_unsupported_specificity_0', 'tc_crit_no_unsupported_specificity', 0, 0, 'invalid_unsupported_specificity', 'ТК непригоден из-за неподтвержденной конкретизации.'),

    ('tc_qsl_step_action_quality_10', 'tc_crit_step_action_quality', 10, 10, 'clear_executable_steps', 'Шаги сформулированы как конкретные, однозначные и выполнимые действия.'),
    ('tc_qsl_step_action_quality_8_9', 'tc_crit_step_action_quality', 8, 9, 'mostly_clear_executable_steps', 'Шаги в целом конкретны и выполнимы, есть minor-неточности.'),
    ('tc_qsl_step_action_quality_6_7', 'tc_crit_step_action_quality', 6, 7, 'partly_clear_steps', 'Часть шагов конкретна, часть требует уточнения.'),
    ('tc_qsl_step_action_quality_4_5', 'tc_crit_step_action_quality', 4, 5, 'weak_step_actions', 'Шаги часто общие, неоднозначные или плохо выполнимые.'),
    ('tc_qsl_step_action_quality_1_3', 'tc_crit_step_action_quality', 1, 3, 'poor_step_actions', 'Шаги почти невозможно выполнить без домысливания.'),
    ('tc_qsl_step_action_quality_0', 'tc_crit_step_action_quality', 0, 0, 'invalid_step_actions', 'Шаги отсутствуют или не являются действиями.'),

    ('tc_qsl_scenario_logic_10', 'tc_crit_scenario_logic', 10, 10, 'logical_scenario', 'Последовательность шагов сохраняет корректную логику сценария и проверяемое требование.'),
    ('tc_qsl_scenario_logic_8_9', 'tc_crit_scenario_logic', 8, 9, 'mostly_logical_scenario', 'Логика сценария в целом корректна, есть minor-неточности.'),
    ('tc_qsl_scenario_logic_6_7', 'tc_crit_scenario_logic', 6, 7, 'partly_logical_scenario', 'Основная логика понятна, но есть спорные переходы или пропуски.'),
    ('tc_qsl_scenario_logic_4_5', 'tc_crit_scenario_logic', 4, 5, 'weak_scenario_logic', 'Логика сценария часто нарушается или требует существенной доработки.'),
    ('tc_qsl_scenario_logic_1_3', 'tc_crit_scenario_logic', 1, 3, 'poor_scenario_logic', 'Сценарий почти нелогичен и плохо проверяет требование.'),
    ('tc_qsl_scenario_logic_0', 'tc_crit_scenario_logic', 0, 0, 'invalid_scenario_logic', 'Сценарий отсутствует или полностью некорректен.');

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
    ('suite_crit_no_suite_level_hallucinations', 'no_suite_level_hallucinations', 'Отсутствие галлюцинаций на уровне набора', 'Насколько весь набор не добавляет неподтвержденные сущности, сценарии и детали.', 0, 10),
    ('suite_crit_insufficient_detail_handling', 'insufficient_detail_handling', 'Обработка insufficient_detail', 'Насколько набор не содержит ТК с додуманными деталями по требованиям, непригодным для генерации.', 0, 10),
    ('suite_crit_multi_requirement_traceability', 'multi_requirement_traceability', 'Трассировка ТК к нескольким требованиям', 'Насколько ТК, покрывающие несколько требований, релевантны каждому связанному требованию.', 0, 10);

INSERT OR IGNORE INTO test_suite_quality_criterion_score_levels (id, criterion_id, score_min, score_max, label, description)
VALUES
    ('suite_qsl_requirement_coverage_10', 'suite_crit_requirement_coverage', 10, 10, 'fully_covered', 'Все пригодные требования покрыты корректными связанными ТК.'),
    ('suite_qsl_requirement_coverage_8_9', 'suite_crit_requirement_coverage', 8, 9, 'mostly_covered', 'Покрыто почти всё, есть единичные некритичные пропуски.'),
    ('suite_qsl_requirement_coverage_6_7', 'suite_crit_requirement_coverage', 6, 7, 'partially_covered', 'Покрыта основная часть требований, но есть заметные пропуски.'),
    ('suite_qsl_requirement_coverage_4_5', 'suite_crit_requirement_coverage', 4, 5, 'weak_coverage', 'Покрытие фрагментарное, значимая часть требований не имеет ТК.'),
    ('suite_qsl_requirement_coverage_1_3', 'suite_crit_requirement_coverage', 1, 3, 'poor_coverage', 'Покрыты единичные требования, набор почти не отражает скоуп.'),
    ('suite_qsl_requirement_coverage_0', 'suite_crit_requirement_coverage', 0, 0, 'not_covered', 'Пригодные требования не покрыты тест-кейсами.'),

    ('suite_qsl_positive_coverage_10', 'suite_crit_positive_coverage', 10, 10, 'positive_complete', 'Для всех требований, где нужен позитивный сценарий, есть релевантные позитивные ТК.'),
    ('suite_qsl_positive_coverage_8_9', 'suite_crit_positive_coverage', 8, 9, 'positive_mostly_complete', 'Позитивное покрытие почти полное, есть minor-пропуски.'),
    ('suite_qsl_positive_coverage_6_7', 'suite_crit_positive_coverage', 6, 7, 'positive_partial', 'Позитивные сценарии есть для основной части требований.'),
    ('suite_qsl_positive_coverage_4_5', 'suite_crit_positive_coverage', 4, 5, 'positive_weak', 'Позитивные сценарии есть выборочно и не закрывают скоуп.'),
    ('suite_qsl_positive_coverage_1_3', 'suite_crit_positive_coverage', 1, 3, 'positive_poor', 'Позитивное покрытие почти отсутствует.'),
    ('suite_qsl_positive_coverage_0', 'suite_crit_positive_coverage', 0, 0, 'positive_missing', 'Позитивные ТК отсутствуют там, где они нужны.'),

    ('suite_qsl_negative_coverage_10', 'suite_crit_negative_coverage', 10, 10, 'negative_complete', 'Для всех требований, где нужны негативные сценарии, есть релевантные негативные ТК.'),
    ('suite_qsl_negative_coverage_8_9', 'suite_crit_negative_coverage', 8, 9, 'negative_mostly_complete', 'Негативное покрытие почти полное, есть minor-пропуски.'),
    ('suite_qsl_negative_coverage_6_7', 'suite_crit_negative_coverage', 6, 7, 'negative_partial', 'Негативные сценарии есть для основной части применимых требований.'),
    ('suite_qsl_negative_coverage_4_5', 'suite_crit_negative_coverage', 4, 5, 'negative_weak', 'Негативные сценарии есть выборочно и не закрывают основные риски.'),
    ('suite_qsl_negative_coverage_1_3', 'suite_crit_negative_coverage', 1, 3, 'negative_poor', 'Негативное покрытие почти отсутствует.'),
    ('suite_qsl_negative_coverage_0', 'suite_crit_negative_coverage', 0, 0, 'negative_missing', 'Негативные ТК отсутствуют там, где они нужны.'),

    ('suite_qsl_required_checks_10', 'suite_crit_required_checks_coverage', 10, 10, 'required_checks_complete', 'Все обязательные проверки из эталона или требования покрыты.'),
    ('suite_qsl_required_checks_8_9', 'suite_crit_required_checks_coverage', 8, 9, 'required_checks_mostly_complete', 'Почти все обязательные проверки покрыты.'),
    ('suite_qsl_required_checks_6_7', 'suite_crit_required_checks_coverage', 6, 7, 'required_checks_partial', 'Покрыта основная часть обязательных проверок.'),
    ('suite_qsl_required_checks_4_5', 'suite_crit_required_checks_coverage', 4, 5, 'required_checks_weak', 'Покрыты отдельные обязательные проверки, но есть существенные пропуски.'),
    ('suite_qsl_required_checks_1_3', 'suite_crit_required_checks_coverage', 1, 3, 'required_checks_poor', 'Большинство обязательных проверок пропущено.'),
    ('suite_qsl_required_checks_0', 'suite_crit_required_checks_coverage', 0, 0, 'required_checks_missing', 'Обязательные проверки не покрыты.'),

    ('suite_qsl_duplicate_rate_10', 'suite_crit_duplicate_rate', 10, 10, 'no_duplicates', 'В наборе нет дублирующих ТК или дублирующих проверок.'),
    ('suite_qsl_duplicate_rate_8_9', 'suite_crit_duplicate_rate', 8, 9, 'minor_duplicates', 'Есть единичные почти-дубли, не влияющие на итоговую полезность набора.'),
    ('suite_qsl_duplicate_rate_6_7', 'suite_crit_duplicate_rate', 6, 7, 'some_duplicates', 'Есть заметные дубли, но набор всё ещё полезен.'),
    ('suite_qsl_duplicate_rate_4_5', 'suite_crit_duplicate_rate', 4, 5, 'many_duplicates', 'Дубли занимают существенную часть набора.'),
    ('suite_qsl_duplicate_rate_1_3', 'suite_crit_duplicate_rate', 1, 3, 'mostly_duplicates', 'Набор в основном состоит из повторов.'),
    ('suite_qsl_duplicate_rate_0', 'suite_crit_duplicate_rate', 0, 0, 'duplicate_set', 'Набор не добавляет полезного покрытия из-за дублей.'),

    ('suite_qsl_extra_relevant_10', 'suite_crit_extra_relevant_test_case_rate', 10, 10, 'extra_relevant', 'Все дополнительные ТК сверх эталона релевантны, не дублируют и не искажают требования.'),
    ('suite_qsl_extra_relevant_8_9', 'suite_crit_extra_relevant_test_case_rate', 8, 9, 'extra_mostly_relevant', 'Дополнительные ТК в основном релевантны, есть minor-замечания.'),
    ('suite_qsl_extra_relevant_6_7', 'suite_crit_extra_relevant_test_case_rate', 6, 7, 'extra_partly_relevant', 'Часть дополнительных ТК полезна, часть спорна.'),
    ('suite_qsl_extra_relevant_4_5', 'suite_crit_extra_relevant_test_case_rate', 4, 5, 'extra_weak_relevance', 'Большая часть дополнительных ТК слабо связана с требованиями.'),
    ('suite_qsl_extra_relevant_1_3', 'suite_crit_extra_relevant_test_case_rate', 1, 3, 'extra_mostly_irrelevant', 'Дополнительные ТК в основном нерелевантны или искажают требования.'),
    ('suite_qsl_extra_relevant_0', 'suite_crit_extra_relevant_test_case_rate', 0, 0, 'extra_invalid', 'Дополнительные ТК полностью нерелевантны, дублируют или содержат неподтвержденные факты.'),

    ('suite_qsl_irrelevant_10', 'suite_crit_irrelevant_test_case_rate', 10, 10, 'no_irrelevant_tests', 'В наборе нет ТК, не связанных с требованиями.'),
    ('suite_qsl_irrelevant_8_9', 'suite_crit_irrelevant_test_case_rate', 8, 9, 'minor_irrelevant_tests', 'Есть единичные слабосвязанные ТК без значимого влияния.'),
    ('suite_qsl_irrelevant_6_7', 'suite_crit_irrelevant_test_case_rate', 6, 7, 'some_irrelevant_tests', 'Есть заметная доля нерелевантных ТК, но основа набора полезна.'),
    ('suite_qsl_irrelevant_4_5', 'suite_crit_irrelevant_test_case_rate', 4, 5, 'many_irrelevant_tests', 'Нерелевантные ТК существенно загрязняют набор.'),
    ('suite_qsl_irrelevant_1_3', 'suite_crit_irrelevant_test_case_rate', 1, 3, 'mostly_irrelevant_tests', 'Большинство ТК не связано с требованиями.'),
    ('suite_qsl_irrelevant_0', 'suite_crit_irrelevant_test_case_rate', 0, 0, 'irrelevant_set', 'Набор фактически не относится к проверяемым требованиям.'),

    ('suite_qsl_coverage_balance_10', 'suite_crit_coverage_balance', 10, 10, 'balanced', 'Покрытие распределено по требованиям без перекосов и искусственного раздувания отдельных требований.'),
    ('suite_qsl_coverage_balance_8_9', 'suite_crit_coverage_balance', 8, 9, 'mostly_balanced', 'Есть minor-перекосы, но покрытие в целом равномерное.'),
    ('suite_qsl_coverage_balance_6_7', 'suite_crit_coverage_balance', 6, 7, 'partly_balanced', 'Есть заметные перекосы между требованиями.'),
    ('suite_qsl_coverage_balance_4_5', 'suite_crit_coverage_balance', 4, 5, 'unbalanced', 'Часть требований перегружена ТК, часть недопокрыта.'),
    ('suite_qsl_coverage_balance_1_3', 'suite_crit_coverage_balance', 1, 3, 'strongly_unbalanced', 'Покрытие сильно сосредоточено на малой части требований.'),
    ('suite_qsl_coverage_balance_0', 'suite_crit_coverage_balance', 0, 0, 'no_balance', 'Распределение покрытия непригодно для оценки набора.'),

    ('suite_qsl_overall_completeness_10', 'suite_crit_overall_completeness', 10, 10, 'complete_suite', 'Набор достаточен для проверяемого скоупа и закрывает основные ожидаемые сценарии.'),
    ('suite_qsl_overall_completeness_8_9', 'suite_crit_overall_completeness', 8, 9, 'mostly_complete_suite', 'Набор почти достаточен, есть minor-пропуски.'),
    ('suite_qsl_overall_completeness_6_7', 'suite_crit_overall_completeness', 6, 7, 'partly_complete_suite', 'Набор покрывает основу, но требует доработки.'),
    ('suite_qsl_overall_completeness_4_5', 'suite_crit_overall_completeness', 4, 5, 'incomplete_suite', 'Набор недостаточен для уверенной проверки скоупа.'),
    ('suite_qsl_overall_completeness_1_3', 'suite_crit_overall_completeness', 1, 3, 'severely_incomplete_suite', 'Набор почти не закрывает проверяемый скоуп.'),
    ('suite_qsl_overall_completeness_0', 'suite_crit_overall_completeness', 0, 0, 'empty_suite', 'Набор отсутствует или непригоден.'),

    ('suite_qsl_no_hallucinations_10', 'suite_crit_no_suite_level_hallucinations', 10, 10, 'no_hallucinations', 'Набор не содержит фактов, сценариев, ролей, UI-элементов или ограничений вне требований.'),
    ('suite_qsl_no_hallucinations_8_9', 'suite_crit_no_suite_level_hallucinations', 8, 9, 'minor_unsupported_details', 'Есть minor-детали, которые слабо подтверждены, но не меняют смысл проверки.'),
    ('suite_qsl_no_hallucinations_6_7', 'suite_crit_no_suite_level_hallucinations', 6, 7, 'some_unsupported_details', 'Есть неподтвержденные детали, часть ТК требует ревью.'),
    ('suite_qsl_no_hallucinations_4_5', 'suite_crit_no_suite_level_hallucinations', 4, 5, 'many_unsupported_details', 'Неподтвержденные детали заметно влияют на качество набора.'),
    ('suite_qsl_no_hallucinations_1_3', 'suite_crit_no_suite_level_hallucinations', 1, 3, 'hallucinated_suite', 'Набор содержит много выдуманных деталей или сценариев.'),
    ('suite_qsl_no_hallucinations_0', 'suite_crit_no_suite_level_hallucinations', 0, 0, 'invalid_hallucinated_suite', 'Набор непригоден из-за галлюцинаций.'),

    ('suite_qsl_insufficient_detail_10', 'suite_crit_insufficient_detail_handling', 10, 10, 'handled_correctly', 'По требованиям insufficient_detail не сгенерированы ТК с додуманными деталями; такие требования корректно исключены или помечены.'),
    ('suite_qsl_insufficient_detail_8_9', 'suite_crit_insufficient_detail_handling', 8, 9, 'mostly_handled', 'Обработка почти корректная, есть minor-спорные случаи.'),
    ('suite_qsl_insufficient_detail_6_7', 'suite_crit_insufficient_detail_handling', 6, 7, 'partly_handled', 'Часть недостаточно детализированных требований обработана корректно, часть требует ревью.'),
    ('suite_qsl_insufficient_detail_4_5', 'suite_crit_insufficient_detail_handling', 4, 5, 'weak_handling', 'Модель иногда генерирует ТК по недостаточным требованиям с допущениями.'),
    ('suite_qsl_insufficient_detail_1_3', 'suite_crit_insufficient_detail_handling', 1, 3, 'poor_handling', 'Модель часто генерирует ТК с додуманными деталями по insufficient_detail.'),
    ('suite_qsl_insufficient_detail_0', 'suite_crit_insufficient_detail_handling', 0, 0, 'not_handled', 'Статус insufficient_detail игнорируется.'),

    ('suite_qsl_multi_traceability_10', 'suite_crit_multi_requirement_traceability', 10, 10, 'fully_relevant_links', 'Каждый ТК, связанный с несколькими требованиями, релевантен каждому связанному требованию.'),
    ('suite_qsl_multi_traceability_8_9', 'suite_crit_multi_requirement_traceability', 8, 9, 'mostly_relevant_links', 'Связи почти все корректны, есть minor-спорные привязки.'),
    ('suite_qsl_multi_traceability_6_7', 'suite_crit_multi_requirement_traceability', 6, 7, 'partly_relevant_links', 'Часть many-to-many связей корректна, часть требует проверки.'),
    ('suite_qsl_multi_traceability_4_5', 'suite_crit_multi_requirement_traceability', 4, 5, 'weak_relevance_links', 'Есть заметное число ТК, привязанных к требованиям, которые они фактически не проверяют.'),
    ('suite_qsl_multi_traceability_1_3', 'suite_crit_multi_requirement_traceability', 1, 3, 'poor_relevance_links', 'Большинство many-to-many связей нерелевантны.'),
    ('suite_qsl_multi_traceability_0', 'suite_crit_multi_requirement_traceability', 0, 0, 'invalid_links', 'Связи ТК с несколькими требованиями непригодны или вводят в заблуждение.');
