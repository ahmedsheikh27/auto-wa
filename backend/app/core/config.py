import os
from dotenv import load_dotenv
from openai import AsyncOpenAI

load_dotenv()


class Settings:
    DATABASE_URL = os.getenv("DATABASE_URL")
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY") #dev
    ACCESS_TOKEN = os.getenv("WHATSAPP_TOKEN")
    PHONE_NUMBER_ID = os.getenv("PHONE_ID")
    WHATSAP_BASE_URL = os.getenv("WHATSAP_BASE_URL")
    HYGRAPH_URL = os.getenv("HYGRAPH_ENDPOINT")
    APP_SECRET = os.getenv("APP_SECRET")
    PHONE_NUMBER = os.getenv("PHONE_NUMBER")
    REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    SESSION_TTL_SECONDS = int(os.getenv("SESSION_TTL_SECONDS", "1800"))
    CLIENT = AsyncOpenAI(
    api_key=GOOGLE_API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

settings = Settings()
