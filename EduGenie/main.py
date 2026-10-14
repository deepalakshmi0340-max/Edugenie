"""EduGenie: Gemini-powered learning assistant."""
import logging
import os
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field

from explanation_module import explain_concept
from learning_path import get_learning_recommendations
from qna import answer_question
from quiz_module import generate_quiz
from summary_module import summarize_text

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")
logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"))
logger = logging.getLogger("edugenie")

app = FastAPI(title="EduGenie API", description="AI-powered learning assistant", version="1.0.0")
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

class TextRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=30000, description="Question, topic, or educational passage")
    level: str = Field(default="beginner", max_length=40)

class QuestionRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=10000)

@app.get("/", response_class=HTMLResponse, include_in_schema=False)
async def home(request: Request):
    return templates.TemplateResponse(request=request, name="index.html", context={})

@app.get("/health")
async def health():
    return {"status": "ok", "service": "EduGenie", "ai_configured": bool(os.getenv("GEMINI_API_KEY"))}

@app.post("/qa")
async def qa(payload: QuestionRequest):
    return await _run_ai("Q&A", answer_question, payload.question)

@app.post("/explain")
async def explain(payload: TextRequest):
    return await _run_ai("explanation", explain_concept, payload.text, payload.level)

@app.post("/quiz")
async def quiz(payload: TextRequest):
    return await _run_ai("quiz generation", generate_quiz, payload.text)

@app.post("/summarize")
async def summarize(payload: TextRequest):
    return await _run_ai("summarization", summarize_text, payload.text)

@app.post("/learn/recommendations")
async def recommendations(payload: TextRequest):
    return await _run_ai("learning recommendations", get_learning_recommendations, payload.text, payload.level)

async def _run_ai(label: str, func, *args) -> dict[str, Any]:
    try:
        result = await func(*args)
        return {"result": result}
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except RuntimeError as exc:
        logger.warning("%s unavailable: %s", label, exc)
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except Exception as exc:
        logger.exception("Unexpected error during %s", label)
        raise HTTPException(status_code=500, detail=f"Unable to complete {label}. Check server logs and API configuration.") from exc
