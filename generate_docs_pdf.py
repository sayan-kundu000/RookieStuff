"""
PDF Generator for RookieStuff Documentation.
Generates an exact 37-page PDF corresponding to 37 topics, each having 7 paragraphs.
"""

import sys
import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    PageBreak,
    Table,
    TableStyle,
    HRFlowable,
)
from reportlab.pdfgen import canvas

from docs_content import TOPICS


class NumberedCanvas(canvas.Canvas):
    """
    Two-pass canvas to dynamically compute and draw accurate total page count
    and consistent running headers/footers.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_decorations(self, total_pages):
        self.saveState()

        # Running Top Header Rule
        self.setStrokeColor(colors.HexColor("#30363d"))
        self.setLineWidth(0.75)
        self.line(36, 792 - 24, 612 - 36, 792 - 24)

        # Running Top Header Text
        self.setFont("Helvetica-Bold", 7.5)
        self.setFillColor(colors.HexColor("#238636"))
        self.drawString(36, 792 - 20, "ROOKIESTUFF")

        self.setFont("Helvetica", 7.5)
        self.setFillColor(colors.HexColor("#57606a"))
        self.drawString(100, 792 - 20, "|  Autonomous Code Review & Refactoring Agent with LangGraph")

        # Running Bottom Footer Rule
        self.setStrokeColor(colors.HexColor("#d0d7de"))
        self.setLineWidth(0.5)
        self.line(36, 32, 612 - 36, 32)

        # Running Bottom Footer Text
        self.setFont("Helvetica", 7.5)
        self.setFillColor(colors.HexColor("#57606a"))
        self.drawString(36, 22, "RookieStuff Master Engineering & Architecture Documentation  •  Super Simple Plain Words Edition")

        page_str = f"Page {self._pageNumber} of {total_pages}"
        self.drawRightString(612 - 36, 22, page_str)

        self.restoreState()


def build_pdf(filename: str = "RookieStuff_Documentation.pdf"):
    print(f"Starting PDF generation: {filename}")
    print(f"Total topics to render: {len(TOPICS)}")

    # Document Geometry
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=36,
        rightMargin=36,
        topMargin=36,
        bottomMargin=40,
    )

    styles = getSampleStyleSheet()

    # Custom typography styles
    category_style = ParagraphStyle(
        "CategoryTag",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=8,
        leading=10,
        textColor=colors.HexColor("#0969da"),
        spaceAfter=3,
        textTransform="uppercase",
    )

    title_style = ParagraphStyle(
        "TopicTitle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=13,
        leading=16,
        textColor=colors.HexColor("#1f2328"),
        spaceAfter=4,
    )

    meta_style = ParagraphStyle(
        "TopicMeta",
        parent=styles["Normal"],
        fontName="Helvetica-Oblique",
        fontSize=7.5,
        leading=9.5,
        textColor=colors.HexColor("#656d76"),
        spaceAfter=6,
    )

    body_style = ParagraphStyle(
        "TopicBody",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8.5,
        leading=11.4,
        textColor=colors.HexColor("#24292f"),
        spaceAfter=4.5,
        alignment=4,  # Justified
    )

    story = []

    for idx, topic in enumerate(TOPICS):
        topic_num = topic["id"]
        title_text = topic["title"]
        category_text = topic["category"]
        paragraphs = topic["paragraphs"]

        # Ensure exact paragraph count
        if len(paragraphs) != 7:
            print(f"WARNING: Topic {topic_num} has {len(paragraphs)} paragraphs instead of 7!")

        # Category Pill / Tag
        story.append(Paragraph(f"<b>{category_text}</b>  •  TOPIC {topic_num} OF 37", category_style))

        # Main Topic Title
        story.append(Paragraph(f"Topic {topic_num}: {title_text}", title_style))

        # Divider rule below header
        story.append(HRFlowable(
            width="100%",
            thickness=1.0,
            color=colors.HexColor("#238636"),
            spaceBefore=2,
            spaceAfter=7,
        ))

        # Render each of the 7 paragraphs
        for p_idx, para in enumerate(paragraphs, 1):
            story.append(Paragraph(para, body_style))

        # PageBreak after each topic except the last one
        if idx < len(TOPICS) - 1:
            story.append(PageBreak())

    # Build the document with the NumberedCanvas
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Successfully generated {filename}")


if __name__ == "__main__":
    output_path = "RookieStuff_Documentation.pdf"
    if len(sys.argv) > 1:
        output_path = sys.argv[1]
    build_pdf(output_path)
