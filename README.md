# 🔍 CVision AI — CV/Resume Parser using Gemini AI

**CVision AI** is a machine learning powered service that extracts structured information from CV/Resume images using **Google Gemini Vision AI** and serves the parsed result as clean JSON via a **FastAPI** backend.

---

## ✨ Features

✅ Upload CV/Resume image (JPG, PNG, etc.)  
✅ Extract structured fields using Gemini AI (Name, Email, Education, Skills, etc.)  
✅ API returns well-formatted JSON  
✅ Built with **FastAPI** for high performance  
✅ Input validation & Pydantic schema  
✅ Easy cURL, Postman, or Thunder Client integration  

---

## 🧠 Tech Stack

| Component | Technology |
|---|---|
| Backend Framework | FastAPI (Python) |
| AI Model | Google Gemini Vision |
| Server | Uvicorn |
| Validation | Pydantic |
| Image Upload | Multipart/Form-Data |
| Environment | Python Virtualenv |

## ⚙️ Setup & Installation

### 1️⃣ Clone the repository

```bash
git clone <repo_url>
cd CVision\ AI
cd ml

##Create .env

GEMINI_API_KEY=your_api_key_here
GEMINI_MODEL=gemini-2.0-flash
PORT=8000


python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
bash run.sh

