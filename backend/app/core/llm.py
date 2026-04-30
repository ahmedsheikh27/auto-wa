from langchain_google_genai import GoogleGenerativeAI
from app.core.config import Settings


def get_llm():
    return GoogleGenerativeAI(
        api_key=Settings.GOOGLE_API_KEY, model="gemini-2.5-flash", temperature=0.3
    )
