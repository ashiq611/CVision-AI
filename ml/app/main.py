from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.gemini_service import parse_cv_with_gemini
from app.utils import extract_json

app = FastAPI(title="CVision AI - CV Parser ML Service")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

ALLOWED_MIME_TYPES = {
    "image/png",
    "image/jpeg",
    "image/jpg",
    "application/pdf",
}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/parse-cv")
async def parse_cv(file: UploadFile = File(...)):
    # 1) Validate mime type
    if file.content_type not in ALLOWED_MIME_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type: {file.content_type}. "
                   f"Supported: PNG, JPG, JPEG, PDF."
        )

    # 2) Read bytes
    document_bytes = await file.read()

    try:
        # 3) Call Gemini helper (handles image/pdf + multipage pdf)
        raw_response = parse_cv_with_gemini(
            document_bytes,
            mime_type=file.content_type,
            filename=file.filename,
        )
    except RuntimeError as e:
        # Custom error from gemini_service
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")

    # 4) Try to extract JSON from model text
    json_data = extract_json(raw_response)
    if not json_data:
        # give raw text for debugging
        return {
            "success": False,
            "parsed": None,
            "raw_text": raw_response,
            "note": "Could not parse strict JSON from Gemini response."
        }

    return {
        "success": True,
        "parsed": json_data
    }
