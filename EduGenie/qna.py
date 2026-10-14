from ai_client import generate_text

async def answer_question(question: str) -> str:
    question = question.strip()
    if not question:
        raise ValueError("Please enter a question.")
    return await generate_text(
        "You are EduGenie, a careful educational tutor. Answer the student's question accurately and clearly. "
        "Use simple language, a short direct answer first, then explain with bullets or an example if useful. "
        "If uncertain, say so rather than inventing facts.\n\nStudent question: " + question
    )
