import os
import time

from dotenv import load_dotenv
from google import genai


# ==========================================
# LOAD ENVIRONMENT VARIABLES
# ==========================================

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError(
        "GEMINI_API_KEY is missing from the .env file."
    )


# ==========================================
# GEMINI CLIENT
# ==========================================

client = genai.Client(
    api_key=API_KEY
)


# ==========================================
# DOCUMENT GENERATOR
# ==========================================

class GeminiDocumentGenerator:

    def __init__(self):

        self.model = "gemini-3.8-flash"


    # ======================================
    # GENERATE DOCUMENT
    # ======================================

    def generate_document(
        self,
        document_type,
        parties,
        terms,
        dates
    ):

        # ----------------------------------
        # PROMPT
        # ----------------------------------

        prompt = f"""
You are an AI legal document drafting assistant.

Create a professional and well-structured
{document_type}.

PARTIES INVOLVED:
{parties}

TERMS AND CONDITIONS:
{terms}

EFFECTIVE DATE / DURATION:
{dates}

Instructions:

1. Create a complete professional document.
2. Use clear and formal language.
3. Add an appropriate document title.
4. Organize the document into logical sections.
5. Include the parties involved.
6. Include the effective date or duration.
7. Include all provided terms and conditions.
8. Do not invent important personal information.
9. Do not leave unnecessary placeholders.
10. Make the document easy to edit and read.
11. Use numbered sections where appropriate.
12. Return ONLY the document content.
"""


        # ==================================
        # RETRY SETTINGS
        # ==================================

        max_attempts = 3


        # ==================================
        # API REQUEST
        # ==================================

        for attempt in range(max_attempts):

            try:

                response = client.models.generate_content(
                    model=self.model,
                    contents=prompt
                )


                # ------------------------------
                # CHECK EMPTY RESPONSE
                # ------------------------------

                if not response.text:

                    raise Exception(
                        "Gemini returned an empty response."
                    )


                # ------------------------------
                # SUCCESS
                # ------------------------------

                return response.text


            except Exception as e:

                error_message = str(e)


                # ==================================
                # 429 - QUOTA EXCEEDED
                # ==================================

                if (
                    "429" in error_message
                    or "RESOURCE_EXHAUSTED" in error_message
                    or "quota" in error_message.lower()
                    or "quota exceeded" in error_message.lower()
                ):

                    raise Exception(
                        "Gemini API quota has been reached. "
                        "Your current Gemini Free Tier request "
                        "limit has been exceeded. "
                        "Please try again after the quota resets "
                        "or check your Gemini API usage and billing "
                        "settings."
                    )


                # ==================================
                # 503 - TEMPORARY SERVER BUSY
                # ==================================

                if (
                    "503" in error_message
                    or "UNAVAILABLE" in error_message
                    or "high demand" in error_message.lower()
                ):

                    if attempt < max_attempts - 1:

                        time.sleep(3)

                        continue


                    raise Exception(
                        "Gemini is temporarily busy. "
                        "Please wait a moment and click "
                        "Generate Document again."
                    )


                # ==================================
                # OTHER GEMINI ERRORS
                # ==================================

                raise Exception(
                    f"Gemini API Error: {error_message}"
                )