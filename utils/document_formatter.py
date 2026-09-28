from docx import Document
from docx.shared import Pt, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

from fpdf import FPDF

import os


# ==========================================
# PROJECT PATHS
# ==========================================

LOGO_PATH = os.path.join(
    "assets",
    "legalese_logo.png"
)


# ==========================================
# TEXT CLEANER
# ==========================================

def clean_text(text):
    """
    Clean common Unicode characters so that
    exported documents remain compatible.
    """

    replacements = {
        "’": "'",
        "‘": "'",
        "“": '"',
        "”": '"',
        "–": "-",
        "—": "-",
        "…": "...",
        "•": "-",
        "₹": "Rs.",
        "©": "(c)",
        "®": "(R)",
        "™": "(TM)",
        "\u00a0": " ",
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    return text


# ==========================================
# DOCX HELPER
# ==========================================

def set_cell_shading(cell, fill):
    """
    Set background colour of a DOCX table cell.
    """

    shading = OxmlElement("w:shd")

    shading.set(
        qn("w:fill"),
        fill
    )

    cell._tc.get_or_add_tcPr().append(
        shading
    )


# ==========================================
# DOCX FORMATTER
# ==========================================

def format_docx(text, doc_type):
    """
    Create a professionally formatted DOCX document.
    """

    document = Document()

    # --------------------------------------
    # PAGE SETUP
    # --------------------------------------

    section = document.sections[0]

    section.top_margin = Inches(0.7)
    section.bottom_margin = Inches(0.7)
    section.left_margin = Inches(0.8)
    section.right_margin = Inches(0.8)


    # --------------------------------------
    # DEFAULT FONT
    # --------------------------------------

    normal_style = document.styles["Normal"]

    normal_style.font.name = "Times New Roman"
    normal_style.font.size = Pt(12)

    normal_style._element.rPr.rFonts.set(
        qn("w:eastAsia"),
        "Times New Roman"
    )


    # ======================================
    # LOGO
    # ======================================

    if os.path.exists(LOGO_PATH):

        logo_paragraph = document.add_paragraph()

        logo_paragraph.alignment = (
            WD_ALIGN_PARAGRAPH.CENTER
        )

        logo_run = logo_paragraph.add_run()

        logo_run.add_picture(
            LOGO_PATH,
            width=Inches(3.2)
        )


    # ======================================
    # DOCUMENT TITLE
    # ======================================

    title_paragraph = document.add_paragraph()

    title_paragraph.alignment = (
        WD_ALIGN_PARAGRAPH.CENTER
    )

    title_run = title_paragraph.add_run(
        clean_text(doc_type).upper()
    )

    title_run.bold = True
    title_run.font.name = "Times New Roman"
    title_run.font.size = Pt(17)

    title_run._element.rPr.rFonts.set(
        qn("w:eastAsia"),
        "Times New Roman"
    )


    # Space after title
    title_paragraph.paragraph_format.space_after = Pt(10)


    # ======================================
    # SEPARATOR
    # ======================================

    separator = document.add_paragraph()

    separator.alignment = (
        WD_ALIGN_PARAGRAPH.CENTER
    )

    separator_run = separator.add_run(
        "________________________________________"
    )

    separator_run.font.name = "Times New Roman"
    separator_run.font.size = Pt(10)


    # ======================================
    # DOCUMENT CONTENT
    # ======================================

    lines = text.splitlines()


    for line in lines:

        line = clean_text(line.strip())


        # Empty line
        if not line:

            empty_paragraph = document.add_paragraph()

            empty_paragraph.paragraph_format.space_after = Pt(3)

            continue


        # ----------------------------------
        # Detect headings
        # ----------------------------------

        is_heading = False


        if line.isupper() and len(line) < 100:

            is_heading = True


        if (
            line.startswith("1.")
            or line.startswith("2.")
            or line.startswith("3.")
            or line.startswith("4.")
            or line.startswith("5.")
            or line.startswith("6.")
            or line.startswith("7.")
            or line.startswith("8.")
            or line.startswith("9.")
        ):

            is_heading = True


        if is_heading:

            paragraph = document.add_paragraph()

            paragraph.paragraph_format.space_before = Pt(8)
            paragraph.paragraph_format.space_after = Pt(5)

            run = paragraph.add_run(line)

            run.bold = True
            run.font.name = "Times New Roman"
            run.font.size = Pt(12)

            run._element.rPr.rFonts.set(
                qn("w:eastAsia"),
                "Times New Roman"
            )

            continue


        # ----------------------------------
        # Normal paragraph
        # ----------------------------------

        paragraph = document.add_paragraph()

        paragraph.alignment = (
            WD_ALIGN_PARAGRAPH.JUSTIFY
        )

        paragraph.paragraph_format.line_spacing = 1.15
        paragraph.paragraph_format.space_after = Pt(6)

        run = paragraph.add_run(line)

        run.font.name = "Times New Roman"
        run.font.size = Pt(12)

        run._element.rPr.rFonts.set(
            qn("w:eastAsia"),
            "Times New Roman"
        )


    # ======================================
    # TERMS TABLE
    # ======================================

    # If the original input contains
    # semicolon-separated terms, create
    # a clean table from them.

    # We only create the table when
    # multiple semicolon-separated items
    # are detected.

    semicolon_items = [
        item.strip()
        for item in text.split(";")
        if item.strip()
    ]


    if len(semicolon_items) >= 3:

        document.add_paragraph()

        table_title = document.add_paragraph()

        table_title_run = table_title.add_run(
            "KEY TERMS"
        )

        table_title_run.bold = True
        table_title_run.font.name = "Times New Roman"
        table_title_run.font.size = Pt(12)


        table = document.add_table(
            rows=1,
            cols=2
        )

        table.alignment = (
            WD_TABLE_ALIGNMENT.CENTER
        )

        table.style = "Table Grid"


        # Header
        header_cells = table.rows[0].cells

        header_cells[0].text = "No."
        header_cells[1].text = "Term / Condition"


        for cell in header_cells:

            set_cell_shading(
                cell,
                "D9E2F3"
            )

            cell.vertical_alignment = (
                WD_CELL_VERTICAL_ALIGNMENT.CENTER
            )

            for paragraph in cell.paragraphs:

                paragraph.alignment = (
                    WD_ALIGN_PARAGRAPH.CENTER
                )

                for run in paragraph.runs:

                    run.bold = True
                    run.font.name = "Times New Roman"
                    run.font.size = Pt(11)


        # Rows
        for index, item in enumerate(
            semicolon_items,
            start=1
        ):

            cells = table.add_row().cells

            cells[0].text = str(index)
            cells[1].text = item

            for cell in cells:

                cell.vertical_alignment = (
                    WD_CELL_VERTICAL_ALIGNMENT.CENTER
                )

                for paragraph in cell.paragraphs:

                    for run in paragraph.runs:

                        run.font.name = "Times New Roman"
                        run.font.size = Pt(10)


    # ======================================
    # FOOTER
    # ======================================

    footer = section.footer

    footer_paragraph = footer.paragraphs[0]

    footer_paragraph.alignment = (
        WD_ALIGN_PARAGRAPH.CENTER
    )

    footer_run = footer_paragraph.add_run(
        "LegalEase | AI-Powered Legal Document Generator"
    )

    footer_run.font.name = "Times New Roman"
    footer_run.font.size = Pt(9)


    # ======================================
    # RETURN DOCX
    # ======================================

    return document


# ==========================================
# PDF FORMATTER
# ==========================================

class LegalEasePDF(FPDF):

    def __init__(self, logo_path):

        super().__init__()

        self.logo_path = logo_path

        self.set_auto_page_break(
            auto=True,
            margin=22
        )


    # --------------------------------------
    # HEADER
    # --------------------------------------

    def header(self):

        if os.path.exists(self.logo_path):

            try:

                self.image(
                    self.logo_path,
                    x=75,
                    y=8,
                    w=60
                )

                self.ln(27)

            except Exception:

                self.set_font(
                    "Helvetica",
                    "B",
                    15
                )

                self.cell(
                    0,
                    10,
                    "LegalEase",
                    align="C"
                )

                self.ln(12)

        else:

            self.set_font(
                "Helvetica",
                "B",
                15
            )

            self.cell(
                0,
                10,
                "LegalEase",
                align="C"
            )

            self.ln(12)


    # --------------------------------------
    # FOOTER
    # --------------------------------------

    def footer(self):

        self.set_y(-15)

        self.set_font(
            "Helvetica",
            "",
            8
        )

        self.cell(
            0,
            8,
            "LegalEase | AI-Powered Legal Document Generator",
            align="C"
        )


# ==========================================
# PDF FORMATTER
# ==========================================

def format_pdf(text, doc_type):
    """
    Create a professional branded PDF.
    """

    pdf = LegalEasePDF(
        LOGO_PATH
    )

    pdf.add_page()


    # ======================================
    # DOCUMENT TITLE
    # ======================================

    pdf.set_font(
        "Helvetica",
        "B",
        15
    )

    safe_doc_type = clean_text(
        doc_type
    )

    pdf.multi_cell(
        0,
        9,
        safe_doc_type.upper(),
        align="C"
    )

    pdf.ln(5)


    # Separator
    pdf.set_font(
        "Helvetica",
        "",
        8
    )

    pdf.cell(
        0,
        5,
        "____________________________________________",
        align="C"
    )

    pdf.ln(8)


    # ======================================
    # DOCUMENT CONTENT
    # ======================================

    clean_document = clean_text(
        text
    )


    for line in clean_document.splitlines():

        line = line.strip()


        # Empty line
        if not line:

            pdf.ln(4)

            continue


        # ----------------------------------
        # Heading detection
        # ----------------------------------

        is_heading = False


        if line.isupper() and len(line) < 100:

            is_heading = True


        if (
            line.startswith("1.")
            or line.startswith("2.")
            or line.startswith("3.")
            or line.startswith("4.")
            or line.startswith("5.")
            or line.startswith("6.")
            or line.startswith("7.")
            or line.startswith("8.")
            or line.startswith("9.")
        ):

            is_heading = True


        if is_heading:

            pdf.set_font(
                "Helvetica",
                "B",
                11
            )

            pdf.multi_cell(
                0,
                7,
                line
            )

            pdf.ln(2)

        else:

            pdf.set_font(
                "Helvetica",
                "",
                10
            )

            pdf.multi_cell(
                0,
                6,
                line
            )

            pdf.ln(2)


    # ======================================
    # KEY TERMS
    # ======================================

    semicolon_items = [
        item.strip()
        for item in clean_document.split(";")
        if item.strip()
    ]


    if len(semicolon_items) >= 3:

        pdf.ln(5)

        pdf.set_font(
            "Helvetica",
            "B",
            11
        )

        pdf.cell(
            0,
            8,
            "KEY TERMS",
            ln=True
        )


        # Table header
        pdf.set_font(
            "Helvetica",
            "B",
            9
        )

        pdf.cell(
            15,
            8,
            "No.",
            border=1,
            align="C"
        )

        pdf.cell(
            165,
            8,
            "Term / Condition",
            border=1,
            align="C"
        )

        pdf.ln()


        # Table rows
        pdf.set_font(
            "Helvetica",
            "",
            8
        )


        for index, item in enumerate(
            semicolon_items,
            start=1
        ):

            # Simple table row
            pdf.cell(
                15,
                7,
                str(index),
                border=1,
                align="C"
            )

            pdf.cell(
                165,
                7,
                item[:120],
                border=1
            )

            pdf.ln()


    return pdf