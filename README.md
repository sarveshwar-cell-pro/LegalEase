# LegalEase

## AI-Powered Legal Document Generator

LegalEase is an AI-powered web application that helps users generate customizable legal documents using Generative AI.

The application provides a simple interface where users can enter document details, generate a legal document, edit the generated content, preview it, and export it into different file formats.

---

## Features

- Generate legal documents using AI
- Support for different document types
- Enter parties, terms, and effective dates
- Editable document preview
- Download documents as TXT
- Download documents as DOCX
- Download documents as PDF
- Professional document formatting
- LegalEase branding and logo
- FastAPI backend
- Streamlit frontend
- Gemini AI integration
- Error handling for API problems and quota limits

---

## Technologies Used

- Python
- Streamlit
- FastAPI
- Google Gemini API
- python-docx
- FPDF
- Pillow
- Requests
- python-dotenv

---

## Project Structure

```text
LegalEase/
│
├── ai_core/
│   ├── __init__.py
│   └── gemini_generator.py
│
├── utils/
│   ├── __init__.py
│   ├── document_formatter.py
│   └── text_utils.py
│
├── assets/
│   └── legalese_logo.png
│
├── app.py
├── main.py
├── routes.py
├── requirements.txt
├── .env
├── .gitignore
└── README.md