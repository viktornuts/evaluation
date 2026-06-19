# Sfera CPT Eval Project

Project for building an evaluation system for CPT: an AI product that decomposes source materials into atomic requirements and generates test cases from those requirements.

## Goal

Create a practical eval pipeline that can answer:

- What is the quality of the input requirements in the dataset?
- Did CPT correctly extract atomic requirements from source materials?
- Did CPT correctly generate test cases from requirements?
- Did a new prompt/model/RAG/code version improve or degrade the result?
- Are hallucinations and unsupported details blocked before release?

## Current MVP

The first implemented piece is a local SQLite-backed dataset store:

```text
dataset
  -> dataset_case
    -> source_materials / source_fragments
    -> requirements
      -> requirement_quality_assessments
    -> test_cases / test_case_steps
    -> requirement_test_case_links
```

It supports the first needed workflow:

```text
load manual dataset -> assess input requirements -> link test cases -> validate traceability -> report dataset profile
```

## Quick Start

Create or reset the local database:

```bash
python scripts/init_db.py --reset
```

Import the example case:

```bash
python scripts/import_dataset.py imports/example_dataset_case.json
```

Validate required links and assessments:

```bash
python scripts/validate_dataset.py
```

Print a dataset profile report:

```bash
python scripts/report_dataset_profile.py
```

Export a dataset case for external AI review:

```bash
python scripts/export_review_pack.py CASE-001
```

Import an external review without overwriting project assessments:

```bash
python scripts/import_external_review.py imports/example_external_review.json
```

Report external review disagreements:

```bash
python scripts/report_external_review.py
```

The default SQLite file is created at:

```text
data/cpt_eval.sqlite
```

## Folder Structure

```text
db/
  schema.sql
  seed.sql
data/
  cpt_eval.sqlite
docs/
  project-context.md
  glossary.md
  implementation-plan.md
  source-documents-notes.md
  source-documents-md/
imports/
  README.md
  example_dataset_case.json
exports/
  review packs for external AI review
scripts/
  init_db.py
  import_dataset.py
  validate_dataset.py
  report_dataset_profile.py
  export_review_pack.py
  import_external_review.py
  report_external_review.py
source-documents/
  original PDF/DOCX source documents
```

## Source Documents

Original strategy notes, PDFs, product specs, and related materials live in `source-documents/`.
Fast Markdown copies for reading and search live in `docs/source-documents-md/`.
