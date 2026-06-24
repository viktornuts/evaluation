# Exports

This folder is for generated outputs: review packs, Markdown support reports, and PDF reports.

## Round Output Structure

Every eval round must get its own output folder:

```text
exports/
  rounds/
    <run_code>/
      round_<run_code>_assessment.md
      artifacts/
```

Current example:

```text
exports/rounds/v0/round_v0_assessment.md
exports/rounds/v1/round_v1_assessment.md
exports/rounds/v2/round_v2_assessment.md
```

PDF report history lives separately:

```text
exports/pdf/history/<run_code>/eval_rounds_report_<run_code>.pdf
```

The latest cumulative PDF report is:

```text
exports/pdf/eval_rounds_report_latest.pdf
```

The scoring methodology PDF is:

```text
exports/pdf/methodology/scoring_methodology.pdf
```

Root-level exports may contain cross-round artifacts such as:

```text
exports/eval_rounds_report.md
exports/review_pack_case_001.md
exports/review_pack_case_001.json
```

Do not place new round-specific files directly in `exports/`; use `exports/rounds/<run_code>/`.

