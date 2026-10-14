"""Shared Gemini client with clear configuration errors."""
import os
from functools import lru_cache
from dotenv import load_dotenv

load_dotenv()

@lru_cache(maxsize=1)
def get_model():
    api_key = os.getenv("GEMINI_API_KEY", "").strip()
    if not api_key or api_key == "replace_me":
        raise RuntimeError("Gemini is not configured. Add your API key to GEMINI_API_KEY in the .env file.")
    try:
        from google import genai
    except ImportError as exc:
        raise RuntimeError("Gemini SDK is missing. Run: pip install -r requirements.txt") from exc
    return genai.Client(api_key=api_key)

async def generate_text(prompt: str) -> str:
    client = get_model()
    model_name = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
    try:
        response = client.models.generate_content(model=model_name, contents=prompt)
        text = getattr(response, "text", None)
        if not text or not text.strip():
            raise RuntimeError("Gemini returned an empty response. Try again or choose another model in .env.")
        return text.strip()
    except RuntimeError:
        raise
    except Exception as exc:
        raise RuntimeError(f"Gemini request failed ({type(exc).__name__}). Check your API key, quota, network, and GEMINI_MODEL setting.") from exc
