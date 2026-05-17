import os
from dotenv import load_dotenv
from agents import AsyncOpenAI

load_dotenv()


class Settings:
    DATABASE_URL = os.getenv("DATABASE_URL")
    GOOGLE_API_KEY = "AIzaSyDJxcEwHEEmDx0PtP8ohBlZQqO4aFfNFNQ" #dev
    ACCESS_TOKEN = os.getenv("WHATSAPP_TOKEN")
    PHONE_NUMBER_ID = os.getenv("PHONE_ID")
    WHATSAP_BASE_URL = os.getenv("WHATSAP_BASE_URL")
    HYGRAPH_URL = os.getenv("HYGRAPH_ENDPOINT")
    APP_SECRET = os.getenv("APP_SECRET")
    REDIS_URL = os.getenv("REDIS_URL")
    CLIENT = AsyncOpenAI(
    api_key=GOOGLE_API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

settings = Settings()
