PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS datasets (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    version TEXT NOT NULL,
    description TEXT,
    status TEXT NOT NULL DEFAULT 'draft',
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (name, version)
);

CREATE TABLE IF NOT EXISTS dataset_input_profiles (
    code TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    expected_behavior TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS dataset_profile_criterion_targets (
    id TEXT PRIMARY KEY,
    input_profile_code TEXT NOT NULL,
    criterion_group TEXT NOT NULL
        CHECK (criterion_group IN ('requirement', 'requirement_decomposition', 'test_suite', 'test_case')),
    criterion_code TEXT NOT NULL,
    target_score REAL CHECK (target_score IS NULL OR (target_score BETWEEN 0 AND 10)),
    target_display TEXT,
    target_description TEXT,
    is_active INTEGER NOT NULL DEFAULT 1,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (input_profile_code) REFERENCES dataset_input_profiles(code) ON DELETE CASCADE,
    UNIQUE (input_profile_code, criterion_group, criterion_code)
);

CREATE TABLE IF NOT EXISTS eval_runs (
    id TEXT PRIMARY KEY,
    dataset_id TEXT NOT NULL,
    run_code TEXT NOT NULL,
    agent_name TEXT NOT NULL CHECK (length(trim(agent_name)) > 0),
    agent_version TEXT NOT NULL CHECK (length(trim(agent_version)) > 0),
    prompt_snapshot TEXT NOT NULL CHECK (length(trim(prompt_snapshot)) > 0),
    model_name TEXT NOT NULL CHECK (length(trim(model_name)) > 0),
    model_version TEXT NOT NULL CHECK (length(trim(model_version)) > 0),
    temperature REAL NOT NULL CHECK (temperature >= 0),
    top_p REAL NOT NULL CHECK (top_p >= 0 AND top_p <= 1),
    run_mode TEXT NOT NULL DEFAULT 'direct_extraction'
        CHECK (run_mode IN ('direct_extraction', 'rag_search', 'hybrid')),
    retrieval_chunk_size INTEGER CHECK (retrieval_chunk_size IS NULL OR retrieval_chunk_size > 0),
    retrieval_top_k INTEGER CHECK (retrieval_top_k IS NULL OR retrieval_top_k >= 0),
    reranker_name TEXT,
    response_format_strictness TEXT NOT NULL DEFAULT 'strict'
        CHECK (response_format_strictness IN ('strict', 'medium', 'freeform')),
    response_contract_json TEXT,
    change_summary TEXT,
    dataset_version TEXT,
    started_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    finished_at TEXT,
    status TEXT NOT NULL DEFAULT 'started',
    FOREIGN KEY (dataset_id) REFERENCES datasets(id) ON DELETE CASCADE,
    UNIQUE (dataset_id, run_code)
);

CREATE TABLE IF NOT EXISTS dataset_cases (
    id TEXT PRIMARY KEY,
    dataset_id TEXT NOT NULL,
    case_code TEXT NOT NULL,
    title TEXT NOT NULL,
    description TEXT,
    case_type TEXT NOT NULL DEFAULT 'manual',
    input_profile_code TEXT,
    input_profile_name TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (dataset_id) REFERENCES datasets(id) ON DELETE CASCADE,
    FOREIGN KEY (input_profile_code) REFERENCES dataset_input_profiles(code) ON DELETE SET NULL,
    UNIQUE (dataset_id, case_code)
);

CREATE TABLE IF NOT EXISTS dataset_case_criterion_targets (
    id TEXT PRIMARY KEY,
    dataset_case_id TEXT NOT NULL,
    criterion_group TEXT NOT NULL
        CHECK (criterion_group IN ('requirement', 'requirement_decomposition', 'test_suite', 'test_case')),
    criterion_code TEXT NOT NULL,
    target_score REAL CHECK (target_score IS NULL OR (target_score BETWEEN 0 AND 10)),
    target_display TEXT,
    target_description TEXT,
    is_active INTEGER NOT NULL DEFAULT 1,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (dataset_case_id) REFERENCES dataset_cases(id) ON DELETE CASCADE,
    UNIQUE (dataset_case_id, criterion_group, criterion_code)
);

CREATE TABLE IF NOT EXISTS source_materials (
    id TEXT PRIMARY KEY,
    dataset_case_id TEXT NOT NULL,
    source_type TEXT NOT NULL,
    source_name TEXT,
    source_version TEXT,
    raw_text TEXT,
    metadata_json TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (dataset_case_id) REFERENCES dataset_cases(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS source_fragments (
    id TEXT PRIMARY KEY,
    source_material_id TEXT NOT NULL,
    fragment_ref TEXT NOT NULL,
    fragment_text TEXT NOT NULL,
    FOREIGN KEY (source_material_id) REFERENCES source_materials(id) ON DELETE CASCADE,
    UNIQUE (source_material_id, fragment_ref)
);

CREATE TABLE IF NOT EXISTS input_requirements (
    id TEXT PRIMARY KEY,
    dataset_case_id TEXT NOT NULL,
    input_requirement_code TEXT NOT NULL,
    title TEXT,
    requirement_text TEXT NOT NULL,
    source_fragment_id TEXT,
    requirement_order INTEGER,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (dataset_case_id) REFERENCES dataset_cases(id) ON DELETE CASCADE,
    FOREIGN KEY (source_fragment_id) REFERENCES source_fragments(id) ON DELETE SET NULL,
    UNIQUE (dataset_case_id, input_requirement_code)
);

CREATE TABLE IF NOT EXISTS requirements (
    id TEXT PRIMARY KEY,
    dataset_case_id TEXT NOT NULL,
    requirement_code TEXT NOT NULL,
    requirement_text TEXT NOT NULL,
    origin TEXT NOT NULL DEFAULT 'expected',
    expected_status TEXT NOT NULL DEFAULT 'ready_for_generation',
    quality_profile_status TEXT,
    risk_level TEXT,
    is_ready_for_generation INTEGER NOT NULL DEFAULT 1,
    eval_run_id TEXT,
    comment TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (dataset_case_id) REFERENCES dataset_cases(id) ON DELETE CASCADE,
    FOREIGN KEY (eval_run_id) REFERENCES eval_runs(id) ON DELETE SET NULL,
    UNIQUE (dataset_case_id, requirement_code, origin)
);

CREATE TABLE IF NOT EXISTS input_requirement_decomposition_links (
    id TEXT PRIMARY KEY,
    input_requirement_id TEXT NOT NULL,
    requirement_id TEXT NOT NULL,
    link_type TEXT NOT NULL DEFAULT 'expected_atomic_requirement',
    rationale TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (input_requirement_id) REFERENCES input_requirements(id) ON DELETE CASCADE,
    FOREIGN KEY (requirement_id) REFERENCES requirements(id) ON DELETE CASCADE,
    UNIQUE (input_requirement_id, requirement_id, link_type)
);

CREATE TABLE IF NOT EXISTS requirement_decomposition_evaluation_results (
    id TEXT PRIMARY KEY,
    eval_run_id TEXT NOT NULL,
    dataset_case_id TEXT NOT NULL,
    input_requirement_id TEXT NOT NULL,
    generated_requirement_id TEXT,
    matched_expected_requirement_id TEXT,
    match_status TEXT NOT NULL DEFAULT 'not_evaluated',
    boundary_status TEXT NOT NULL DEFAULT 'not_evaluated',
    traceability_status TEXT NOT NULL DEFAULT 'not_evaluated',
    unsupported_detail_count INTEGER NOT NULL DEFAULT 0,
    score REAL CHECK (score IS NULL OR (score BETWEEN 0 AND 10)),
    severity TEXT NOT NULL DEFAULT 'info',
    evaluator_name TEXT NOT NULL DEFAULT 'unknown',
    evaluator_type TEXT NOT NULL DEFAULT 'manual',
    rationale TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (eval_run_id) REFERENCES eval_runs(id) ON DELETE CASCADE,
    FOREIGN KEY (dataset_case_id) REFERENCES dataset_cases(id) ON DELETE CASCADE,
    FOREIGN KEY (input_requirement_id) REFERENCES input_requirements(id) ON DELETE CASCADE,
    FOREIGN KEY (generated_requirement_id) REFERENCES requirements(id) ON DELETE CASCADE,
    FOREIGN KEY (matched_expected_requirement_id) REFERENCES requirements(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS requirement_decomposition_quality_criteria (
    id TEXT PRIMARY KEY,
    code TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL,
    description TEXT,
    scale_min INTEGER NOT NULL DEFAULT 0,
    scale_max INTEGER NOT NULL DEFAULT 10,
    target_score REAL CHECK (target_score IS NULL OR (target_score BETWEEN 0 AND 10)),
    target_display TEXT,
    target_description TEXT,
    is_active INTEGER NOT NULL DEFAULT 1
);

CREATE TABLE IF NOT EXISTS requirement_decomposition_quality_criterion_score_levels (
    id TEXT PRIMARY KEY,
    criterion_id TEXT NOT NULL,
    score_min INTEGER NOT NULL CHECK (score_min BETWEEN 0 AND 10),
    score_max INTEGER NOT NULL CHECK (score_max BETWEEN 0 AND 10),
    label TEXT NOT NULL,
    description TEXT NOT NULL,
    FOREIGN KEY (criterion_id) REFERENCES requirement_decomposition_quality_criteria(id) ON DELETE CASCADE,
    CHECK (score_min <= score_max),
    UNIQUE (criterion_id, score_min, score_max)
);

CREATE TABLE IF NOT EXISTS requirement_decomposition_quality_assessments (
    id TEXT PRIMARY KEY,
    decomposition_evaluation_result_id TEXT NOT NULL,
    criterion_id TEXT NOT NULL,
    score REAL NOT NULL CHECK (score BETWEEN 0 AND 10),
    label TEXT NOT NULL,
    rationale TEXT,
    assessed_by TEXT NOT NULL DEFAULT 'unknown',
    assessment_method TEXT NOT NULL DEFAULT 'human',
    confidence REAL CHECK (confidence IS NULL OR (confidence >= 0 AND confidence <= 1)),
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (decomposition_evaluation_result_id)
        REFERENCES requirement_decomposition_evaluation_results(id) ON DELETE CASCADE,
    FOREIGN KEY (criterion_id) REFERENCES requirement_decomposition_quality_criteria(id) ON DELETE RESTRICT,
    UNIQUE (decomposition_evaluation_result_id, criterion_id)
);

CREATE TABLE IF NOT EXISTS requirement_source_links (
    id TEXT PRIMARY KEY,
    requirement_id TEXT NOT NULL,
    source_fragment_id TEXT NOT NULL,
    link_type TEXT NOT NULL DEFAULT 'derived_from',
    rationale TEXT,
    FOREIGN KEY (requirement_id) REFERENCES requirements(id) ON DELETE CASCADE,
    FOREIGN KEY (source_fragment_id) REFERENCES source_fragments(id) ON DELETE CASCADE,
    UNIQUE (requirement_id, source_fragment_id, link_type)
);

CREATE TABLE IF NOT EXISTS requirement_quality_criteria (
    id TEXT PRIMARY KEY,
    code TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL,
    description TEXT,
    scale_min INTEGER NOT NULL DEFAULT 0,
    scale_max INTEGER NOT NULL DEFAULT 10,
    target_score REAL CHECK (target_score IS NULL OR (target_score BETWEEN 0 AND 10)),
    target_display TEXT,
    target_description TEXT,
    is_active INTEGER NOT NULL DEFAULT 1
);

CREATE TABLE IF NOT EXISTS requirement_quality_criterion_score_levels (
    id TEXT PRIMARY KEY,
    criterion_id TEXT NOT NULL,
    score_min INTEGER NOT NULL CHECK (score_min BETWEEN 0 AND 10),
    score_max INTEGER NOT NULL CHECK (score_max BETWEEN 0 AND 10),
    label TEXT NOT NULL,
    description TEXT NOT NULL,
    FOREIGN KEY (criterion_id) REFERENCES requirement_quality_criteria(id) ON DELETE CASCADE,
    CHECK (score_min <= score_max),
    UNIQUE (criterion_id, score_min, score_max)
);

CREATE TABLE IF NOT EXISTS requirement_quality_assessments (
    id TEXT PRIMARY KEY,
    requirement_id TEXT NOT NULL,
    criterion_id TEXT NOT NULL,
    score REAL NOT NULL CHECK (score BETWEEN 0 AND 10),
    label TEXT NOT NULL,
    rationale TEXT,
    assessed_by TEXT NOT NULL DEFAULT 'unknown',
    assessment_method TEXT NOT NULL DEFAULT 'human',
    confidence REAL CHECK (confidence IS NULL OR (confidence >= 0 AND confidence <= 1)),
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (requirement_id) REFERENCES requirements(id) ON DELETE CASCADE,
    FOREIGN KEY (criterion_id) REFERENCES requirement_quality_criteria(id) ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS test_cases (
    id TEXT PRIMARY KEY,
    dataset_case_id TEXT NOT NULL,
    test_case_code TEXT NOT NULL,
    title TEXT NOT NULL,
    test_case_type TEXT,
    direction TEXT,
    origin TEXT NOT NULL DEFAULT 'expected',
    preconditions TEXT,
    postconditions TEXT,
    eval_run_id TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (dataset_case_id) REFERENCES dataset_cases(id) ON DELETE CASCADE,
    FOREIGN KEY (eval_run_id) REFERENCES eval_runs(id) ON DELETE SET NULL,
    UNIQUE (dataset_case_id, test_case_code, origin)
);

CREATE TABLE IF NOT EXISTS test_case_steps (
    id TEXT PRIMARY KEY,
    test_case_id TEXT NOT NULL,
    step_number INTEGER NOT NULL,
    action TEXT NOT NULL,
    expected_result TEXT NOT NULL,
    FOREIGN KEY (test_case_id) REFERENCES test_cases(id) ON DELETE CASCADE,
    UNIQUE (test_case_id, step_number)
);

CREATE TABLE IF NOT EXISTS test_case_quality_criteria (
    id TEXT PRIMARY KEY,
    code TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL,
    description TEXT,
    scale_min INTEGER NOT NULL DEFAULT 0,
    scale_max INTEGER NOT NULL DEFAULT 10,
    target_score REAL CHECK (target_score IS NULL OR (target_score BETWEEN 0 AND 10)),
    target_display TEXT,
    target_description TEXT,
    is_active INTEGER NOT NULL DEFAULT 1
);

CREATE TABLE IF NOT EXISTS test_case_quality_criterion_score_levels (
    id TEXT PRIMARY KEY,
    criterion_id TEXT NOT NULL,
    score_min INTEGER NOT NULL CHECK (score_min BETWEEN 0 AND 10),
    score_max INTEGER NOT NULL CHECK (score_max BETWEEN 0 AND 10),
    label TEXT NOT NULL,
    description TEXT NOT NULL,
    FOREIGN KEY (criterion_id) REFERENCES test_case_quality_criteria(id) ON DELETE CASCADE,
    CHECK (score_min <= score_max),
    UNIQUE (criterion_id, score_min, score_max)
);

CREATE TABLE IF NOT EXISTS test_case_quality_assessments (
    id TEXT PRIMARY KEY,
    test_case_id TEXT NOT NULL,
    criterion_id TEXT NOT NULL,
    score REAL NOT NULL CHECK (score BETWEEN 0 AND 10),
    label TEXT NOT NULL,
    rationale TEXT,
    assessed_by TEXT NOT NULL DEFAULT 'unknown',
    assessment_method TEXT NOT NULL DEFAULT 'human',
    confidence REAL CHECK (confidence IS NULL OR (confidence >= 0 AND confidence <= 1)),
    eval_run_id TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (test_case_id) REFERENCES test_cases(id) ON DELETE CASCADE,
    FOREIGN KEY (criterion_id) REFERENCES test_case_quality_criteria(id) ON DELETE RESTRICT,
    FOREIGN KEY (eval_run_id) REFERENCES eval_runs(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS test_suite_quality_criteria (
    id TEXT PRIMARY KEY,
    code TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL,
    description TEXT,
    scale_min INTEGER NOT NULL DEFAULT 0,
    scale_max INTEGER NOT NULL DEFAULT 10,
    target_score REAL CHECK (target_score IS NULL OR (target_score BETWEEN 0 AND 10)),
    target_display TEXT,
    target_description TEXT,
    is_active INTEGER NOT NULL DEFAULT 1
);

CREATE TABLE IF NOT EXISTS test_suite_quality_criterion_score_levels (
    id TEXT PRIMARY KEY,
    criterion_id TEXT NOT NULL,
    score_min INTEGER NOT NULL CHECK (score_min BETWEEN 0 AND 10),
    score_max INTEGER NOT NULL CHECK (score_max BETWEEN 0 AND 10),
    label TEXT NOT NULL,
    description TEXT NOT NULL,
    FOREIGN KEY (criterion_id) REFERENCES test_suite_quality_criteria(id) ON DELETE CASCADE,
    CHECK (score_min <= score_max),
    UNIQUE (criterion_id, score_min, score_max)
);

CREATE TABLE IF NOT EXISTS test_suite_quality_assessments (
    id TEXT PRIMARY KEY,
    criterion_id TEXT NOT NULL,
    scope_type TEXT NOT NULL,
    scope_id TEXT NOT NULL,
    dataset_id TEXT,
    dataset_case_id TEXT,
    requirement_id TEXT,
    eval_run_id TEXT,
    score REAL NOT NULL CHECK (score BETWEEN 0 AND 10),
    label TEXT NOT NULL,
    rationale TEXT,
    assessed_by TEXT NOT NULL DEFAULT 'unknown',
    assessment_method TEXT NOT NULL DEFAULT 'human',
    confidence REAL CHECK (confidence IS NULL OR (confidence >= 0 AND confidence <= 1)),
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (criterion_id) REFERENCES test_suite_quality_criteria(id) ON DELETE RESTRICT,
    FOREIGN KEY (dataset_id) REFERENCES datasets(id) ON DELETE CASCADE,
    FOREIGN KEY (dataset_case_id) REFERENCES dataset_cases(id) ON DELETE CASCADE,
    FOREIGN KEY (requirement_id) REFERENCES requirements(id) ON DELETE CASCADE,
    FOREIGN KEY (eval_run_id) REFERENCES eval_runs(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS requirement_test_case_links (
    id TEXT PRIMARY KEY,
    requirement_id TEXT NOT NULL,
    test_case_id TEXT NOT NULL,
    coverage_status TEXT NOT NULL DEFAULT 'covered',
    coverage_type TEXT,
    is_primary INTEGER NOT NULL DEFAULT 0,
    rationale TEXT,
    linked_by TEXT NOT NULL DEFAULT 'unknown',
    review_status TEXT NOT NULL DEFAULT 'draft',
    FOREIGN KEY (requirement_id) REFERENCES requirements(id) ON DELETE CASCADE,
    FOREIGN KEY (test_case_id) REFERENCES test_cases(id) ON DELETE CASCADE,
    UNIQUE (requirement_id, test_case_id, coverage_type)
);

CREATE TABLE IF NOT EXISTS test_case_step_requirement_links (
    id TEXT PRIMARY KEY,
    test_case_step_id TEXT NOT NULL,
    requirement_id TEXT NOT NULL,
    source_fragment_id TEXT,
    rationale TEXT,
    linked_by TEXT NOT NULL DEFAULT 'unknown',
    review_status TEXT NOT NULL DEFAULT 'draft',
    FOREIGN KEY (test_case_step_id) REFERENCES test_case_steps(id) ON DELETE CASCADE,
    FOREIGN KEY (requirement_id) REFERENCES requirements(id) ON DELETE CASCADE,
    FOREIGN KEY (source_fragment_id) REFERENCES source_fragments(id) ON DELETE SET NULL,
    UNIQUE (test_case_step_id, requirement_id)
);

CREATE TABLE IF NOT EXISTS unsupported_details (
    id TEXT PRIMARY KEY,
    test_case_id TEXT NOT NULL,
    test_case_step_id TEXT,
    detail_text TEXT NOT NULL,
    detail_type TEXT,
    reason TEXT,
    severity TEXT NOT NULL DEFAULT 'minor',
    review_status TEXT NOT NULL DEFAULT 'draft',
    FOREIGN KEY (test_case_id) REFERENCES test_cases(id) ON DELETE CASCADE,
    FOREIGN KEY (test_case_step_id) REFERENCES test_case_steps(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS test_case_evaluation_results (
    id TEXT PRIMARY KEY,
    eval_run_id TEXT NOT NULL,
    dataset_case_id TEXT NOT NULL,
    generated_test_case_id TEXT NOT NULL,
    matched_expected_test_case_id TEXT,
    match_status TEXT NOT NULL DEFAULT 'not_evaluated',
    structure_status TEXT NOT NULL DEFAULT 'not_evaluated',
    classification_status TEXT NOT NULL DEFAULT 'not_evaluated',
    hallucination_status TEXT NOT NULL DEFAULT 'not_evaluated',
    unsupported_detail_count INTEGER NOT NULL DEFAULT 0,
    score REAL CHECK (score IS NULL OR (score >= 0 AND score <= 1)),
    severity TEXT NOT NULL DEFAULT 'info',
    evaluator_name TEXT NOT NULL DEFAULT 'unknown',
    evaluator_type TEXT NOT NULL DEFAULT 'manual',
    rationale TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (eval_run_id) REFERENCES eval_runs(id) ON DELETE CASCADE,
    FOREIGN KEY (dataset_case_id) REFERENCES dataset_cases(id) ON DELETE CASCADE,
    FOREIGN KEY (generated_test_case_id) REFERENCES test_cases(id) ON DELETE CASCADE,
    FOREIGN KEY (matched_expected_test_case_id) REFERENCES test_cases(id) ON DELETE SET NULL,
    UNIQUE (eval_run_id, generated_test_case_id)
);

CREATE TABLE IF NOT EXISTS external_reviews (
    id TEXT PRIMARY KEY,
    dataset_id TEXT NOT NULL,
    dataset_case_id TEXT,
    reviewer_name TEXT NOT NULL,
    reviewer_type TEXT NOT NULL DEFAULT 'llm',
    model_name TEXT,
    prompt_version TEXT,
    review_status TEXT NOT NULL DEFAULT 'draft',
    summary TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    metadata_json TEXT,
    FOREIGN KEY (dataset_id) REFERENCES datasets(id) ON DELETE CASCADE,
    FOREIGN KEY (dataset_case_id) REFERENCES dataset_cases(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS external_requirement_assessment_reviews (
    id TEXT PRIMARY KEY,
    external_review_id TEXT NOT NULL,
    requirement_id TEXT NOT NULL,
    criterion_id TEXT NOT NULL,
    original_assessment_id TEXT,
    original_score REAL,
    reviewer_score REAL CHECK (reviewer_score IS NULL OR reviewer_score BETWEEN 0 AND 10),
    reviewer_label TEXT,
    agreement_status TEXT NOT NULL,
    reviewer_comment TEXT,
    severity TEXT NOT NULL DEFAULT 'info',
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (external_review_id) REFERENCES external_reviews(id) ON DELETE CASCADE,
    FOREIGN KEY (requirement_id) REFERENCES requirements(id) ON DELETE CASCADE,
    FOREIGN KEY (criterion_id) REFERENCES requirement_quality_criteria(id) ON DELETE RESTRICT,
    FOREIGN KEY (original_assessment_id) REFERENCES requirement_quality_assessments(id) ON DELETE SET NULL,
    UNIQUE (external_review_id, requirement_id, criterion_id)
);

CREATE TABLE IF NOT EXISTS external_test_case_reviews (
    id TEXT PRIMARY KEY,
    external_review_id TEXT NOT NULL,
    test_case_id TEXT NOT NULL,
    requirement_id TEXT,
    agreement_status TEXT NOT NULL,
    reviewer_comment TEXT,
    severity TEXT NOT NULL DEFAULT 'info',
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (external_review_id) REFERENCES external_reviews(id) ON DELETE CASCADE,
    FOREIGN KEY (test_case_id) REFERENCES test_cases(id) ON DELETE CASCADE,
    FOREIGN KEY (requirement_id) REFERENCES requirements(id) ON DELETE SET NULL
);

CREATE INDEX IF NOT EXISTS idx_dataset_cases_dataset_id ON dataset_cases(dataset_id);
CREATE INDEX IF NOT EXISTS idx_dataset_cases_input_profile ON dataset_cases(input_profile_code);
CREATE INDEX IF NOT EXISTS idx_dataset_profile_targets_profile
    ON dataset_profile_criterion_targets(input_profile_code, criterion_group, criterion_code);
CREATE INDEX IF NOT EXISTS idx_dataset_case_targets_case
    ON dataset_case_criterion_targets(dataset_case_id, criterion_group, criterion_code);
CREATE INDEX IF NOT EXISTS idx_sources_case_id ON source_materials(dataset_case_id);
CREATE INDEX IF NOT EXISTS idx_fragments_source_id ON source_fragments(source_material_id);
CREATE INDEX IF NOT EXISTS idx_input_requirements_case_id ON input_requirements(dataset_case_id);
CREATE INDEX IF NOT EXISTS idx_requirements_case_id ON requirements(dataset_case_id);
CREATE INDEX IF NOT EXISTS idx_input_req_decomp_input_id ON input_requirement_decomposition_links(input_requirement_id);
CREATE INDEX IF NOT EXISTS idx_input_req_decomp_req_id ON input_requirement_decomposition_links(requirement_id);
CREATE INDEX IF NOT EXISTS idx_req_decomp_eval_run_id ON requirement_decomposition_evaluation_results(eval_run_id);
CREATE INDEX IF NOT EXISTS idx_req_decomp_eval_input_id ON requirement_decomposition_evaluation_results(input_requirement_id);
CREATE INDEX IF NOT EXISTS idx_req_decomp_eval_generated_req_id ON requirement_decomposition_evaluation_results(generated_requirement_id);
CREATE INDEX IF NOT EXISTS idx_req_decomp_eval_expected_req_id ON requirement_decomposition_evaluation_results(matched_expected_requirement_id);
CREATE INDEX IF NOT EXISTS idx_req_decomp_quality_score_levels_criterion_id
    ON requirement_decomposition_quality_criterion_score_levels(criterion_id);
CREATE INDEX IF NOT EXISTS idx_req_decomp_quality_assessments_result_id
    ON requirement_decomposition_quality_assessments(decomposition_evaluation_result_id);
CREATE INDEX IF NOT EXISTS idx_req_decomp_quality_assessments_criterion_id
    ON requirement_decomposition_quality_assessments(criterion_id);
CREATE INDEX IF NOT EXISTS idx_requirement_source_req_id ON requirement_source_links(requirement_id);
CREATE INDEX IF NOT EXISTS idx_req_quality_score_levels_criterion_id ON requirement_quality_criterion_score_levels(criterion_id);
CREATE INDEX IF NOT EXISTS idx_requirement_quality_req_id ON requirement_quality_assessments(requirement_id);
CREATE INDEX IF NOT EXISTS idx_test_cases_case_id ON test_cases(dataset_case_id);
CREATE INDEX IF NOT EXISTS idx_test_steps_tc_id ON test_case_steps(test_case_id);
CREATE INDEX IF NOT EXISTS idx_tc_quality_score_levels_criterion_id ON test_case_quality_criterion_score_levels(criterion_id);
CREATE INDEX IF NOT EXISTS idx_tc_quality_assessments_tc_id ON test_case_quality_assessments(test_case_id);
CREATE INDEX IF NOT EXISTS idx_tc_quality_assessments_criterion_id ON test_case_quality_assessments(criterion_id);
CREATE INDEX IF NOT EXISTS idx_suite_quality_score_levels_criterion_id ON test_suite_quality_criterion_score_levels(criterion_id);
CREATE INDEX IF NOT EXISTS idx_suite_quality_assessments_scope ON test_suite_quality_assessments(scope_type, scope_id);
CREATE INDEX IF NOT EXISTS idx_suite_quality_assessments_case_id ON test_suite_quality_assessments(dataset_case_id);
CREATE INDEX IF NOT EXISTS idx_suite_quality_assessments_requirement_id ON test_suite_quality_assessments(requirement_id);
CREATE INDEX IF NOT EXISTS idx_suite_quality_assessments_run_id ON test_suite_quality_assessments(eval_run_id);
CREATE INDEX IF NOT EXISTS idx_eval_runs_agent ON eval_runs(agent_name, agent_version);
CREATE INDEX IF NOT EXISTS idx_eval_runs_model ON eval_runs(model_name, model_version);
CREATE INDEX IF NOT EXISTS idx_eval_runs_mode ON eval_runs(run_mode);
CREATE INDEX IF NOT EXISTS idx_req_tc_req_id ON requirement_test_case_links(requirement_id);
CREATE INDEX IF NOT EXISTS idx_req_tc_tc_id ON requirement_test_case_links(test_case_id);
CREATE INDEX IF NOT EXISTS idx_step_req_step_id ON test_case_step_requirement_links(test_case_step_id);
CREATE INDEX IF NOT EXISTS idx_tc_eval_results_run_id ON test_case_evaluation_results(eval_run_id);
CREATE INDEX IF NOT EXISTS idx_tc_eval_results_generated_tc_id ON test_case_evaluation_results(generated_test_case_id);
CREATE INDEX IF NOT EXISTS idx_tc_eval_results_case_id ON test_case_evaluation_results(dataset_case_id);
CREATE INDEX IF NOT EXISTS idx_external_reviews_dataset_id ON external_reviews(dataset_id);
CREATE INDEX IF NOT EXISTS idx_external_req_reviews_review_id ON external_requirement_assessment_reviews(external_review_id);
CREATE INDEX IF NOT EXISTS idx_external_req_reviews_requirement_id ON external_requirement_assessment_reviews(requirement_id);
CREATE INDEX IF NOT EXISTS idx_external_tc_reviews_review_id ON external_test_case_reviews(external_review_id);

CREATE VIEW IF NOT EXISTS requirement_source_summary AS
SELECT
    d.id AS dataset_id,
    d.name AS dataset_name,
    d.version AS dataset_version,
    dc.id AS dataset_case_id,
    dc.case_code,
    r.id AS requirement_id,
    r.requirement_code,
    r.origin,
    COUNT(DISTINCT rsl.source_fragment_id) AS source_fragment_count,
    COUNT(DISTINCT sf.source_material_id) AS source_material_count
FROM requirements r
JOIN dataset_cases dc ON dc.id = r.dataset_case_id
JOIN datasets d ON d.id = dc.dataset_id
LEFT JOIN requirement_source_links rsl ON rsl.requirement_id = r.id
LEFT JOIN source_fragments sf ON sf.id = rsl.source_fragment_id
GROUP BY d.id, dc.id, r.id;

CREATE VIEW IF NOT EXISTS dataset_case_requirement_source_profile AS
SELECT
    dataset_id,
    dataset_name,
    dataset_version,
    dataset_case_id,
    case_code,
    COUNT(*) AS requirement_count,
    ROUND(AVG(source_material_count), 2) AS avg_source_materials_per_requirement,
    MAX(source_material_count) AS max_source_materials_per_requirement,
    SUM(CASE WHEN source_material_count = 0 THEN 1 ELSE 0 END) AS no_source_requirements,
    SUM(CASE WHEN source_material_count = 1 THEN 1 ELSE 0 END) AS single_source_requirements,
    SUM(CASE WHEN source_material_count > 1 THEN 1 ELSE 0 END) AS multi_source_requirements
FROM requirement_source_summary
GROUP BY dataset_id, dataset_case_id;
