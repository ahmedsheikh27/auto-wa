from langchain_google_genai import GoogleGenerativeAI
from app.core.config import settings


def get_llm():
    return GoogleGenerativeAI(
        api_key=settings.GOOGLE_API_KEY, model="gemini-2.5-flash", temperature=0.3
    )
