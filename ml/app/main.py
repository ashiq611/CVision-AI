from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from app.gemini_service import parse_cv_with_gemini
from app.utils import extract_json
from app.schemas import CVResponse

app = FastAPI(title="CV Parser ML Service")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/parse-cv", response_model=CVResponse)
async def parse_cv(file: UploadFile = File(...)):
    image_bytes = await file.read()
    raw_response = parse_cv_with_gemini(image_bytes, file.content_type)

    json_data = extract_json(raw_response)
    if not json_data:
        return {"error": "Failed to parse JSON", "raw": raw_response}

    return json_data
