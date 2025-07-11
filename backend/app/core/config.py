# app/core/config.py

from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

class Settings(BaseSettings):
    DATABASE_URL: str = os.getenv("DATABASE_URL")

settings = Settings()
