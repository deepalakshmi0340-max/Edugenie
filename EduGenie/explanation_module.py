"""Concept explanation using optional local LaMini-Flan-T5 or Gemini."""
import os
from ai_client import generate_text

async def explain_concept(topic: str, level: str = "beginner") -> str:
    topic = topic.strip()
    if not topic:
        raise ValueError("Please enter a topic to explain.")
    provider = os.getenv("EXPLANATION_PROVIDER", "gemini").lower()
    if provider == "local":
        try:
            from transformers import pipeline
            # Lazy-load once; this downloads model weights on first use.
            return _local_explainer()(f"Explain {topic} simply for a {level} learner.")
        except Exception as exc:
            if os.getenv("LOCAL_MODEL_FALLBACK", "true").lower() != "true":
                raise RuntimeError("Local model could not be loaded. Install the optional ML dependencies or enable LOCAL_MODEL_FALLBACK=true.") from exc
    return await generate_text(
        f"Explain the topic below for a {level} learner. Start with a plain-language definition, use a relatable example, "
        f"and finish with 2-3 key takeaways. Avoid unnecessary jargon.\n\nTopic: {topic}"
    )

_LOCAL_PIPELINE = None
def _local_explainer():
    global _LOCAL_PIPELINE
    if _LOCAL_PIPELINE is None:
        from transformers import pipeline
        model_name = os.getenv("LOCAL_MODEL_NAME", "MBZUAI/LaMini-Flan-T5-783M")
        _LOCAL_PIPELINE = pipeline("text2text-generation", model=model_name, max_new_tokens=220)
    def run(prompt: str) -> str:
        result = _LOCAL_PIPELINE(prompt)
        return result[0]["generated_text"].strip()
    return run
