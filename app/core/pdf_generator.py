"""توليد تقارير PDF باللغة العربية."""
from __future__ import annotations

from io import BytesIO
from typing import Iterable

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
from reportlab.lib import colors

ARABIC_FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

# تسجيل خط يدعم العربية
try:
    pdfmetrics.registerFont(TTFont("Arabic", ARABIC_FONT_PATH))
except Exception:
    pass


def generate_table_pdf(title: str, headers: list[str], rows: Iterable[Iterable[str | float]]) -> bytes:
    """إنشاء ملف PDF بسيط لعرض بيانات جدوليّة."""

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
    story: list = []

    title_style = ParagraphStyle(name="Title", fontName="Arabic", fontSize=16, alignment=2)
    table_style = TableStyle(
        [
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#21808D")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("ALIGN", (0, 0), (-1, -1), "RIGHT"),
            ("FONTNAME", (0, 0), (-1, -1), "Arabic"),
            ("FONTSIZE", (0, 0), (-1, -1), 10),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ]
    )

    story.append(Paragraph(title, title_style))
    story.append(Spacer(1, 12))

    table_data = [headers]
    for row in rows:
        table_data.append(list(row))

    table = Table(table_data)
    table.setStyle(table_style)
    story.append(table)

    doc.build(story)
    pdf_value = buffer.getvalue()
    buffer.close()
    return pdf_value
