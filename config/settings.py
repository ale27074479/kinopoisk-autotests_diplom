import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    BASE_URL = os.getenv("BASE_URL", "https://www.kinopoisk.ru")
    API_URL = os.getenv("API_URL", "https://api.kinopoisk.dev")
    API_TOKEN = os.getenv("API_TOKEN")
    
    # Настройки браузера
    HEADLESS = os.getenv("HEADLESS", "False").lower() == "true"
    BROWSER = os.getenv("BROWSER", "chrome")
    
settings = Settings()
