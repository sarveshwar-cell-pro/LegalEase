from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from ai_core.gemini_generator import GeminiDocumentGenerator


# Create router
router = APIRouter()


# Create Gemini generator
generator = GeminiDocumentGenerator()


# ==========================================
# REQUEST MODEL
# ==========================================

class DocumentRequest(BaseModel):

    document_type: str

    parties: str

    terms: str

    dates: str


# ==========================================
# GENERATE DOCUMENT
# ==========================================

@router.post("/generate")
def generate_document(
    request: DocumentRequest
):

    try:

        document = generator.generate_document(

            document_type=request.document_type,

            parties=request.parties,

            terms=request.terms,

            dates=request.dates
        )


        return {

            "document_type": request.document_type,

            "document": document
        }


    except Exception as e:

        # Show the real error
        raise HTTPException(

            status_code=500,

            detail=str(e)
        )