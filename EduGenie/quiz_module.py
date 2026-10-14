import json
import re
from ai_client import generate_text

async def generate_quiz(text: str) -> list[dict]:
    text = text.strip()
    if not text:
        raise ValueError("Enter a topic or passage to generate a quiz.")
    prompt = """Create exactly 3 educational multiple-choice questions based only on the topic/passage below.
Return ONLY a valid JSON array. Each item must have keys: question (string), options (array of exactly 4 strings), answer (string exactly matching one option), explanation (short string).
Make distractors plausible and ensure only one correct answer per question.

Topic or passage:
""" + text
    raw = await generate_text(prompt)
    cleaned = re.sub(r"^\s*```(?:json)?\s*|\s*```\s*$", "", raw, flags=re.I)
    try:
        data = json.loads(cleaned)
    except json.JSONDecodeError:
        match = re.search(r"\[.*\]", cleaned, flags=re.S)
        if not match:
            raise RuntimeError("The AI returned quiz data that was not valid JSON. Please try again.")
        try:
            data = json.loads(match.group(0))
        except json.JSONDecodeError as exc:
            raise RuntimeError("The AI returned malformed quiz JSON. Please try again.") from exc
    if not isinstance(data, list) or len(data) != 3:
        raise RuntimeError("The AI did not return exactly 3 quiz questions. Please try again.")
    validated = []
    for item in data:
        if not isinstance(item, dict) or not isinstance(item.get("question"), str):
            raise RuntimeError("Quiz question format was invalid. Please try again.")
        options = item.get("options")
        answer = item.get("answer")
        if not isinstance(options, list) or len(options) != 4 or answer not in options:
            raise RuntimeError("A quiz question must contain four options and a matching correct answer.")
        validated.append({"question": item["question"], "options": options, "answer": answer, "explanation": str(item.get("explanation", ""))})
    return validated
