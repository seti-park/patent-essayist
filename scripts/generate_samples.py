"""Generate 6 synthetic patent-style PDFs that exercise the hard cases of a
patent OCR/Markdown pipeline.

Each sample emits:
    data/samples/<id>.pdf        — the document
    data/samples/<id>.truth.json — ground-truth metadata for regression checks
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from io import BytesIO
from pathlib import Path

import pymupdf
from reportlab.lib import colors
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.pdfgen import canvas
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "samples"
OUT.mkdir(parents=True, exist_ok=True)


# ---------- shared styles ----------

styles = getSampleStyleSheet()
H1 = ParagraphStyle("H1", parent=styles["Heading1"], fontSize=14, spaceAfter=8)
H2 = ParagraphStyle("H2", parent=styles["Heading2"], fontSize=11, spaceAfter=4)
BODY = ParagraphStyle("Body", parent=styles["BodyText"], fontSize=9, leading=12)
CLAIM = ParagraphStyle("Claim", parent=BODY, leftIndent=12, spaceAfter=4)
CAPTION = ParagraphStyle("Caption", parent=BODY, fontSize=8, alignment=1, textColor=colors.grey)


@dataclass
class Truth:
    sample_id: str
    title: str
    pages_expected: int
    claims_count: int
    has_formulas: bool = False
    has_tables: bool = False
    has_figures: bool = False
    is_scanned: bool = False
    language: str = "en"


# ---------- helpers ----------

def two_column_template(filename: str) -> BaseDocTemplate:
    doc = BaseDocTemplate(filename, pagesize=LETTER,
                          leftMargin=0.6 * inch, rightMargin=0.6 * inch,
                          topMargin=0.7 * inch, bottomMargin=0.7 * inch)
    frame_w = (doc.width - 0.3 * inch) / 2
    frames = [
        Frame(doc.leftMargin, doc.bottomMargin, frame_w, doc.height, id="L"),
        Frame(doc.leftMargin + frame_w + 0.3 * inch, doc.bottomMargin,
              frame_w, doc.height, id="R"),
    ]
    doc.addPageTemplates(PageTemplate(id="two-col", frames=frames))
    return doc


def single_column_template(filename: str) -> BaseDocTemplate:
    doc = BaseDocTemplate(filename, pagesize=LETTER,
                          leftMargin=0.8 * inch, rightMargin=0.8 * inch,
                          topMargin=0.8 * inch, bottomMargin=0.8 * inch)
    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="single")
    doc.addPageTemplates(PageTemplate(id="single", frames=[frame]))
    return doc


def write_truth(truth: Truth) -> None:
    path = OUT / f"{truth.sample_id}.truth.json"
    path.write_text(json.dumps(truth.__dict__, indent=2, ensure_ascii=False))


# ---------- 01. multi-column claims with dependency graph ----------

def sample_01_claims() -> Truth:
    sid = "01_claims_multicol"
    pdf = OUT / f"{sid}.pdf"
    doc = two_column_template(str(pdf))

    story: list = []
    story += [Paragraph("(54) METHOD AND APPARATUS FOR ADAPTIVE QUERY ROUTING", H1),
              Paragraph("(57) Abstract", H2),
              Paragraph(
                  "A method for adaptive routing of database queries across "
                  "heterogeneous backends using a learned cost model. The system "
                  "selects a backend based on predicted latency, freshness, and "
                  "load, and adapts the model online from execution feedback.",
                  BODY),
              Spacer(1, 6),
              Paragraph("Claims", H2)]

    claims = [
        ("1.", "A method comprising: receiving a query Q at a router; computing "
               "a feature vector F from Q; predicting, via a cost model M, an "
               "expected latency for each backend in a set B; and dispatching Q "
               "to argmin_b latency(b)."),
        ("2.", "The method of claim 1, wherein computing F includes hashing the "
               "query plan and concatenating cardinality estimates."),
        ("3.", "The method of claim 1, wherein M is a gradient-boosted regressor "
               "updated nightly from execution traces."),
        ("4.", "The method of claim 3, wherein updating M comprises minimising a "
               "Huber loss over (F, observed_latency) tuples."),
        ("5.", "The method of any of claims 1 to 4, further comprising falling "
               "back to a default backend when predicted latency exceeds a "
               "threshold T."),
        ("6.", "An apparatus comprising memory and one or more processors "
               "configured to perform the method of any one of claims 1 to 5."),
        ("7.", "A non-transitory computer-readable medium storing instructions "
               "that, when executed, cause performance of the method of claim 1."),
    ]
    for n, t in claims:
        story.append(Paragraph(f"<b>{n}</b> {t}", CLAIM))

    doc.build(story)
    truth = Truth(sid, "Adaptive Query Routing", 1, len(claims))
    write_truth(truth)
    return truth


# ---------- 02. math-heavy (RSA-style display equations) ----------

def sample_02_math() -> Truth:
    sid = "02_math_heavy"
    pdf = OUT / f"{sid}.pdf"
    doc = single_column_template(str(pdf))
    story: list = []

    story += [Paragraph("(54) CRYPTOGRAPHIC COMMUNICATIONS SYSTEM AND METHOD", H1),
              Paragraph("(57) Abstract", H2),
              Paragraph(
                  "A cryptographic system based on the difficulty of factoring "
                  "the product of two large primes. Public and private exponents "
                  "are derived such that decryption inverts encryption modulo n.",
                  BODY),
              Spacer(1, 6),
              Paragraph("Detailed Description", H2),
              Paragraph(
                  "Let p and q be distinct primes and let n = p·q. Define "
                  "phi(n) = (p-1)(q-1). Choose e coprime to phi(n) and let d be "
                  "the multiplicative inverse of e modulo phi(n):",
                  BODY),
              Spacer(1, 4),
              Paragraph("    e · d  ≡  1   (mod  φ(n))", BODY),
              Spacer(1, 4),
              Paragraph(
                  "Encryption of message m ∈ Z_n proceeds as c = m^e mod n, "
                  "and decryption as m = c^d mod n. Correctness follows from "
                  "Euler's theorem:",
                  BODY),
              Spacer(1, 4),
              Paragraph("    m^(e·d)  ≡  m^(1 + k·φ(n))  ≡  m   (mod  n)", BODY),
              Spacer(1, 6),
              Paragraph("Claims", H2),
              Paragraph(
                  "<b>1.</b> A communications method comprising: encoding a "
                  "plaintext m as an integer in [0, n); computing c = m^e mod n; "
                  "transmitting c; and recovering m = c^d mod n at a receiver, "
                  "wherein n = p·q for distinct primes p, q and d ≡ e^(-1) "
                  "mod (p-1)(q-1).",
                  CLAIM),
              Paragraph(
                  "<b>2.</b> The method of claim 1, wherein |p| = |q| = 1024 bits.",
                  CLAIM),
              Paragraph(
                  "<b>3.</b> The method of claim 1, wherein e = 65537.",
                  CLAIM)]

    doc.build(story)
    truth = Truth(sid, "RSA-style Cryptosystem", 1, 3, has_formulas=True)
    write_truth(truth)
    return truth


# ---------- 03. chemistry table + caption ----------

def sample_03_chem_table() -> Truth:
    sid = "03_chem_table"
    pdf = OUT / f"{sid}.pdf"
    doc = single_column_template(str(pdf))
    story: list = []

    story += [Paragraph("(54) PYRAZOLOPYRIMIDINONE COMPOUNDS FOR THE TREATMENT OF X", H1),
              Paragraph("(57) Abstract", H2),
              Paragraph(
                  "Compounds of formula (I) and pharmaceutically acceptable "
                  "salts thereof, useful as inhibitors of phosphodiesterase 5.",
                  BODY),
              Spacer(1, 6),
              Paragraph("Examples", H2),
              Paragraph(
                  "Representative compounds and their IC50 values (nM) against "
                  "PDE5 are listed in Table 1. Substituent groups R1–R3 follow "
                  "the numbering of formula (I).",
                  BODY),
              Spacer(1, 6)]

    data = [
        ["Cpd", "R1", "R2", "R3", "IC50 (nM)", "logP"],
        ["1",   "Me",   "n-Pr", "OEt",   "3.5",  "2.1"],
        ["2",   "Et",   "n-Pr", "OEt",   "5.2",  "2.4"],
        ["3",   "Me",   "i-Pr", "OEt",   "12.0", "2.3"],
        ["4",   "Me",   "n-Pr", "OMe",   "8.7",  "1.9"],
        ["5",   "Me",   "n-Pr", "NH-Me", "1.8",  "1.7"],
    ]
    table = Table(data, hAlign="LEFT", colWidths=[40, 50, 60, 70, 70, 50])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
        ("FONT", (0, 0), (-1, 0), "Helvetica-Bold", 9),
        ("FONT", (0, 1), (-1, -1), "Helvetica", 9),
        ("ALIGN", (4, 1), (5, -1), "RIGHT"),
    ]))
    story.append(table)
    story.append(Spacer(1, 4))
    story.append(Paragraph("Table 1. Structure-activity relationships for compounds 1–5.", CAPTION))
    story.append(Spacer(1, 8))
    story.append(Paragraph("Claims", H2))
    story.append(Paragraph(
        "<b>1.</b> A compound of formula (I) wherein R1 is C1–C3 alkyl, R2 is "
        "n-propyl, and R3 is selected from OMe, OEt, and NH-C1–C3-alkyl, or a "
        "pharmaceutically acceptable salt thereof.",
        CLAIM))
    story.append(Paragraph(
        "<b>2.</b> The compound of claim 1, wherein R1 is methyl and R3 is OEt.",
        CLAIM))

    doc.build(story)
    truth = Truth(sid, "Pyrazolopyrimidinone Compounds", 1, 2, has_tables=True)
    write_truth(truth)
    return truth


# ---------- 04. drawings with reference numerals ----------

def _draw_reference_figure(c: canvas.Canvas, x: float, y: float, w: float, h: float) -> None:
    c.setLineWidth(0.7)
    c.rect(x, y, w, h)                           # 100 housing
    c.rect(x + 20, y + 20, 60, 40)               # 110 sensor
    c.rect(x + w - 80, y + 20, 60, 40)           # 120 actuator
    c.line(x + 80, y + 40, x + w - 80, y + 40)   # 130 bus
    c.circle(x + w / 2, y + h - 20, 6, stroke=1, fill=0)  # 140 controller

    c.setFont("Helvetica", 7)
    for label, lx, ly in [("100", x - 12, y + h / 2),
                          ("110", x + 50, y + 8),
                          ("120", x + w - 50, y + 8),
                          ("130", x + w / 2 - 10, y + 32),
                          ("140", x + w / 2 + 10, y + h - 18)]:
        c.drawString(lx, ly, label)


def sample_04_drawings() -> Truth:
    sid = "04_drawings_refs"
    pdf = OUT / f"{sid}.pdf"
    c = canvas.Canvas(str(pdf), pagesize=LETTER)
    width, height = LETTER

    # Page 1: drawing
    c.setFont("Helvetica-Bold", 11)
    c.drawString(0.8 * inch, height - 0.8 * inch, "FIG. 1")
    _draw_reference_figure(c, 1.2 * inch, height - 4.5 * inch, 4.5 * inch, 2.5 * inch)
    c.setFont("Helvetica", 8)
    c.drawString(1.2 * inch, height - 5.0 * inch,
                 "FIG. 1 shows a system 100 having sensor 110, actuator 120, "
                 "communication bus 130, and controller 140.")
    c.showPage()

    # Page 2: description referring to numerals
    c.setFont("Helvetica-Bold", 12)
    c.drawString(0.8 * inch, height - 0.8 * inch, "DETAILED DESCRIPTION")
    text = c.beginText(0.8 * inch, height - 1.1 * inch)
    text.setFont("Helvetica", 10)
    for line in [
        "Referring to FIG. 1, the system 100 includes a sensor 110 communicatively",
        "coupled to a controller 140 via a bus 130. An actuator 120 receives",
        "command signals from the controller 140 over the same bus 130. In some",
        "embodiments, the sensor 110 is an inertial measurement unit; in others,",
        "an optical encoder.",
        "",
        "Claims",
        "1. A system 100 comprising a sensor 110, an actuator 120, a bus 130, and",
        "   a controller 140 coupled to said sensor 110 and said actuator 120 via",
        "   said bus 130.",
        "2. The system of claim 1, wherein the sensor 110 comprises an inertial",
        "   measurement unit.",
    ]:
        text.textLine(line)
    c.drawText(text)
    c.showPage()
    c.save()

    truth = Truth(sid, "System with Sensor/Actuator/Bus/Controller", 2, 2, has_figures=True)
    write_truth(truth)
    return truth


# ---------- 05. scanned-style (no text layer) ----------

def sample_05_scanned() -> Truth:
    sid = "05_scanned_noocr"
    intermediate = OUT / f"_{sid}_text.pdf"
    final = OUT / f"{sid}.pdf"

    # First build a normal text PDF, then re-render as image-only
    doc = single_column_template(str(intermediate))
    story = [
        Paragraph("(54) IMPROVEMENT IN ELECTRIC LAMPS", H1),
        Paragraph("Specification", H2),
        Paragraph(
            "Be it known that I have invented a new and useful Improvement in "
            "Electric Lamps, of which the following is a specification. The "
            "object of this invention is to produce electric lamps giving light "
            "by incandescence, which lamps shall have high resistance, so as to "
            "allow of the practical subdivision of the electric light.",
            BODY),
        Spacer(1, 4),
        Paragraph(
            "The invention consists in a filament of carbon of high resistance, "
            "made as described and secured to metallic wires, the carbon being "
            "enclosed in a glass receiver substantially exhausted of air.",
            BODY),
        Spacer(1, 6),
        Paragraph("Claims", H2),
        Paragraph(
            "<b>1.</b> An electric lamp for giving light by incandescence, "
            "consisting of a filament of carbon of high resistance, made "
            "substantially as described, and secured to metallic wires, as set "
            "forth.",
            CLAIM),
        Paragraph(
            "<b>2.</b> The combination of carbon filaments with a receiver made "
            "entirely of glass and conductors passing through the glass, and "
            "from which receiver the air is exhausted, for the purposes set forth.",
            CLAIM),
    ]
    doc.build(story)

    # Re-render as image-only (no text layer) to simulate a scan
    src = pymupdf.open(intermediate)
    out = pymupdf.open()
    for page in src:
        pix = page.get_pixmap(dpi=200, colorspace=pymupdf.csGRAY)
        img_bytes = pix.tobytes("png")
        new_page = out.new_page(width=page.rect.width, height=page.rect.height)
        new_page.insert_image(new_page.rect, stream=img_bytes)
    out.save(final)
    out.close()
    src.close()
    intermediate.unlink()

    truth = Truth(sid, "Improvement in Electric Lamps (scanned)", 1, 2, is_scanned=True)
    write_truth(truth)
    return truth


# ---------- 06. Korean (CJK) ----------

def sample_06_korean() -> Truth:
    sid = "06_korean_cjk"
    pdf = OUT / f"{sid}.pdf"

    pdfmetrics.registerFont(UnicodeCIDFont("HYSMyeongJo-Medium"))
    pdfmetrics.registerFont(UnicodeCIDFont("HYGothic-Medium"))

    KO_H1 = ParagraphStyle("KO_H1", fontName="HYGothic-Medium", fontSize=14, spaceAfter=8)
    KO_H2 = ParagraphStyle("KO_H2", fontName="HYGothic-Medium", fontSize=11, spaceAfter=4)
    KO_BODY = ParagraphStyle("KO_BODY", fontName="HYSMyeongJo-Medium", fontSize=10, leading=14)
    KO_CLAIM = ParagraphStyle("KO_CLAIM", parent=KO_BODY, leftIndent=12, spaceAfter=6)

    doc = single_column_template(str(pdf))
    story = [
        Paragraph("(54) 적응형 캐시 무효화 방법 및 장치", KO_H1),
        Paragraph("(57) 요약", KO_H2),
        Paragraph(
            "본 발명은 분산 데이터베이스 시스템에서 적응형으로 캐시를 무효화하는 "
            "방법 및 장치에 관한 것이다. 본 발명의 일 실시예에 따르면, 쓰기 빈도와 "
            "키 접근 패턴에 기초하여 무효화 정책을 동적으로 선택함으로써 평균 응답 "
            "지연을 감소시킬 수 있다.",
            KO_BODY),
        Spacer(1, 6),
        Paragraph("발명의 상세한 설명", KO_H2),
        Paragraph(
            "도 1을 참조하면, 시스템(100)은 캐시 매니저(110), 통계 수집기(120), "
            "정책 선택기(130)를 포함한다. 통계 수집기(120)는 키별 쓰기율과 읽기율을 "
            "주기적으로 집계하고, 정책 선택기(130)는 임계값 비교를 통해 TTL 기반 "
            "정책과 쓰기-시-무효화 정책 중 하나를 선택한다.",
            KO_BODY),
        Spacer(1, 6),
        Paragraph("청구항", KO_H2),
        Paragraph(
            "<b>청구항 1.</b> 분산 데이터베이스 시스템에서 캐시를 무효화하는 "
            "방법으로서, 키별 쓰기율과 읽기율을 수집하는 단계; 상기 쓰기율이 임계값 "
            "T를 초과하는 키에 대하여 쓰기-시-무효화 정책을 적용하는 단계; 그렇지 "
            "않은 키에 대하여 TTL 기반 정책을 적용하는 단계를 포함하는 방법.",
            KO_CLAIM),
        Paragraph(
            "<b>청구항 2.</b> 제1항에 있어서, 상기 임계값 T는 최근 1시간 동안의 "
            "전체 쓰기율의 90 백분위수로 동적으로 결정되는 방법.",
            KO_CLAIM),
        Paragraph(
            "<b>청구항 3.</b> 제1항 또는 제2항의 방법을 수행하도록 구성된 하나 이상의 "
            "프로세서 및 메모리를 포함하는 장치.",
            KO_CLAIM),
    ]
    doc.build(story)
    truth = Truth(sid, "적응형 캐시 무효화 방법 및 장치", 1, 3, language="ko")
    write_truth(truth)
    return truth


def main() -> None:
    samples = [
        sample_01_claims,
        sample_02_math,
        sample_03_chem_table,
        sample_04_drawings,
        sample_05_scanned,
        sample_06_korean,
    ]
    for fn in samples:
        truth = fn()
        print(f"  built {truth.sample_id:30s} pages~={truth.pages_expected} claims={truth.claims_count}")


if __name__ == "__main__":
    main()
