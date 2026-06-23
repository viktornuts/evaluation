UPDATE requirement_decomposition_quality_criteria
SET
    target_score = 10.0,
    target_display = CASE code
        WHEN 'decomposition_completeness' THEN '10 / 100%'
        WHEN 'decomposition_boundaries' THEN '10 / корректные границы'
        WHEN 'requirement_consolidation' THEN '10 / без дублей и потери смысла'
    END,
    target_description = CASE code
        WHEN 'decomposition_completeness' THEN 'Все значимые атомарные требования из эталона выделены.'
        WHEN 'decomposition_boundaries' THEN 'Границы атомарных требований соответствуют эталонной разметке.'
        WHEN 'requirement_consolidation' THEN 'Связанная информация объединена корректно, без дублей, противоречий и потери смысла.'
    END
WHERE code IN ('decomposition_completeness', 'decomposition_boundaries', 'requirement_consolidation');

UPDATE requirement_quality_criteria
SET
    target_score = 10.0,
    target_display = CASE code
        WHEN 'source_quality' THEN '10 / подтвержденный источник'
        WHEN 'completeness' THEN '10 / полное требование'
        WHEN 'consistency' THEN '10 / без противоречий'
        WHEN 'correctness' THEN '10 / корректно'
        WHEN 'unambiguity' THEN '10 / однозначно'
        WHEN 'testability' THEN '10 / проверяемо'
        WHEN 'traceability' THEN '10 / трассируемо'
        WHEN 'modifiability' THEN '10 / поддерживаемо'
        WHEN 'atomicity' THEN '10 / атомарно'
        WHEN 'feasibility' THEN '10 / выполнимо'
    END,
    target_description = CASE code
        WHEN 'source_quality' THEN 'Требование подтверждено надежным источником и имеет понятное происхождение.'
        WHEN 'completeness' THEN 'Требование содержит всю информацию, необходимую для генерации и проверки.'
        WHEN 'consistency' THEN 'Требование не конфликтует с собой, другими требованиями и ограничениями.'
        WHEN 'correctness' THEN 'Требование отражает реальную потребность и не искажает смысл источника.'
        WHEN 'unambiguity' THEN 'Требование допускает одну интерпретацию.'
        WHEN 'testability' THEN 'Для требования можно сформировать проверяемые pass/fail условия.'
        WHEN 'traceability' THEN 'Требование связано с исходным материалом или фрагментом источника.'
        WHEN 'modifiability' THEN 'Требование можно изменять без неконтролируемого влияния на другие требования.'
        WHEN 'atomicity' THEN 'Требование описывает одну проверяемую функцию или поведение.'
        WHEN 'feasibility' THEN 'Требование технологически реализуемо и не содержит технических противоречий.'
    END
WHERE code IN (
    'source_quality',
    'completeness',
    'consistency',
    'correctness',
    'unambiguity',
    'testability',
    'traceability',
    'modifiability',
    'atomicity',
    'feasibility'
);

UPDATE test_suite_quality_criteria
SET
    target_score = 10.0,
    target_display = CASE code
        WHEN 'positive_coverage' THEN '10 / 100%'
        WHEN 'negative_coverage' THEN '10 / 100% где применимо'
        WHEN 'suite_cleanliness' THEN '10 / 0 лишних'
        WHEN 'required_checks_coverage' THEN '10 / 100%'
        WHEN 'overall_completeness' THEN '10 / достаточно для scope'
    END,
    target_description = CASE code
        WHEN 'positive_coverage' THEN 'Все требования, где нужен позитивный сценарий, покрыты релевантными позитивными ТК.'
        WHEN 'negative_coverage' THEN 'Все требования, где нужны негативные сценарии, покрыты релевантными негативными ТК.'
        WHEN 'suite_cleanliness' THEN 'В наборе нет лишних, нерелевантных и дублирующих тест-кейсов.'
        WHEN 'required_checks_coverage' THEN 'Все обязательные проверки из требований или эталона покрыты.'
        WHEN 'overall_completeness' THEN 'Набор достаточен для проверяемого scope и закрывает основные ожидаемые сценарии.'
    END
WHERE code IN (
    'positive_coverage',
    'negative_coverage',
    'suite_cleanliness',
    'required_checks_coverage',
    'overall_completeness'
);

UPDATE test_case_quality_criteria
SET
    target_score = 10.0,
    target_display = CASE code
        WHEN 'classification_correctness' THEN '10 / вид ТК корректен'
        WHEN 'template_required_attributes' THEN '10 / 100% атрибутов'
        WHEN 'conditions_quality' THEN '10 / условия корректны'
        WHEN 'step_atomicity' THEN '10 / шаги атомарны'
        WHEN 'expected_result_quality' THEN '10 / ожидаемый результат у каждого шага'
        WHEN 'no_hallucinations' THEN '10 / 0 галлюцинаций'
    END,
    target_description = CASE code
        WHEN 'classification_correctness' THEN 'Вид ТК корректно определен как WEB/API/INT/E2E или другой применимый тип.'
        WHEN 'template_required_attributes' THEN 'ТК соответствует шаблону, обязательные атрибуты заполнены.'
        WHEN 'conditions_quality' THEN 'Предусловия и постусловия корректны и соответствуют сценарию.'
        WHEN 'step_atomicity' THEN 'Каждый шаг содержит одно действие или одну проверяемую операцию.'
        WHEN 'expected_result_quality' THEN 'У каждого шага есть конкретный проверяемый ожидаемый результат, соответствующий действию.'
        WHEN 'no_hallucinations' THEN 'ТК не содержит фактов, деталей или ограничений, отсутствующих в требованиях и источниках.'
    END
WHERE code IN (
    'classification_correctness',
    'template_required_attributes',
    'conditions_quality',
    'step_atomicity',
    'expected_result_quality',
    'no_hallucinations'
);
