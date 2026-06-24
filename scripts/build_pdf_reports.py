from __future__ import annotations

import argparse
import html
import re
import sqlite3
from pathlib import Path

from pypdf import PdfReader
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4, landscape, portrait
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    KeepTogether,
    PageBreak,
    Paragraph,
    Preformatted,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

from report_eval_rounds import DATASET_ID, build_report, connect, eval_runs


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DB = ROOT / "data" / "cpt_eval.sqlite"
METHODOLOGY_MD = ROOT / "Документация" / "Доки по проекту + критерии" / "scoring-methodology.md"
PDF_ROOT = ROOT / "exports" / "pdf"
METHODOLOGY_PDF = PDF_ROOT / "methodology" / "scoring_methodology.pdf"
LATEST_REPORT_PDF = PDF_ROOT / "eval_rounds_report_latest.pdf"
HISTORY_ROOT = PDF_ROOT / "history"


def register_fonts() -> None:
    fonts_dir = Path("C:/Windows/Fonts")
    pdfmetrics.registerFont(TTFont("Arial", str(fonts_dir / "arial.ttf")))
    pdfmetrics.registerFont(TTFont("Arial-Bold", str(fonts_dir / "arialbd.ttf")))


def styles() -> dict[str, ParagraphStyle]:
    base = getSampleStyleSheet()
    return {
        "h1": ParagraphStyle(
            "h1",
            parent=base["Heading1"],
            fontName="Arial-Bold",
            fontSize=17,
            leading=21,
            spaceAfter=8,
            textColor=colors.HexColor("#1f2937"),
        ),
        "h2": ParagraphStyle(
            "h2",
            parent=base["Heading2"],
            fontName="Arial-Bold",
            fontSize=13,
            leading=16,
            spaceBefore=8,
            spaceAfter=6,
            textColor=colors.HexColor("#111827"),
        ),
        "h3": ParagraphStyle(
            "h3",
            parent=base["Heading3"],
            fontName="Arial-Bold",
            fontSize=10.5,
            leading=13,
            spaceBefore=6,
            spaceAfter=5,
            textColor=colors.HexColor("#374151"),
        ),
        "body": ParagraphStyle(
            "body",
            parent=base["BodyText"],
            fontName="Arial",
            fontSize=8.5,
            leading=11,
            alignment=TA_LEFT,
            spaceAfter=4,
        ),
        "small": ParagraphStyle(
            "small",
            parent=base["BodyText"],
            fontName="Arial",
            fontSize=7.5,
            leading=9.5,
            alignment=TA_LEFT,
            spaceAfter=3,
        ),
        "code": ParagraphStyle(
            "code",
            parent=base["Code"],
            fontName="Arial",
            fontSize=7.5,
            leading=9,
            leftIndent=4,
            backColor=colors.HexColor("#f3f4f6"),
        ),
        "footer": ParagraphStyle(
            "footer",
            parent=base["BodyText"],
            fontName="Arial",
            fontSize=7,
            leading=8,
            textColor=colors.HexColor("#6b7280"),
        ),
    }


def clean_inline(text: str) -> str:
    escaped = html.escape(text)
    escaped = re.sub(r"`([^`]+)`", r"<font name='Arial-Bold'>\1</font>", escaped)
    escaped = re.sub(r"\*\*([^*]+)\*\*", r"<font name='Arial-Bold'>\1</font>", escaped)
    return escaped


def paragraph(text: str, style: ParagraphStyle) -> Paragraph:
    return Paragraph(clean_inline(text), style)


def parse_table(lines: list[str], style: ParagraphStyle, available_width: float) -> Table:
    rows: list[list[str]] = []
    for line in lines:
        stripped = line.strip()
        if re.fullmatch(r"\|?\s*:?-{3,}:?\s*(\|\s*:?-{3,}:?\s*)+\|?", stripped):
            continue
        cells = [cell.strip() for cell in stripped.strip("|").split("|")]
        rows.append(cells)
    if not rows:
        return Table([[""]])

    max_cols = max(len(row) for row in rows)
    for row in rows:
        row.extend([""] * (max_cols - len(row)))

    para_rows = [[paragraph(cell, style) for cell in row] for row in rows]
    first_width = min(45 * mm, available_width * 0.24)
    rest_width = (available_width - first_width) / max(1, max_cols - 1)
    col_widths = [first_width] + [rest_width] * (max_cols - 1)

    table = Table(para_rows, colWidths=col_widths, repeatRows=1, splitByRow=1)
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#fbbf24")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.HexColor("#111827")),
                ("FONTNAME", (0, 0), (-1, 0), "Arial-Bold"),
                ("GRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#d1d5db")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 4),
                ("RIGHTPADDING", (0, 0), (-1, -1), 4),
                ("TOPPADDING", (0, 0), (-1, -1), 3),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f9fafb")]),
            ]
        )
    )
    return table


def markdown_to_flowables(markdown_text: str, page_width: float) -> list[object]:
    st = styles()
    story: list[object] = []
    lines = markdown_text.splitlines()
    index = 0
    in_code = False
    code_lines: list[str] = []

    while index < len(lines):
        line = lines[index].rstrip()

        if line.startswith("```"):
            if in_code:
                story.append(Preformatted("\n".join(code_lines), st["code"]))
                story.append(Spacer(1, 4))
                code_lines = []
                in_code = False
            else:
                in_code = True
            index += 1
            continue

        if in_code:
            code_lines.append(line)
            index += 1
            continue

        if not line.strip():
            story.append(Spacer(1, 3))
            index += 1
            continue

        if line.startswith("|"):
            table_lines = []
            while index < len(lines) and lines[index].lstrip().startswith("|"):
                table_lines.append(lines[index])
                index += 1
            story.append(parse_table(table_lines, st["small"], page_width))
            story.append(Spacer(1, 6))
            continue

        if line.startswith("# "):
            story.append(paragraph(line[2:].strip(), st["h1"]))
        elif line.startswith("## "):
            story.append(paragraph(line[3:].strip(), st["h2"]))
        elif line.startswith("### "):
            story.append(paragraph(line[4:].strip(), st["h3"]))
        elif line.startswith("- "):
            story.append(paragraph("• " + line[2:].strip(), st["body"]))
        else:
            story.append(paragraph(line, st["body"]))
        index += 1

    return story


def add_page_number(canvas, doc) -> None:  # noqa: ANN001
    st = styles()["footer"]
    text = f"Стр. {doc.page}"
    paragraph_obj = Paragraph(text, st)
    width, height = doc.pagesize
    paragraph_obj.wrapOn(canvas, 40 * mm, 10 * mm)
    paragraph_obj.drawOn(canvas, width - 35 * mm, 8 * mm)


def write_pdf(markdown_text: str, output_path: Path, title: str, *, landscape_page: bool) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    page_size = landscape(A4) if landscape_page else portrait(A4)
    margin = 12 * mm
    doc = SimpleDocTemplate(
        str(output_path),
        pagesize=page_size,
        leftMargin=margin,
        rightMargin=margin,
        topMargin=12 * mm,
        bottomMargin=14 * mm,
        title=title,
        author="Codex",
    )
    story = markdown_to_flowables(markdown_text, doc.width)
    doc.build(story, onFirstPage=add_page_number, onLaterPages=add_page_number)


def methodology_pdf_text() -> str:
    return METHODOLOGY_MD.read_text(encoding="utf-8")


def report_pdf_text(connection: sqlite3.Connection, run_code: str | None = None) -> str:
    text = build_report(connection, run_code)
    relative_methodology = "exports/pdf/methodology/scoring_methodology.pdf"
    return (
        text.replace(
            "Формат отчета: цели берутся из БД,",
            f"Методология оценок: `{relative_methodology}`.\n\nФормат отчета: цели берутся из БД,",
            1,
        )
        + "\n"
    )


def verify_pdf(path: Path) -> tuple[int, int]:
    reader = PdfReader(str(path))
    pages = len(reader.pages)
    text_chars = sum(len(page.extract_text() or "") for page in reader.pages)
    if pages == 0 or text_chars == 0:
        raise RuntimeError(f"PDF verification failed for {path}: pages={pages}, text_chars={text_chars}")
    return pages, text_chars


def build_all(db_path: Path) -> list[Path]:
    register_fonts()
    generated: list[Path] = []

    methodology_text = methodology_pdf_text()
    write_pdf(methodology_text, METHODOLOGY_PDF, "Методика выставления оценок", landscape_page=False)
    generated.append(METHODOLOGY_PDF)

    with connect(db_path) as connection:
        latest_text = report_pdf_text(connection)
        write_pdf(latest_text, LATEST_REPORT_PDF, "Отчет по eval-прогонам", landscape_page=True)
        generated.append(LATEST_REPORT_PDF)

        for run in eval_runs(connection):
            run_code = run["run_code"]
            folder = HISTORY_ROOT / run_code
            snapshot_text = report_pdf_text(connection, run_code)
            snapshot_pdf = folder / f"eval_rounds_report_{run_code}.pdf"
            write_pdf(snapshot_text, snapshot_pdf, f"Отчет по eval-прогонам до {run_code}", landscape_page=True)
            generated.append(snapshot_pdf)

    for path in generated:
        pages, text_chars = verify_pdf(path)
        print(f"Verified {path}: {pages} pages, {text_chars} text chars")
    return generated


def main() -> None:
    parser = argparse.ArgumentParser(description="Build PDF reports and methodology.")
    parser.add_argument("--db", type=Path, default=DEFAULT_DB)
    args = parser.parse_args()

    generated = build_all(args.db)
    print("Generated PDFs:")
    for path in generated:
        print(path)


if __name__ == "__main__":
    main()
