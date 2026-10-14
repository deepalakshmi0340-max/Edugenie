from ai_client import generate_text

async def get_learning_recommendations(topic: str, level: str = "beginner") -> str:
    topic = topic.strip()
    if not topic:
        raise ValueError("Enter a topic for your learning path.")
    return await generate_text(
        f"Create a practical learning roadmap for '{topic}' for a learner currently at {level} level. "
        "Organize it from beginner to intermediate to advanced. Include suggested order, estimated time per stage, "
        "practice projects, ways to check understanding, and trustworthy resource names or official URLs when known. "
        "Do not invent specific links; mark any resource URL you cannot verify as a suggested search. Format with headings and bullets."
    )
