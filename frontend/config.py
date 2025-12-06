import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    BACKEND_URL = os.getenv("BACKEND_URL")
    APP_TITLE = "DocuMind AI"
    APP_ICON = "🧠"
    
config = Config()