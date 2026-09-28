import streamlit as st
import requests
from io import BytesIO
import html
import os

from utils.document_formatter import format_docx, format_pdf


# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="LegalEase",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ==========================================
# PATHS
# ==========================================

logo_path = os.path.join(
    "assets",
    "legalese_logo.png"
)


# ==========================================
# CUSTOM CSS
# ==========================================

st.markdown(
    """
    <style>

    /* =====================================
       GENERAL PAGE
       ===================================== */

    .main {
        padding-top: 1rem;
        padding-bottom: 2rem;
    }


    /* =====================================
       HEADER
       ===================================== */

    .hero-title {
        text-align: center;
        font-size: 42px;
        font-weight: 700;
        margin-top: 5px;
        margin-bottom: 5px;
    }

    .hero-subtitle {
        text-align: center;
        font-size: 17px;
        margin-bottom: 25px;
    }


    /* =====================================
       SECTION HEADINGS
       ===================================== */

    .section-title {
        font-size: 25px;
        font-weight: 700;
        margin-top: 10px;
        margin-bottom: 5px;
    }

    .section-description {
        font-size: 14px;
        margin-bottom: 18px;
    }


    /* =====================================
       PREVIEW BOX
       ===================================== */

    .preview-box {
        padding: 30px;
        border-radius: 14px;
        border: 1px solid #d9d9d9;
        background-color: #f8f9fa;
        line-height: 1.8;
        white-space: pre-wrap;
        min-height: 300px;
        font-size: 15px;
    }


    /* =====================================
       INFO CARD
       ===================================== */

    .info-card {
        padding: 18px;
        border-radius: 12px;
        border: 1px solid #dddddd;
        margin-top: 10px;
        margin-bottom: 20px;
    }


    /* =====================================
       DOWNLOAD AREA
       ===================================== */

    .download-title {
        font-size: 22px;
        font-weight: 700;
        margin-bottom: 12px;
    }


    /* =====================================
       FOOTER
       ===================================== */

    .footer {
        text-align: center;
        margin-top: 45px;
        padding-top: 20px;
        padding-bottom: 20px;
        font-size: 13px;
    }


    /* =====================================
       SMALL SCREEN
       ===================================== */

    @media (max-width: 768px) {

        .hero-title {
            font-size: 30px;
        }

        .hero-subtitle {
            font-size: 15px;
        }

        .preview-box {
            padding: 20px;
        }

    }

    </style>
    """,
    unsafe_allow_html=True
)


# ==========================================
# BRAND HEADER
# ==========================================

if os.path.exists(logo_path):

    logo_left, logo_center, logo_right = st.columns(
        [1, 2, 1]
    )

    with logo_center:

        st.image(
            logo_path,
            use_container_width=True
        )

else:

    st.markdown(
        """
        <div class="hero-title">
            ⚖️ LegalEase
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="hero-subtitle">
            AI-Powered Legal Document Generator
        </div>
        """,
        unsafe_allow_html=True
    )


# ==========================================
# INTRODUCTION
# ==========================================

st.info(
    "Create customizable legal documents by providing "
    "the document type, parties, terms and effective date."
)


# ==========================================
# DOCUMENT DETAILS
# ==========================================

st.markdown(
    '<div class="section-title">📋 Document Details</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-description">'
    'Enter the basic information required to generate your document.'
    '</div>',
    unsafe_allow_html=True
)


col1, col2 = st.columns(
    2,
    gap="large"
)


# ==========================================
# LEFT COLUMN
# ==========================================

with col1:

    document_type = st.text_input(
        "Document Type",
        placeholder="Example: Employment Agreement"
    )

    parties = st.text_area(
        "Parties Involved",
        placeholder=(
            "Example: Employer: ABC Technologies; "
            "Employee: John Doe"
        ),
        height=150
    )


# ==========================================
# RIGHT COLUMN
# ==========================================

with col2:

    dates = st.text_input(
        "Effective Date / Duration",
        placeholder=(
            "Example: 1 October 2026; Duration: 1 year"
        )
    )

    terms = st.text_area(
        "Terms and Conditions",
        placeholder=(
            "Example: Full-time employment; "
            "Monthly salary Rs. 40,000; Confidentiality"
        ),
        height=150
    )


# ==========================================
# GENERATE BUTTON
# ==========================================

st.markdown("")

generate = st.button(
    "✨ Generate Document",
    type="primary",
    use_container_width=True
)


# ==========================================
# GENERATE DOCUMENT
# ==========================================

if generate:

    if (
        not document_type
        or not parties
        or not terms
        or not dates
    ):

        st.warning(
            "Please fill in all the fields before generating the document."
        )

    else:

        payload = {
            "document_type": document_type,
            "parties": parties,
            "terms": terms,
            "dates": dates
        }


        try:

            with st.spinner(
                "Generating your legal document..."
            ):

                response = requests.post(
                    "http://127.0.0.1:8000/generate",
                    json=payload,
                    timeout=120
                )


            # ==================================
            # SUCCESS
            # ==================================

            if response.status_code == 200:

                result = response.json()

                st.session_state["document"] = (
                    result["document"]
                )

                st.session_state["document_type"] = (
                    document_type
                )

                st.success(
                    "Document generated successfully!"
                )


            # ==================================
            # BACKEND ERROR
            # ==================================

            else:

                st.error(
                    f"Backend error: {response.status_code}"
                )

                try:

                    error_data = response.json()

                    detail = error_data.get(
                        "detail",
                        "Unknown backend error."
                    )


                    # Friendly quota message
                    if (
                        "quota" in detail.lower()
                        or "429" in detail
                        or "resource_exhausted"
                        in detail.lower()
                    ):

                        st.warning(
                            "Gemini API quota has been reached. "
                            "Please try again after your Gemini "
                            "quota becomes available."
                        )

                    else:

                        st.error(detail)


                except Exception:

                    st.error(
                        response.text
                    )


        # ======================================
        # CONNECTION ERROR
        # ======================================

        except requests.exceptions.ConnectionError:

            st.error(
                "Could not connect to the FastAPI backend."
            )

            st.info(
                "Make sure FastAPI is running with:"
            )

            st.code(
                "uvicorn main:app --reload"
            )


        # ======================================
        # OTHER ERROR
        # ======================================

        except Exception as e:

            st.error(
                f"Error: {str(e)}"
            )


# ==========================================
# GENERATED DOCUMENT
# ==========================================

if "document" in st.session_state:

    st.divider()


    # ======================================
    # DOCUMENT PREVIEW
    # ======================================

    st.markdown(
        '<div class="section-title">📄 Generated Document</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-description">'
        'Review the generated document before downloading it.'
        '</div>',
        unsafe_allow_html=True
    )


    st.markdown(
        "### 👁️ Document Preview"
    )


    safe_document = html.escape(
        st.session_state["document"]
    )


    safe_title = html.escape(
        st.session_state.get(
            "document_type",
            "Legal Document"
        ).upper()
    )


    preview_html = f"""
    <div class="preview-box">

        <strong>
            {safe_title}
        </strong>

        <br><br>

        {safe_document}

    </div>
    """


    st.markdown(
        preview_html,
        unsafe_allow_html=True
    )


    # ======================================
    # EDIT DOCUMENT
    # ======================================

    st.markdown(
        "### ✏️ Edit Document"
    )


    edited_document = st.text_area(

        "Modify the generated document if required:",

        value=st.session_state["document"],

        height=500,

        key="document_editor"
    )


    st.session_state["document"] = (
        edited_document
    )


    # ======================================
    # DOWNLOAD SECTION
    # ======================================

    st.divider()


    st.markdown(
        '<div class="download-title">'
        '⬇️ Download Document'
        '</div>',
        unsafe_allow_html=True
    )


    st.caption(
        "Choose a format to save your document."
    )


    download_col1, download_col2, download_col3 = (
        st.columns(3, gap="medium")
    )


    # ======================================
    # TXT DOWNLOAD
    # ======================================

    with download_col1:

        st.download_button(

            label="📄 Download TXT",

            data=st.session_state["document"],

            file_name="LegalEase_Document.txt",

            mime="text/plain",

            use_container_width=True
        )


    # ======================================
    # DOCX DOWNLOAD
    # ======================================

    with download_col2:

        try:

            docx_document = format_docx(

                st.session_state["document"],

                st.session_state.get(
                    "document_type",
                    "Legal Document"
                )
            )


            docx_buffer = BytesIO()


            docx_document.save(
                docx_buffer
            )


            docx_buffer.seek(0)


            st.download_button(

                label="📝 Download DOCX",

                data=docx_buffer.getvalue(),

                file_name="LegalEase_Document.docx",

                mime=(
                    "application/vnd.openxmlformats-"
                    "officedocument.wordprocessingml.document"
                ),

                use_container_width=True
            )


        except Exception as e:

            st.error(
                f"DOCX error: {str(e)}"
            )


    # ======================================
    # PDF DOWNLOAD
    # ======================================

    with download_col3:

        try:

            pdf_document = format_pdf(

                st.session_state["document"],

                st.session_state.get(
                    "document_type",
                    "Legal Document"
                )
            )


            pdf_data = pdf_document.output(
                dest="S"
            )


            if isinstance(
                pdf_data,
                str
            ):

                pdf_data = pdf_data.encode(
                    "latin-1"
                )


            pdf_buffer = BytesIO(
                pdf_data
            )


            pdf_buffer.seek(0)


            st.download_button(

                label="📕 Download PDF",

                data=pdf_buffer.getvalue(),

                file_name="LegalEase_Document.pdf",

                mime="application/pdf",

                use_container_width=True
            )


        except Exception as e:

            st.error(
                f"PDF error: {str(e)}"
            )


# ==========================================
# DISCLAIMER
# ==========================================

st.divider()

st.caption(
    "⚖️ LegalEase generates AI-assisted legal documents. "
    "Review the generated content carefully before using "
    "it for any real legal purpose."
)


# ==========================================
# FOOTER
# ==========================================

st.markdown(
    """
    <div class="footer">
        LegalEase • AI-Powered Legal Document Generator
    </div>
    """,
    unsafe_allow_html=True
)