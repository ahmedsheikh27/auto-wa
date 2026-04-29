import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    DATABASE_URL = os.getenv("DATABASE_URL")
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    ACCESS_TOKEN = os.getenv("WHATSAPP_TOKEN")
    PHONE_NUMBER_ID = os.getenv("PHONE_ID")
    WHATSAP_BASE_URL = os.getenv("WHATSAP_BASE_URL")

settings = Settings()
