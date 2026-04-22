import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    WEATHER_API = os.getenv('WEATHER_API')
    EMAIL = os.getenv('EMAIL')
    EMAIL_PASS = os.getenv('EMAIL_PASS')
    HF_TOKEN = os.getenv('HF_TOKEN')

    # Default settings
    DEFAULT_MODEL = "gemini-3-flash-preview"
    DEFAULT_TIMEZONE = "Asia/Dhaka"
    
    # Tool settings
    SMTP_SERVER = "smtp.gmail.com"
    SMTP_PORT = 587
