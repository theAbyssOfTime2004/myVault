#!/usr/bin/env python3
"""Generate a formal bilingual (Vietnamese/English) academic transcript PDF from a GPA CSV export.

Usage:
    python3 generate_transcript.py GPA.csv Transcript.pdf [student_info.json]

The optional JSON file fills in the personal details the CSV does not contain, e.g.:
    {"name": "Nguyen Van A", "student_id": "22120001", "institution": "...",
     "faculty": "...", "program": "...", "cohort": "...", "date_of_birth": "..."}
"""

import csv
import json
import re
import sys
import unicodedata
from datetime import date

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, Frame, KeepTogether, PageBreak,
                                PageTemplate, Paragraph, Spacer, Table, TableStyle)

# ---------------------------------------------------------------- fonts ----
FONT_DIR = "/usr/share/fonts/truetype/liberation"
pdfmetrics.registerFont(TTFont("Serif", f"{FONT_DIR}/LiberationSerif-Regular.ttf"))
pdfmetrics.registerFont(TTFont("Serif-Bold", f"{FONT_DIR}/LiberationSerif-Bold.ttf"))
pdfmetrics.registerFont(TTFont("Serif-Italic", f"{FONT_DIR}/LiberationSerif-Italic.ttf"))
pdfmetrics.registerFont(TTFont("Serif-BoldItalic", f"{FONT_DIR}/LiberationSerif-BoldItalic.ttf"))
pdfmetrics.registerFontFamily("Serif", normal="Serif", bold="Serif-Bold",
                              italic="Serif-Italic", boldItalic="Serif-BoldItalic")

INK = colors.HexColor("#101010")
MUTED = colors.HexColor("#5a5a5a")
RULE = colors.HexColor("#9a9a9a")
BAND = colors.HexColor("#ececec")
LIGHT = colors.HexColor("#d6d6d6")

# ---------------------------------------------------- English course names ----
EN = {
    "BAA00003": "Ho Chi Minh Ideology",
    "BAA00004": "Introduction to Law",
    "BAA00005": "General Economics",
    "BAA00101": "Marxist-Leninist Philosophy",
    "BAA00102": "Marxist-Leninist Political Economy",
    "BAA00103": "Scientific Socialism",
    "BAA00104": "History of the Communist Party of Vietnam",
    "CSC00004": "Introduction to Information Technology",
    "ENV00003": "Human Beings and the Environment",
    "MTH00003": "Calculus 1B",
    "MTH00004": "Calculus 2B",
    "MTH00016": "Fundamentals of Data Processing",
    "MTH00030": "Linear Algebra",
    "MTH00041": "Discrete Mathematics",
    "MTH00042": "Probability",
    "MTH00050": "Combinatorial Mathematics",
    "MTH00055": "Programming Fundamentals",
    "MTH00081": "Calculus 1B (Laboratory)",
    "MTH00082": "Calculus 2B (Laboratory)",
    "MTH00083": "Linear Algebra (Laboratory)",
    "MTH00086": "Discrete Mathematics (Laboratory)",
    "MTH10107": "Programming Techniques",
    "MTH10109": "Statistics (Laboratory)",
    "MTH10131": "Statistical Theory",
    "MTH10171": "Introduction to Data Science",
    "MTH10311": "Computer Networks",
    "MTH10312": "Databases",
    "MTH10318": "Introduction to Artificial Intelligence",
    "MTH10322": "Pattern Recognition",
    "MTH10353": "Introduction to Machine Learning",
    "MTH10358": "Data Mining",
    "MTH10359": "Natural Language Processing",
    "MTH10405": "Data Structures and Algorithms",
    "MTH10407": "Object-Oriented Programming",
    "MTH10433": "Numerical Analysis",
    "MTH10449": "Linear Programming",
    "MTH10595": "Undergraduate Thesis",
    "MTH10605": "Python for Data Science",
    "MTH10607": "Numerical Methods for Data Science",
    "MTH10620": "Data Science Seminar",
    "PHY00001": "General Physics 1 (Mechanics - Thermodynamics)",
    "PHY00002": "General Physics 2 (Electromagnetism - Optics)",
}


def clean(text):
    """Drop invisible bidi/zero-width marks and collapse whitespace."""
    text = "".join(ch for ch in text if unicodedata.category(ch) != "Cf")
    return re.sub(r"\s+", " ", text).strip()


def parse_csv(path):
    rows, totals = [], {}
    with open(path, encoding="utf-8-sig", newline="") as fh:
        for raw in csv.reader(fh):
            cells = [clean(c) for c in raw]
            if not cells or not cells[0]:
                continue
            if cells[0].startswith("Tên môn học"):
                continue
            if len(cells) < 7 or not re.match(r"^[A-Z]{3}\d{5}\s*-", cells[0]):
                key = cells[0].split(":")[0].strip()
                if ":" in cells[0]:
                    totals[key] = cells[0].split(":", 1)[1].strip()
                continue
            code, _, title = cells[0].partition("-")
            rows.append({
                "code": code.strip(),
                "title_vi": title.strip(),
                "title_en": EN.get(code.strip(), ""),
                "credits": int(float(cells[1])),
                "score10": float(cells[2]),
                "letter": cells[3].rstrip("."),
                "score4": float(cells[4]),
                "term": cells[5],
            })
    return rows, totals


def term_sort_key(term):
    years, part = term.split("/")
    return (int(years.split("-")[0]), int(part))


def term_label(term):
    years, part = term.split("/")
    y1, y2 = years.split("-")
    name = {"1": "Semester 1", "2": "Semester 2", "3": "Summer Term"}.get(part, f"Term {part}")
    vi = {"1": "Học kỳ 1", "2": "Học kỳ 2", "3": "Học kỳ hè"}.get(part, f"Học kỳ {part}")
    return f"{name} &nbsp;·&nbsp; Academic Year 20{y1}-20{y2}", f"{vi} · Năm học 20{y1}-20{y2}"


def gpa(rows, field):
    credits = sum(r["credits"] for r in rows)
    if not credits:
        return 0.0, 0
    return sum(r[field] * r["credits"] for r in rows) / credits, credits


def classify(g4):
    for cut, vi, en in ((3.60, "Xuất sắc", "Excellent"), (3.20, "Giỏi", "Very Good"),
                        (2.50, "Khá", "Good"), (2.00, "Trung bình", "Average")):
        if g4 >= cut:
            return vi, en
    return "Trung bình yếu", "Below Average"


# ---------------------------------------------------------------- styles ----
def styles():
    base = dict(fontName="Serif")
    return {
        "org": ParagraphStyle("org", **base, fontSize=9.5, alignment=TA_CENTER,
                              spaceAfter=1, leading=12, textColor=INK),
        "orgsub": ParagraphStyle("orgsub", **base, fontSize=8.5, leading=11,
                                 alignment=TA_CENTER, textColor=MUTED),
        "title": ParagraphStyle("title", fontName="Serif-Bold", fontSize=17, leading=20,
                                alignment=TA_CENTER, textColor=INK, spaceBefore=6),
        "subtitle": ParagraphStyle("subtitle", fontName="Serif-Italic", fontSize=10.5,
                                   leading=13, alignment=TA_CENTER, textColor=MUTED),
        "label": ParagraphStyle("label", **base, fontSize=8.5, textColor=MUTED, leading=12),
        "value": ParagraphStyle("value", fontName="Serif-Bold", fontSize=9.5, leading=12,
                                textColor=INK),
        "section": ParagraphStyle("section", fontName="Serif-Bold", fontSize=9.5, leading=12,
                                  textColor=INK, spaceBefore=2, spaceAfter=4),
        "th": ParagraphStyle("th", fontName="Serif-Bold", fontSize=7.6, leading=9.2,
                             alignment=TA_CENTER, textColor=INK),
        "vi": ParagraphStyle("vi", **base, fontSize=8.6, leading=10.2, textColor=INK),
        "en": ParagraphStyle("en", fontName="Serif-Italic", fontSize=7.4, leading=8.8,
                             textColor=MUTED),
        "num": ParagraphStyle("num", **base, fontSize=8.6, leading=10.2, alignment=TA_CENTER, textColor=INK),
        "band": ParagraphStyle("band", fontName="Serif-Bold", fontSize=8.4, leading=10,
                               textColor=INK),
        "bandvi": ParagraphStyle("bandvi", fontName="Serif-Italic", fontSize=7.4, leading=9,
                                 textColor=MUTED),
        "sub": ParagraphStyle("sub", fontName="Serif-Italic", fontSize=7.8, leading=9.5,
                              textColor=MUTED),
        "note": ParagraphStyle("note", **base, fontSize=7.6, textColor=MUTED,
                               leading=10, alignment=TA_JUSTIFY),
        "legend": ParagraphStyle("legend", **base, fontSize=7.6, leading=9.4,
                                 alignment=TA_CENTER, textColor=INK),
        "legendh": ParagraphStyle("legendh", fontName="Serif-Bold", fontSize=7.6, leading=9.4,
                                  alignment=TA_CENTER, textColor=INK),
        "big": ParagraphStyle("big", fontName="Serif-Bold", fontSize=13, leading=15,
                              alignment=TA_CENTER, textColor=INK),
        "bigcap": ParagraphStyle("bigcap", **base, fontSize=7.4, textColor=MUTED,
                                 leading=9, alignment=TA_CENTER),
    }


COLS = [24, 55, 244, 40, 40, 36, 38]   # sums to 477 pt


def info_block(st, info):
    def cell(label, key, fallback="." * 54):
        v = info.get(key) or ""
        value = v if v else f'<font color="#9a9a9a">{fallback}</font>'
        return [Paragraph(label, st["label"]), Paragraph(value, st["value"])]

    pairs = [
        ("Full name / Họ và tên", "name", "Student ID / Mã số sinh viên", "student_id"),
        ("Date of birth / Ngày sinh", "date_of_birth", "Cohort / Khóa", "cohort"),
        ("Program / Ngành đào tạo", "program", "Degree awarded / Trình độ", "degree"),
        ("Faculty / Khoa", "faculty", "Mode of study / Loại hình đào tạo", "mode"),
        ("Institution / Trường", "institution", "Period of study / Thời gian đào tạo", "period"),
    ]
    data = [[cell(l1, k1), cell(l2, k2)] for l1, k1, l2, k2 in pairs]
    t = Table(data, colWidths=[243, 234])
    t.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (0, -1), 0),
        ("LEFTPADDING", (1, 0), (1, -1), 9),
        ("RIGHTPADDING", (0, 0), (-1, -1), 12),
    ]))
    return t


def course_table(st, rows):
    head = ["No.", "Course<br/>code", "Course title / Tên môn học", "Credits<br/>Tín chỉ",
            "Score<br/>(10.0)", "Letter<br/>grade", "Grade<br/>(4.0)"]
    data = [[Paragraph(h, st["th"]) for h in head]]
    style = [
        ("FONTNAME", (0, 0), (-1, -1), "Serif"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 3.5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3.5),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("BACKGROUND", (0, 0), (-1, 0), BAND),
        ("LINEABOVE", (0, 0), (-1, 0), 0.9, INK),
        ("LINEBELOW", (0, 0), (-1, 0), 0.9, INK),
        ("ALIGN", (3, 1), (-1, -1), "CENTER"),
    ]

    n = 0
    r = 1
    for term in sorted({x["term"] for x in rows}, key=term_sort_key):
        block = [x for x in rows if x["term"] == term]
        en_lab, vi_lab = term_label(term)
        data.append([Paragraph(f"{en_lab}", st["band"]), "", "",
                     Paragraph(vi_lab, st["bandvi"]), "", "", ""])
        style += [("SPAN", (0, r), (2, r)), ("SPAN", (3, r), (6, r)),
                  ("BACKGROUND", (0, r), (-1, r), BAND),
                  ("ALIGN", (3, r), (6, r), "RIGHT"),
                  ("LINEABOVE", (0, r), (-1, r), 0.5, RULE)]
        r += 1
        for c in block:
            n += 1
            title = Paragraph(c["title_vi"], st["vi"])
            cell = [title]
            if c["title_en"]:
                cell.append(Paragraph(c["title_en"], st["en"]))
            data.append([
                Paragraph(str(n), st["num"]), Paragraph(c["code"], st["num"]), cell,
                Paragraph(str(c["credits"]), st["num"]),
                Paragraph(f'{c["score10"]:.1f}', st["num"]),
                Paragraph(c["letter"], st["num"]),
                Paragraph(f'{c["score4"]:.2f}', st["num"]),
            ])
            style.append(("LINEBELOW", (0, r), (-1, r), 0.25, LIGHT))
            r += 1
        g10, cr = gpa(block, "score10")
        g4, _ = gpa(block, "score4")
        data.append(["", "", Paragraph(
            f"Term credits: <b>{cr}</b> &nbsp;&nbsp;|&nbsp;&nbsp; Term GPA: "
            f"<b>{g10:.2f}</b>/10.0 &nbsp;&nbsp;|&nbsp;&nbsp; <b>{g4:.2f}</b>/4.0",
            st["sub"]), "", "", "", ""])
        style += [("SPAN", (2, r), (6, r)), ("ALIGN", (2, r), (6, r), "RIGHT"),
                  ("LINEBELOW", (0, r), (-1, r), 0.5, RULE)]
        r += 1

    style.append(("LINEBELOW", (0, r - 1), (-1, r - 1), 0.9, INK))
    t = Table(data, colWidths=COLS, repeatRows=1)
    t.setStyle(TableStyle(style))
    return t


def summary_block(st, rows, totals):
    g10, credits = gpa(rows, "score10")
    g4, _ = gpa(rows, "score4")
    vi, en = classify(g4)
    cards = [
        (f"{credits}", "Total credits earned<br/>Số tín chỉ tích lũy"),
        (f"{g10:.2f}<font size=8>/10.0</font>", "Cumulative GPA<br/>Điểm trung bình tích lũy"),
        (f"{g4:.2f}<font size=8>/4.0</font>", "Cumulative GPA (4.0)<br/>ĐTB tích lũy hệ 4"),
        (en, f"Classification<br/>Xếp loại: {vi}"),
    ]
    data = [[Paragraph(v, st["big"]) for v, _ in cards],
            [Paragraph(c, st["bigcap"]) for _, c in cards]]
    t = Table(data, colWidths=[477 / 4] * 4)
    t.setStyle(TableStyle([
        ("BOX", (0, 0), (-1, -1), 0.9, INK),
        ("INNERGRID", (0, 0), (-1, -1), 0.35, LIGHT),
        ("SPAN", (0, 0), (0, 0)),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, 0), 9),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 1),
        ("TOPPADDING", (0, 1), (-1, 1), 0),
        ("BOTTOMPADDING", (0, 1), (-1, 1), 9),
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#f7f7f7")),
    ]))
    return t


def legend_block(st, rows):
    scale = [("A+", "9.0 - 10.0", "4.00", "Excellent"),
             ("A", "8.0 - 8.9", "3.50 - 3.80", "Very good"),
             ("B+", "7.0 - 7.9", "3.15 - 3.45", "Good"),
             ("B", "6.0 - 6.9", "2.50 - 2.90", "Fairly good"),
             ("C", "5.0 - 5.9", "2.00 - 2.20", "Average"),
             ("D", "4.0 - 4.9", "1.50 - 1.95", "Below average"),
             ("F", "below 4.0", "0.00", "Fail")]
    head = ["Letter grade", "Score (10.0 scale)", "Grade point (4.0)", "Description"]
    data = [[Paragraph(h, st["legendh"]) for h in head]]
    data += [[Paragraph(c, st["legend"]) for c in row] for row in scale]
    t = Table(data, colWidths=[95, 130, 122, 130])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), BAND),
        ("LINEABOVE", (0, 0), (-1, 0), 0.7, INK),
        ("LINEBELOW", (0, 0), (-1, 0), 0.5, RULE),
        ("LINEBELOW", (0, -1), (-1, -1), 0.7, INK),
        ("INNERGRID", (0, 1), (-1, -1), 0.25, LIGHT),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 2.6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2.6),
    ]))
    return t


def build(csv_path, out_path, info):
    rows, totals = parse_csv(csv_path)
    terms = sorted({r["term"] for r in rows}, key=term_sort_key)
    info.setdefault("period", "20{} - 20{}".format(terms[0].split("-")[0],
                                                   terms[-1].split("/")[0].split("-")[1]))
    st = styles()
    doc = BaseDocTemplate(out_path, pagesize=A4,
                          leftMargin=(A4[0] - 477) / 2, rightMargin=(A4[0] - 477) / 2,
                          topMargin=17 * mm, bottomMargin=17 * mm,
                          title="Academic Transcript",
                          author=info.get("name") or "Academic Transcript",
                          subject="Undergraduate academic record")

    name = info.get("name") or ""

    def decorate(canvas, docu):
        canvas.saveState()
        canvas.setFont("Serif", 7.2)
        canvas.setFillColor(MUTED)
        y = 11 * mm
        canvas.setStrokeColor(LIGHT)
        canvas.setLineWidth(0.4)
        canvas.line(docu.leftMargin, y + 9, A4[0] - docu.rightMargin, y + 9)
        left = f"Academic Transcript / Bảng điểm học tập" + (f" - {name}" if name else "")
        canvas.drawString(docu.leftMargin, y, left)
        canvas.drawRightString(A4[0] - docu.rightMargin, y, f"Page {docu.page}")
        canvas.restoreState()

    frame = Frame(doc.leftMargin, doc.bottomMargin, 477,
                  A4[1] - doc.topMargin - doc.bottomMargin, id="body",
                  leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
    doc.addPageTemplates([PageTemplate(id="all", frames=[frame], onPage=decorate)])

    flow = []
    org = info.get("institution") or ""
    if org:
        flow.append(Paragraph(org.upper(), st["org"]))
    if info.get("institution_en"):
        flow.append(Paragraph(info["institution_en"], st["orgsub"]))
    flow.append(Spacer(1, 4))
    flow.append(Paragraph("ACADEMIC TRANSCRIPT", st["title"]))
    flow.append(Paragraph("Bảng điểm học tập &nbsp;·&nbsp; Undergraduate Program", st["subtitle"]))
    flow.append(Spacer(1, 9))

    line = Table([[""]], colWidths=[477], rowHeights=[0.1])
    line.setStyle(TableStyle([("LINEABOVE", (0, 0), (-1, -1), 0.9, INK)]))
    flow += [line, Spacer(1, 8), info_block(st, info), Spacer(1, 2)]
    flow.append(line)
    flow.append(Spacer(1, 10))

    flow.append(Paragraph("I. &nbsp;RECORD OF COURSES / KẾT QUẢ HỌC TẬP", st["section"]))
    flow.append(course_table(st, rows))
    flow.append(Spacer(1, 12))

    tail = [Paragraph("II. &nbsp;SUMMARY / TỔNG KẾT", st["section"]),
            summary_block(st, rows, totals), Spacer(1, 12),
            Paragraph("III. &nbsp;GRADING SYSTEM / THANG ĐIỂM", st["section"]),
            legend_block(st, rows), Spacer(1, 9),
            Paragraph(
                "<b>Notes.</b> &nbsp;Courses are listed in chronological order by academic term. "
                "A grade point on the 4.0 scale is derived from the 10.0-scale score as "
                "min(4.00, 0.5 x score - 0.5). The cumulative grade point average is the "
                "credit-weighted mean of all graded "
                "courses listed above, computed on both the Vietnamese 10.0 scale and the "
                "4.0 scale. English course titles are provided for reference; the Vietnamese "
                "titles are authoritative.<br/>"
                "<i>Ghi chú: Các môn học được liệt kê theo thứ tự học kỳ. Điểm trung bình tích "
                "lũy được tính theo trung bình có trọng số theo số tín chỉ.</i>", st["note"]),
            Spacer(1, 6),
            Paragraph(
                f"This document is a personal summary of the holder's academic record, compiled "
                f"from the official grade report issued by the university on "
                f"{date.today():%d %B %Y}. It is provided for information only and does not "
                f"replace the official transcript issued and sealed by the institution.<br/>"
                f"<i>Tài liệu này là bản tổng hợp cá nhân, không thay thế bảng điểm chính thức "
                f"do nhà trường cấp.</i>", st["note"])]
    flow.append(KeepTogether(tail[:2]))
    flow += tail[2:]

    doc.build(flow)
    g10, credits = gpa(rows, "score10")
    g4, _ = gpa(rows, "score4")
    print(f"Wrote {out_path}: {len(rows)} courses, {credits} credits, "
          f"GPA {g10:.4f}/10, {g4:.4f}/4")
    for k, v in totals.items():
        print(f"  source: {k} = {v}")


if __name__ == "__main__":
    csv_path = sys.argv[1]
    out_path = sys.argv[2] if len(sys.argv) > 2 else "transcript.pdf"
    info = {}
    if len(sys.argv) > 3:
        with open(sys.argv[3], encoding="utf-8") as fh:
            info = json.load(fh)
    build(csv_path, out_path, info)
