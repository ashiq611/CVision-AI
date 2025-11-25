import tempfile
import os

import google.generativeai as genai
import google.api_core.exceptions as gexc

from app.config import GEMINI_API_KEY, GEMINI_MODEL

genai.configure(api_key=GEMINI_API_KEY)


def _build_prompt() -> str:
    # Same prompt, but wording ektu generic “document” kore dilam
    return """
You are an assistant that extracts structured CV/resume data from a document.
The document may be:
- A single-page or multi-page PDF
- A PNG/JPG/JPEG image of a CV (possibly multi-page if PDF)

Read ALL pages of the document and return ONLY valid JSON with this exact shape:

{
  "name": string | null,
  "email": string | null,
  "phone": string | null,
  "summary": string | null,
  "education": [
    {
      "degree": string | null,
      "institution": string | null,
      "start_year": string | null,
      "end_year": string | null
    }
  ],
  "work_experience": [
    {
      "title": string | null,
      "company": string | null,
      "start": string | null,
      "end": string | null,
      "description": string | null
    }
  ],
  "skills": [string],
  "certifications": [string],
  "languages": [string],
  "address": string | null,
  "other": {}
}

Rules:
- Analyse ALL pages together and merge into ONE combined JSON.
- If any field is missing, use null (or empty arrays where applicable).
- Dates should be in 'YYYY' or 'Month YYYY' format when possible.
- Output MUST be ONLY JSON, no explanation, no markdown.
"""


def parse_cv_with_gemini(
    file_bytes: bytes,
    mime_type: str,
    filename: str | None = None,
) -> str:
    """
    Supports:
      - image/png, image/jpeg, image/jpg  (inline bytes)
      - application/pdf                   (multi-page PDF via file upload API)

    Returns: raw text from Gemini (JSON as text).
    Raises: RuntimeError on Gemini / API level issues.
    """
    if not GEMINI_API_KEY:
        raise RuntimeError("GEMINI_API_KEY is not configured.")

    model = genai.GenerativeModel(GEMINI_MODEL)
    prompt = _build_prompt()

    try:
        # If image → send as inline data
        if mime_type.startswith("image/"):
            response = model.generate_content(
                [
                    {
                        "mime_type": mime_type,
                        "data": file_bytes,
                    },
                    prompt,
                ]
            )
            return response.text

        # If PDF → use file upload API (better multi-page handling)
        elif mime_type == "application/pdf":
            # write bytes to a temp file because upload_file expects a path
            suffix = ".pdf"
            if filename and filename.lower().endswith(".pdf"):
                suffix = os.path.splitext(filename)[1]

            with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
                tmp.write(file_bytes)
                tmp_path = tmp.name

            try:
                uploaded_file = genai.upload_file(path=tmp_path)
                # now send both file + prompt
                response = model.generate_content(
                    [
                        uploaded_file,
                        prompt,
                    ]
                )
                return response.text
            finally:
                # clean up temp file
                if os.path.exists(tmp_path):
                    os.remove(tmp_path)

        else:
            # should not arrive here due to filtering in main.py
            raise RuntimeError(f"Unsupported mime type in gemini_service: {mime_type}")

    except gexc.InvalidArgument as e:
        # Typically API key invalid/expired or bad request
        raise RuntimeError(f"Gemini API error (InvalidArgument): {e.message}")
    except gexc.GoogleAPICallError as e:
        raise RuntimeError(f"Gemini API call error: {e.message}")
    except Exception as e:
        raise RuntimeError(f"Unexpected error while calling Gemini: {e}")
