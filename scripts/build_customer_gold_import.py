from __future__ import annotations

import json
import shutil
from pathlib import Path

from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[1]
IMPORT_DATASET_DIR = ROOT / "imports" / "datasets" / "customer_gold_v1"
ROWS_PATH = IMPORT_DATASET_DIR / "customer_gold_v1_requirement_rows.json"
IMPORT_PATH = IMPORT_DATASET_DIR / "customer_gold_v1_requirements.json"
PDF_TMP_PATH = ROOT / "tmp" / "pdfs" / "source_requirements.pdf"
DATASET_DIR = ROOT / "Документация" / "Датасеты" / "customer_gold_v1"
SOURCE_PDF_PATH = DATASET_DIR / "source" / "source_requirements.pdf"
REQUIREMENTS_MD_PATH = DATASET_DIR / "requirements" / "requirements.md"

CRITERIA = [
    "source_quality",
    "completeness",
    "consistency",
    "correctness",
    "unambiguity",
    "testability",
    "traceability",
    "modifiability",
    "atomicity",
    "feasibility",
]


def read_pdf_text(pdf_path: Path) -> tuple[str, int]:
    reader = PdfReader(str(pdf_path))
    page_texts = [page.extract_text() or "" for page in reader.pages]
    return "\n\n".join(page_texts), len(page_texts)


def build_payload(rows: list[dict[str, str]], raw_text: str, page_count: int) -> dict:
    fragments = []
    input_requirements = []
    expected_requirements = []
    decomposition_links = []

    for order, row in enumerate(rows, start=1):
        code = row["code"]
        suffix = code.lower().replace("-", "_")
        fragment_id = f"frag_customer_gold_{suffix}"
        input_id = f"input_customer_gold_{suffix}"
        req_id = f"req_customer_gold_{suffix}"

        fragments.append(
            {
                "id": fragment_id,
                "fragment_ref": (
                    f"{code}; пункт {row['point']}; стр. {row['page']}; "
                    f"канал {row['channel']}"
                ),
                "fragment_text": (
                    f"{row['quote']}\n"
                    f"Пункт: {row['point']}. Стр.: {row['page']}. "
                    f"Канал: {row['channel']}."
                ),
            }
        )
        input_requirements.append(
            {
                "id": input_id,
                "input_requirement_code": code,
                "title": row["text"],
                "requirement_text": row["text"],
                "source_fragment_id": fragment_id,
                "requirement_order": order,
            }
        )
        expected_requirements.append(
            {
                "id": req_id,
                "requirement_code": code,
                "requirement_text": row["text"],
                "origin": "expected",
                "expected_status": "ready_for_generation",
                "quality_profile_status": "gold_standard",
                "risk_level": "normal",
                "is_ready_for_generation": True,
                "comment": (
                    "Эталонное требование заказчика. "
                    f"Пункт: {row['point']}; стр.: {row['page']}; "
                    f"канал: {row['channel']}."
                ),
                "source_links": [
                    {
                        "id": f"rsl_customer_gold_{suffix}",
                        "source_fragment_id": fragment_id,
                        "link_type": "derived_from",
                        "rationale": "Требование выделено из эталонного ТЗ заказчика.",
                    }
                ],
                "quality_assessments": [
                    {
                        "id": f"rqa_customer_gold_{suffix}_{criterion}",
                        "criterion": criterion,
                        "score": 10.0,
                        "label": "gold_standard",
                        "rationale": (
                            "Эталонное требование от заказчика; по текущей "
                            "договоренности для золотого набора выставлен максимум."
                        ),
                        "assessed_by": "Viktor/Codex",
                        "assessment_method": "human_assisted",
                        "confidence": 1.0,
                    }
                    for criterion in CRITERIA
                ],
            }
        )
        decomposition_links.append(
            {
                "id": f"decomp_customer_gold_{suffix}",
                "input_requirement_id": input_id,
                "requirement_id": req_id,
                "link_type": "expected_atomic_requirement",
                "rationale": (
                    "В текущем gold import входное эталонное требование совпадает "
                    "с ожидаемым атомарным требованием."
                ),
            }
        )

    return {
        "dataset": {
            "id": "dataset_customer_gold_v1",
            "name": "customer_gold",
            "version": "v1",
            "description": (
                "Высокоприоритетный эталонный датасет от заказчика: "
                "требования по интеграции С.ФТ с С.Релизы."
            ),
            "status": "draft",
        },
        "cases": [
            {
                "id": "case_customer_gold_release_integration",
                "case_code": "GOLD-REQ-001",
                "title": "Интеграция С.ФТ с С.Релизы: эталонные требования",
                "description": (
                    "Эталонный набор требований из ТЗ заказчика. На текущем этапе "
                    "всем требованиям выставлен score 10 по критериям качества требований."
                ),
                "case_type": "golden",
                "input_profile_code": "customer_gold_requirements",
                "input_profile_name": "Эталонные требования заказчика",
                "source_materials": [
                    {
                        "id": "src_customer_gold_v1_release_integration_tz",
                        "source_type": "ТЗ",
                        "source_name": "ТЗ Интеграция с С.Релизы 20.1",
                        "source_version": "20.1",
                        "raw_text": raw_text,
                        "metadata": {
                            "source_file": (
                                "Документация/Датасеты/customer_gold_v1/"
                                "source/source_requirements.pdf"
                            ),
                            "pages": page_count,
                            "priority": "super_high",
                        },
                        "fragments": fragments,
                    }
                ],
                "input_requirements": input_requirements,
                "requirements": expected_requirements,
                "input_requirement_decomposition_links": decomposition_links,
                "test_cases": [],
                "requirement_test_case_links": [],
                "unsupported_details": [],
            }
        ],
    }


def write_requirements_md(rows: list[dict[str, str]]) -> None:
    REQUIREMENTS_MD_PATH.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Эталонные требования customer_gold_v1",
        "",
        "Источник: `../source/source_requirements.pdf`.",
        "",
        "| Код | Требование | Пункт | Стр. | Канал |",
        "|---|---|---|---|---|",
    ]
    for row in rows:
        lines.append(
            f"| {row['code']} | {row['text']} | {row['point']} | "
            f"{row['page']} | {row['channel']} |"
        )
    REQUIREMENTS_MD_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    rows = json.loads(ROWS_PATH.read_text(encoding="utf-8"))
    pdf_path = PDF_TMP_PATH if PDF_TMP_PATH.exists() else SOURCE_PDF_PATH
    raw_text, page_count = read_pdf_text(pdf_path)
    payload = build_payload(rows, raw_text, page_count)

    IMPORT_PATH.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    SOURCE_PDF_PATH.parent.mkdir(parents=True, exist_ok=True)
    if pdf_path != SOURCE_PDF_PATH:
        shutil.copy2(pdf_path, SOURCE_PDF_PATH)
    write_requirements_md(rows)

    print(f"Wrote {IMPORT_PATH}")
    print(f"Requirements: {len(rows)}")
    print(f"Assessments: {len(rows) * len(CRITERIA)}")


if __name__ == "__main__":
    main()
