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

CREATE TABLE IF NOT EXISTS eval_runs (
    id TEXT PRIMARY KEY,
    dataset_id TEXT NOT NULL,
    run_code TEXT NOT NULL,
    prompt_version TEXT,
    model_version TEXT,
    code_version TEXT,
    dataset_version TEXT,
    started_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    finished_at TEXT,
    status TEXT NOT NULL DEFAULT 'started',
    metadata_json TEXT,
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
    UNIQUE (dataset_id, case_code)
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

CREATE TABLE IF NOT EXISTS quality_criteria (
    id TEXT PRIMARY KEY,
    code TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL,
    description TEXT,
    scale_min INTEGER NOT NULL DEFAULT 1,
    scale_max INTEGER NOT NULL DEFAULT 5,
    is_active INTEGER NOT NULL DEFAULT 1
);

CREATE TABLE IF NOT EXISTS requirement_quality_assessments (
    id TEXT PRIMARY KEY,
    requirement_id TEXT NOT NULL,
    criterion_id TEXT NOT NULL,
    score INTEGER NOT NULL CHECK (score BETWEEN 1 AND 5),
    label TEXT NOT NULL,
    rationale TEXT,
    assessed_by TEXT NOT NULL DEFAULT 'unknown',
    assessment_method TEXT NOT NULL DEFAULT 'human',
    confidence REAL CHECK (confidence IS NULL OR (confidence >= 0 AND confidence <= 1)),
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (requirement_id) REFERENCES requirements(id) ON DELETE CASCADE,
    FOREIGN KEY (criterion_id) REFERENCES quality_criteria(id) ON DELETE RESTRICT
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
    scale_min INTEGER NOT NULL DEFAULT 1,
    scale_max INTEGER NOT NULL DEFAULT 5,
    is_active INTEGER NOT NULL DEFAULT 1
);

CREATE TABLE IF NOT EXISTS test_case_quality_assessments (
    id TEXT PRIMARY KEY,
    test_case_id TEXT NOT NULL,
    criterion_id TEXT NOT NULL,
    score INTEGER NOT NULL CHECK (score BETWEEN 1 AND 5),
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
    scale_min INTEGER NOT NULL DEFAULT 1,
    scale_max INTEGER NOT NULL DEFAULT 5,
    is_active INTEGER NOT NULL DEFAULT 1
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
    score INTEGER NOT NULL CHECK (score BETWEEN 1 AND 5),
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
    original_score INTEGER,
    reviewer_score INTEGER CHECK (reviewer_score IS NULL OR reviewer_score BETWEEN 1 AND 5),
    reviewer_label TEXT,
    agreement_status TEXT NOT NULL,
    reviewer_comment TEXT,
    severity TEXT NOT NULL DEFAULT 'info',
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (external_review_id) REFERENCES external_reviews(id) ON DELETE CASCADE,
    FOREIGN KEY (requirement_id) REFERENCES requirements(id) ON DELETE CASCADE,
    FOREIGN KEY (criterion_id) REFERENCES quality_criteria(id) ON DELETE RESTRICT,
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
CREATE INDEX IF NOT EXISTS idx_sources_case_id ON source_materials(dataset_case_id);
CREATE INDEX IF NOT EXISTS idx_fragments_source_id ON source_fragments(source_material_id);
CREATE INDEX IF NOT EXISTS idx_requirements_case_id ON requirements(dataset_case_id);
CREATE INDEX IF NOT EXISTS idx_requirement_source_req_id ON requirement_source_links(requirement_id);
CREATE INDEX IF NOT EXISTS idx_requirement_quality_req_id ON requirement_quality_assessments(requirement_id);
CREATE INDEX IF NOT EXISTS idx_test_cases_case_id ON test_cases(dataset_case_id);
CREATE INDEX IF NOT EXISTS idx_test_steps_tc_id ON test_case_steps(test_case_id);
CREATE INDEX IF NOT EXISTS idx_tc_quality_assessments_tc_id ON test_case_quality_assessments(test_case_id);
CREATE INDEX IF NOT EXISTS idx_tc_quality_assessments_criterion_id ON test_case_quality_assessments(criterion_id);
CREATE INDEX IF NOT EXISTS idx_suite_quality_assessments_scope ON test_suite_quality_assessments(scope_type, scope_id);
CREATE INDEX IF NOT EXISTS idx_suite_quality_assessments_case_id ON test_suite_quality_assessments(dataset_case_id);
CREATE INDEX IF NOT EXISTS idx_suite_quality_assessments_requirement_id ON test_suite_quality_assessments(requirement_id);
CREATE INDEX IF NOT EXISTS idx_suite_quality_assessments_run_id ON test_suite_quality_assessments(eval_run_id);
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
