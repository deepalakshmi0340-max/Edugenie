from ai_client import generate_text

async def summarize_text(text: str) -> str:
    text = text.strip()
    if not text:
        raise ValueError("Enter a passage to summarize.")
    return await generate_text(
        "Summarize the educational text below in clear, concise language. Preserve the main ideas and important facts. "
        "Use a short paragraph followed by key points when appropriate. Do not add facts that are not in the source.\n\nText:\n" + text
    )
