"""
PDF Generator for the RookieStuff 45-Minute YouTube Script.
Produces a beautiful, professional, multi-page video production script PDF
with scene timecodes, on-screen camera/action cues, spoken dialogue,
and presenter pro-tips.
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
    KeepTogether,
)
from reportlab.pdfgen import canvas

from youtube_script_content import SCENES


class ScriptNumberedCanvas(canvas.Canvas):
    """
    Two-pass canvas for running header and page numbering footer.
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
            self.draw_decorations(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_decorations(self, total_pages):
        self.saveState()

        # Running Top Header Rule
        self.setStrokeColor(colors.HexColor("#30363d"))
        self.setLineWidth(0.75)
        self.line(36, 792 - 24, 612 - 36, 792 - 24)

        # Running Top Header Text
        self.setFont("Helvetica-Bold", 7.5)
        self.setFillColor(colors.HexColor("#da3633"))
        self.drawString(36, 792 - 20, "YOUTUBE PRODUCTION SCRIPT")

        self.setFont("Helvetica", 7.5)
        self.setFillColor(colors.HexColor("#57606a"))
        self.drawString(165, 792 - 20, "|  RookieStuff 45-Minute Deep Dive Video  •  Action & Speech Blueprint")

        # Running Bottom Footer Rule
        self.setStrokeColor(colors.HexColor("#d0d7de"))
        self.setLineWidth(0.5)
        self.line(36, 32, 612 - 36, 32)

        # Running Bottom Footer Text
        self.setFont("Helvetica", 7.5)
        self.setFillColor(colors.HexColor("#57606a"))
        self.drawString(36, 22, "RookieStuff YouTube Script  •  Super Simple Plain Words  •  45-Minute Target Runtime")

        page_str = f"Page {self._pageNumber} of {total_pages}"
        self.drawRightString(612 - 36, 22, page_str)

        self.restoreState()


def build_youtube_script_pdf(filename: str = "RookieStuff_YouTube_Script.pdf"):
    print(f"Starting YouTube Script PDF generation: {filename}")
    print(f"Total scenes to render: {len(SCENES)}")

    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=36,
        rightMargin=36,
        topMargin=36,
        bottomMargin=40,
    )

    styles = getSampleStyleSheet()

    # Typography styles
    main_title_style = ParagraphStyle(
        "ScriptMainTitle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=18,
        leading=22,
        textColor=colors.HexColor("#0d1117"),
        spaceAfter=4,
    )

    subtitle_style = ParagraphStyle(
        "ScriptSubtitle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=10,
        leading=13,
        textColor=colors.HexColor("#57606a"),
        spaceAfter=12,
    )

    scene_tag_style = ParagraphStyle(
        "SceneTag",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=8,
        leading=10,
        textColor=colors.HexColor("#cf222e"),
        spaceAfter=2,
    )

    scene_title_style = ParagraphStyle(
        "SceneTitle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=12,
        leading=15,
        textColor=colors.HexColor("#1f2328"),
        spaceAfter=6,
    )

    action_style = ParagraphStyle(
        "ActionCue",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=8,
        leading=11,
        textColor=colors.HexColor("#0969da"),
    )

    dialogue_style = ParagraphStyle(
        "DialogueText",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8.5,
        leading=11.6,
        textColor=colors.HexColor("#24292f"),
        spaceAfter=5,
        alignment=4,  # Justified
    )

    tip_style = ParagraphStyle(
        "PresenterTip",
        parent=styles["Normal"],
        fontName="Helvetica-Oblique",
        fontSize=7.5,
        leading=10,
        textColor=colors.HexColor("#6e7781"),
    )

    story = []

    # ----------------------------------------------------
    # SCRIPT COVER / HEADER BANNER
    # ----------------------------------------------------
    story.append(Paragraph("RookieStuff: Autonomous Code Review & Refactoring Agent", main_title_style))
    story.append(Paragraph("Complete 45-Minute YouTube Video Script  •  Word-for-Word Dialogue & Action Cues", subtitle_style))

    # Production Metadata Card
    meta_table_data = [
        [
            Paragraph("<b>Target Duration:</b> ~45 Minutes (6,800+ Words)", styles["Normal"]),
            Paragraph("<b>Host Style:</b> Conversational, High-Energy, Visual Tech Guide", styles["Normal"]),
        ],
        [
            Paragraph("<b>Core Tech Stack:</b> LangGraph, FastAPI, Docker, Flake8/Black", styles["Normal"]),
            Paragraph("<b>Local Server:</b> http://localhost:3000 (Live Review Dashboard)", styles["Normal"]),
        ],
        [
            Paragraph("<b>Repository:</b> https://github.com/sayan-kundu000/RookieStuff", styles["Normal"]),
            Paragraph("<b>Key Concept:</b> Human-in-the-Loop (HITL) Persistent Gate", styles["Normal"]),
        ],
    ]
    meta_table = Table(meta_table_data, colWidths=[270, 270])
    meta_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#f6f8fa")),
        ("BOX", (0, 0), (-1, -1), 1, colors.HexColor("#d0d7de")),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#e1e4e8")),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 14))

    # ----------------------------------------------------
    # RENDER 15 SCENES
    # ----------------------------------------------------
    for idx, scene in enumerate(SCENES):
        scene_num = scene["scene_num"]
        timecode = scene["timecode"]
        title = scene["title"]
        action = scene["action"]
        dialogue_paras = scene["dialogue"]
        tip = scene["presenter_tip"]

        # Scene Header
        story.append(Paragraph(f"SCENE {scene_num} OF 15  •  TIMECODE [{timecode}]", scene_tag_style))
        story.append(Paragraph(title, scene_title_style))

        # Action / Visual Cue Box
        action_table = Table([[Paragraph(action, action_style)]], colWidths=[540])
        action_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#ddf4ff")),
            ("BOX", (0, 0), (-1, -1), 1, colors.HexColor("#54aeff")),
            ("TOPPADDING", (0, 0), (-1, -1), 4),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ("LEFTPADDING", (0, 0), (-1, -1), 8),
            ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ]))
        story.append(action_table)
        story.append(Spacer(1, 6))

        # Dialogue Paragraphs
        for p_idx, text in enumerate(dialogue_paras):
            # Prepend speaker indicator on first paragraph
            lead = "<b>HOST (TO CAMERA):</b> " if p_idx == 0 else ""
            story.append(Paragraph(lead + text, dialogue_style))

        # Presenter Pro-Tip Callout
        tip_table = Table([[Paragraph(f"<b>💡 PRESENTER PRO-TIP:</b> {tip}", tip_style)]], colWidths=[540])
        tip_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#fff8c5")),
            ("BOX", (0, 0), (-1, -1), 0.75, colors.HexColor("#d4a72c")),
            ("TOPPADDING", (0, 0), (-1, -1), 3),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
            ("LEFTPADDING", (0, 0), (-1, -1), 8),
            ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ]))
        story.append(tip_table)
        story.append(Spacer(1, 12))

        # Divider between scenes except after the last scene
        if idx < len(SCENES) - 1:
            story.append(HRFlowable(
                width="100%",
                thickness=0.5,
                color=colors.HexColor("#d0d7de"),
                spaceBefore=4,
                spaceAfter=12,
            ))

    doc.build(story, canvasmaker=ScriptNumberedCanvas)
    print(f"Successfully generated {filename}")


if __name__ == "__main__":
    output_file = "RookieStuff_YouTube_Script.pdf"
    if len(sys.argv) > 1:
        output_file = sys.argv[1]
    build_youtube_script_pdf(output_file)

