# Notes From Source Documents

## Documents Added

- `source-documents/sfera-eval-strategy.pdf`
- `source-documents/2026-06-19 Eval-процесс разработки ЦПТ.pdf`
- `source-documents/Целевые_критерии_качества_работы_ЦПТ.docx`

## Main Product Context

The current documents describe evals for ЦПТ: a product that decomposes source materials into atomic requirements and generates test cases from those requirements.

The quality model has two main stages:

1. Quality of decomposition from source materials into atomic requirements.
2. Quality of test-case generation from atomic requirements.

This means the eval system should not only check the final generated test cases. It also needs to check the intermediate layer: extracted atomic requirements, their statuses, boundaries, consolidation, and traceability.

## Dataset Levels

The eval process document defines three dataset levels:

- Smoke dataset: 5-10 cases for fast local checks after prompt, code, RAG, chunking, reranker, or response-schema changes.
- Regression dataset: 50-150 cases for merge, demo, delivery, and regression tracking.
- Corner cases dataset: difficult cases, including incomplete requirements, insufficient detail, duplicate requirements across sources, mixed API/WEB/integration scenarios, ambiguous classification, and hallucination-prone cases.

## Minimum Dataset Example Contents

Each etalon dataset example should contain:

- source document or source material;
- etalon list of atomic requirements;
- requirement statuses;
- etalon test cases;
- requirement-to-test-case links;
- expected test-case type;
- expected test-case direction;
- required checks.

## Requirement Statuses

The target quality criteria mention these requirement statuses:

- `ready_for_generation`
- `covered`
- `partially_covered`
- `insufficient_detail`
- `not_covered`
- `excluded`

Important rule: requirements with `insufficient_detail` should be excluded from test-case coverage calculation. The product should not invent missing details and generate unsupported test cases for them.

## Traceability

ЦПТ must preserve internal traceability:

```text
source -> atomic requirement -> requirement status -> generated test cases
```

The UI does not currently need to show atomic requirements to the user, but a service API should expose:

- extracted atomic requirements for a generation run;
- requirement statuses;
- links between atomic requirements and generated test cases.

## Required Metadata

Atomic requirement metadata should include:

- `generationRunId`
- `atomicRequirementId`
- `requirementText`
- `requirementStatus`
- `sourceType`
- `sourceId`
- `sourceVersion` / `updatedAt` / `hash`
- `sourceFragmentRef`
- `linkedTestCaseIds`

Generated test-case metadata should include:

- `testCaseId`
- `generationRunId`
- `linkedRequirementIds`
- `testCaseType`
- `direction`
- `promptVersion`
- `modelVersion`

## Key Metrics

Decomposition metrics:

- requirement extraction recall;
- requirement extraction precision;
- boundary accuracy;
- consolidation accuracy;
- insufficient detail accuracy.

Generation metrics:

- requirement coverage;
- positive coverage;
- negative coverage;
- etalon match;
- extra relevant test-case rate.

Structure metrics:

- schema pass rate;
- required fields completeness;
- expected result completeness;
- step atomicity rate.

Classification metrics:

- test-case type accuracy;
- direction accuracy.

Quality metrics:

- hallucination count;
- unsupported specificity count;
- irrelevant test-case count;
- broken expected result count.

Performance metrics:

- average generation time;
- P95 generation time;
- time by stage.

## Hard Gates

Suggested hard gates:

- schema pass rate equals 100%;
- etalon 30.06 coverage equals 100%;
- no hallucinations on the etalon dataset;
- requirement coverage does not degrade compared with previous baseline;
- hallucination count does not increase;
- smoke dataset cases do not break.

## Implication For Our Implementation

The first implementation should model ЦПТ as a two-stage pipeline:

```text
source materials
  -> extracted atomic requirements
  -> requirement statuses
  -> generated test cases
  -> links between test cases and requirements
  -> metrics and case-level diff
```

The grader layer should therefore include both decomposition graders and test-case generation graders.

