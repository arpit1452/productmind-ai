from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.agents.pm_agent import run_agent
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/generate")
def generate(idea: str, gemini_api_key: str = ""):
    # Validate API key
    if not gemini_api_key or not gemini_api_key.strip():
        raise HTTPException(
            status_code=401,
            detail="Gemini API key is required. Please enter your key in the sidebar."
        )

    if not gemini_api_key.startswith("AIza"):
        raise HTTPException(
            status_code=401,
            detail="Invalid Gemini API key format. It should start with 'AIza'."
        )

    # Set the user's key for this request
    os.environ["GEMINI_API_KEY"] = gemini_api_key.strip()

    result = run_agent(idea)
    return {"result": result}


@app.post("/upload_pdf")
async def upload_pdf(file: bytes = None, gemini_api_key: str = ""):
    from fastapi import UploadFile, File
    return {"message": "PDF upload endpoint"}


@app.get("/health")
def health():
    return {"status": "ok"}