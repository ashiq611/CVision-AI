import google.generativeai as genai
from app.config import GEMINI_API_KEY, GEMINI_MODEL

genai.configure(api_key=GEMINI_API_KEY)

def parse_cv_with_gemini(image_bytes: bytes, mime_type: str):
    model = genai.GenerativeModel(GEMINI_MODEL)

    prompt = """
    Extract all resume details from this image and return ONLY valid JSON in this format:

    {
      "name": null,
      "email": null,
      "phone": null,
      "summary": null,
      "education": [{"degree": null, "institution": null, "start_year": null, "end_year": null}],
      "work_experience": [{"title": null, "company": null, "start": null, "end": null, "description": null}],
      "skills": [],
      "certifications": [],
      "languages": [],
      "address": null,
      "other": {}
    }

    RULES:
    - No explanation, no markdown, only JSON output.
    - If data missing, keep null or empty list.
    """

    response = model.generate_content([
        {"mime_type": mime_type, "data": image_bytes},
        prompt
    ])

    return response.text
