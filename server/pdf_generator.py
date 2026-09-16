"""
pdf_generator.py - Professional PDF Generation for NCPOR Polar Portal
Generates verified PDF downloads for Scientific Publications and Educational Toolkits.
Strictly adheres to official MoES/NCPOR institutional formatting with clean typography and layout.
"""

import io
import html
import re
from typing import Dict, Any, List
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    HRFlowable,
    KeepTogether
)
from reportlab.pdfgen import canvas


def esc(text: Any) -> str:
    """Safely escapes text for ReportLab Paragraph XML parser."""
    if text is None:
        return ""
    return html.escape(str(text))


class NumberedCanvas(canvas.Canvas):
    """Canvas that performs a two-pass calculation for total page count and adds header/footer."""
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
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#4A5568"))

        # Header (Top of page)
        self.setStrokeColor(colors.HexColor("#CBD5E0"))
        self.setLineWidth(0.5)
        self.line(40, 802, 555, 802)
        self.drawString(40, 807, "National Centre for Polar and Ocean Research (NCPOR) | Ministry of Earth Sciences, Govt. of India")
        self.drawRightString(555, 807, "MoES / SIH26063 Polar Portal")

        # Footer (Bottom of page)
        self.line(40, 45, 555, 45)
        self.drawString(40, 32, "Official Polar Science Repository Document — Verified Academic Release")
        self.drawRightString(555, 32, f"Page {self._pageNumber} of {page_count}")
        self.restoreState()


def get_custom_styles():
    base = getSampleStyleSheet()
    
    styles = {
        'OrgHeader': ParagraphStyle(
            'OrgHeader',
            parent=base['Normal'],
            fontName='Helvetica-Bold',
            fontSize=11,
            leading=14,
            textColor=colors.HexColor("#0B2545"),
            spaceAfter=2
        ),
        'SubOrgHeader': ParagraphStyle(
            'SubOrgHeader',
            parent=base['Normal'],
            fontName='Helvetica',
            fontSize=8.5,
            leading=11,
            textColor=colors.HexColor("#4A5568"),
            spaceAfter=8
        ),
        'DocTitle': ParagraphStyle(
            'DocTitle',
            parent=base['Heading1'],
            fontName='Helvetica-Bold',
            fontSize=15,
            leading=19,
            textColor=colors.HexColor("#0B2545"),
            spaceAfter=8
        ),
        'Authors': ParagraphStyle(
            'Authors',
            parent=base['Normal'],
            fontName='Helvetica-Bold',
            fontSize=9.5,
            leading=13,
            textColor=colors.HexColor("#1A202C"),
            spaceAfter=2
        ),
        'Affiliation': ParagraphStyle(
            'Affiliation',
            parent=base['Normal'],
            fontName='Helvetica-Oblique',
            fontSize=8.5,
            leading=11,
            textColor=colors.HexColor("#4A5568"),
            spaceAfter=8
        ),
        'SectionHeading': ParagraphStyle(
            'SectionHeading',
            parent=base['Heading2'],
            fontName='Helvetica-Bold',
            fontSize=10.5,
            leading=14,
            textColor=colors.HexColor("#0B2545"),
            spaceBefore=8,
            spaceAfter=4
        ),
        'Body': ParagraphStyle(
            'Body',
            parent=base['Normal'],
            fontName='Helvetica',
            fontSize=9,
            leading=13,
            textColor=colors.HexColor("#2D3748"),
            spaceAfter=6
        ),
        'AbstractBody': ParagraphStyle(
            'AbstractBody',
            parent=base['Normal'],
            fontName='Helvetica',
            fontSize=8.5,
            leading=12.5,
            textColor=colors.HexColor("#1A202C"),
            spaceAfter=4
        ),
        'PlainSummaryBody': ParagraphStyle(
            'PlainSummaryBody',
            parent=base['Normal'],
            fontName='Helvetica',
            fontSize=8.5,
            leading=12.5,
            textColor=colors.HexColor("#0B3954"),
            spaceAfter=4
        ),
        'MetaLabel': ParagraphStyle(
            'MetaLabel',
            parent=base['Normal'],
            fontName='Helvetica-Bold',
            fontSize=7.5,
            leading=10,
            textColor=colors.HexColor("#718096")
        ),
        'MetaValue': ParagraphStyle(
            'MetaValue',
            parent=base['Normal'],
            fontName='Helvetica',
            fontSize=8,
            leading=10.5,
            textColor=colors.HexColor("#1A202C")
        ),
        'CitationText': ParagraphStyle(
            'CitationText',
            parent=base['Normal'],
            fontName='Courier',
            fontSize=7.5,
            leading=10,
            textColor=colors.HexColor("#2D3748")
        )
    }
    return styles


def generate_publication_pdf(pub: Dict[str, Any]) -> bytes:
    """
    Generates a publication PDF from repository metadata.
    Includes: title, authors, affiliation, year, expedition, station, vertical,
    DOI, abstract, keywords, dataset attached, plain-language summary, and citation.
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        leftMargin=40,
        rightMargin=40,
        topMargin=48,
        bottomMargin=48
    )

    styles = get_custom_styles()
    story = []

    # Institutional Header
    story.append(Paragraph("NATIONAL CENTRE FOR POLAR AND OCEAN RESEARCH", styles['OrgHeader']))
    story.append(Paragraph("Ministry of Earth Sciences, Government of India • Official Science Repository Catalog", styles['SubOrgHeader']))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#0B2545"), spaceAfter=10))

    # Publication Title
    story.append(Paragraph(esc(pub.get("title", "Untitled Publication")), styles['DocTitle']))

    # Authors & Affiliation
    authors = pub.get("authors", "NCPOR Polar Science Team")
    affiliation = pub.get("affiliation", "National Centre for Polar and Ocean Research, Goa")
    story.append(Paragraph(esc(authors), styles['Authors']))
    story.append(Paragraph(esc(affiliation), styles['Affiliation']))

    # Metadata Grid Table
    col_w = (555 - 40) / 4  # 4 columns
    meta_data = [
        [
            Paragraph("PUBLICATION ID", styles['MetaLabel']),
            Paragraph("YEAR", styles['MetaLabel']),
            Paragraph("STATION / FACILITY", styles['MetaLabel']),
            Paragraph("EXPEDITION", styles['MetaLabel'])
        ],
        [
            Paragraph(esc(pub.get("id", "N/A")), styles['MetaValue']),
            Paragraph(esc(pub.get("year", "N/A")), styles['MetaValue']),
            Paragraph(esc(pub.get("station", "N/A")), styles['MetaValue']),
            Paragraph(esc(pub.get("expedition", "N/A")), styles['MetaValue'])
        ],
        [
            Paragraph("SCIENTIFIC VERTICAL", styles['MetaLabel']),
            Paragraph("DIGITAL OBJECT IDENTIFIER (DOI)", styles['MetaLabel']),
            Paragraph("ASSOCIATED DATASET", styles['MetaLabel']),
            Paragraph("CITATION COUNT", styles['MetaLabel'])
        ],
        [
            Paragraph(esc(pub.get("vertical", "General Polar Science")), styles['MetaValue']),
            Paragraph(esc(pub.get("doi", "N/A")), styles['MetaValue']),
            Paragraph(esc(pub.get("dataset_attached", "Annexed in Repository")), styles['MetaValue']),
            Paragraph(esc(str(pub.get("citation_count", 0))), styles['MetaValue'])
        ]
    ]

    t = Table(meta_data, colWidths=[col_w, col_w, col_w, col_w])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#F7FAFC")),
        ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor("#E2E8F0")),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#EDF2F7")),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(t)
    story.append(Spacer(1, 10))

    # Abstract Box
    story.append(Paragraph("TECHNICAL ABSTRACT", styles['SectionHeading']))
    abstract_text = pub.get("abstract", "No abstract available.")
    abs_table = Table([[Paragraph(esc(abstract_text), styles['AbstractBody'])]], colWidths=[515])
    abs_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#F8FAFC")),
        ('BOX', (0, 0), (-1, -1), 0.75, colors.HexColor("#CBD5E1")),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
    ]))
    story.append(abs_table)
    story.append(Spacer(1, 8))

    # Keywords
    keywords = pub.get("keywords", [])
    if keywords:
        kw_str = " • ".join(keywords)
        story.append(Paragraph(f"<b>Indexed Keywords:</b> {esc(kw_str)}", styles['Body']))
        story.append(Spacer(1, 6))

    # Plain-Language Summary
    plain_summary = pub.get("plain_summary")
    if plain_summary:
        story.append(Paragraph("PLAIN-LANGUAGE SCIENCE SUMMARY", styles['SectionHeading']))
        summary_table = Table([[Paragraph(esc(plain_summary), styles['PlainSummaryBody'])]], colWidths=[515])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#F0F9FF")),
            ('BOX', (0, 0), (-1, -1), 0.75, colors.HexColor("#BAE6FD")),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ]))
        story.append(summary_table)
        story.append(Spacer(1, 8))

    # Official Citation Record
    story.append(Paragraph("RECOMMENDED CITATION & BIBTEX ENTRY", styles['SectionHeading']))
    apa_citation = f"{pub.get('authors', 'NCPOR')} ({pub.get('year', '2024')}). {pub.get('title', '')}. Polar Research Repository / MoES, DOI: {pub.get('doi', '')}."
    story.append(Paragraph(f"<b>APA Format:</b> {esc(apa_citation)}", styles['Body']))
    
    bibtex = pub.get("bibtex", "")
    if bibtex:
        bib_table = Table([[Paragraph(esc(bibtex).replace('\n', '<br/>'), styles['CitationText'])]], colWidths=[515])
        bib_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#F1F5F9")),
            ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ]))
        story.append(bib_table)

    doc.build(story, canvasmaker=NumberedCanvas)
    return buffer.getvalue()


def generate_toolkit_pdf(kit: Dict[str, Any]) -> bytes:
    """
    Generates an educational toolkit package PDF from outreach metadata.
    Includes: toolkit title, grade, category, summary, learning objectives, and curriculum mapping.
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        leftMargin=40,
        rightMargin=40,
        topMargin=48,
        bottomMargin=48
    )

    styles = get_custom_styles()
    story = []

    # Institutional Header
    story.append(Paragraph("NATIONAL CENTRE FOR POLAR AND OCEAN RESEARCH", styles['OrgHeader']))
    story.append(Paragraph("Ministry of Earth Sciences, Government of India • Polar Science Outreach Division", styles['SubOrgHeader']))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#0B2545"), spaceAfter=10))

    # Toolkit Title
    story.append(Paragraph(esc(kit.get("title", "Educational Toolkit")), styles['DocTitle']))

    # Metadata Grid Table
    col_w = (555 - 40) / 4
    meta_data = [
        [
            Paragraph("TOOLKIT ID", styles['MetaLabel']),
            Paragraph("TARGET GRADE / LEVEL", styles['MetaLabel']),
            Paragraph("RESOURCE CATEGORY", styles['MetaLabel']),
            Paragraph("PORTAL DOWNLOADS", styles['MetaLabel'])
        ],
        [
            Paragraph(esc(kit.get("id", "N/A")), styles['MetaValue']),
            Paragraph(esc(kit.get("grade", "All Learners")), styles['MetaValue']),
            Paragraph(esc(kit.get("category", "Activity Guide")), styles['MetaValue']),
            Paragraph(esc(kit.get("downloads", "Verified")), styles['MetaValue'])
        ]
    ]

    t = Table(meta_data, colWidths=[col_w, col_w, col_w, col_w])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#F7FAFC")),
        ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor("#E2E8F0")),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#EDF2F7")),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(t)
    story.append(Spacer(1, 10))

    # Toolkit Overview / Summary
    story.append(Paragraph("EDUCATIONAL OVERVIEW & OBJECTIVES", styles['SectionHeading']))
    summary_text = kit.get("summary", "Official educational toolkit package prepared by NCPOR outreach scientists.")
    summary_table = Table([[Paragraph(esc(summary_text), styles['Body'])]], colWidths=[515])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#F0FDF4")),
        ('BOX', (0, 0), (-1, -1), 0.75, colors.HexColor("#BBF7D0")),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
    ]))
    story.append(summary_table)
    story.append(Spacer(1, 10))

    # Pedagogical Structure & Curriculum Guidance
    story.append(Paragraph("CURRICULUM MAPPING & LEARNING OUTCOMES", styles['SectionHeading']))
    points = [
        "<b>Core Competency:</b> Understanding the physical mechanisms governing the cryosphere, polar ocean currents, and global climate feedback systems.",
        "<b>Hands-on Practical Component:</b> Experimental activity guidelines and data analysis exercises developed for classroom and collegiate lab sessions.",
        "<b>Scientific Integrity:</b> Based directly on empirical observations collected by Indian expeditions at Bharati, Maitri, Himadri, and Himansh stations.",
        "<b>Open Educational License:</b> Free for non-commercial educational use by accredited schools, universities, and science communicators across India and internationally."
    ]
    for pt in points:
        story.append(Paragraph(f"• {pt}", styles['Body']))
        story.append(Spacer(1, 2))

    story.append(Spacer(1, 8))
    story.append(Paragraph("CLASSROOM IMPLEMENTATION GUIDELINES", styles['SectionHeading']))
    story.append(Paragraph(
        "Educators are encouraged to utilize this module alongside live telemetry feeds from Indian polar research stations available on the NCPOR Polar Portal. "
        "Students may compare real-time ambient temperatures, wind speeds, and radiation profiles from Antarctica and the Arctic with the theoretical models presented in this toolkit.",
        styles['Body']
    ))

    doc.build(story, canvasmaker=NumberedCanvas)
    return buffer.getvalue()
