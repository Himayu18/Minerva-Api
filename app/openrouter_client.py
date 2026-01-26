import httpx
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    OPENROUTER_API_KEY: str
    OPENROUTER_SITE_URL: str = "http://localhost"
    OPENROUTER_APP_NAME: str = "Minerva"
    OPENROUTER_MODEL: str 

settings = Settings()

BASE_URL = "https://openrouter.ai/api/v1"

def headers():
    # OpenRouter supports OpenAI-compatible auth + optional ranking headers
    return {
        "Authorization": f"Bearer {settings.OPENROUTER_API_KEY}",
        "HTTP-Referer": settings.OPENROUTER_SITE_URL,  # optional
        "X-Title": settings.OPENROUTER_APP_NAME,        # optional
        "Content-Type": "application/json",
    }

async def chat_completion(payload: dict) -> dict:
    async with httpx.AsyncClient(timeout=60.0) as client:
        r = await client.post(f"{BASE_URL}/chat/completions", headers=headers(), json=payload)
        r.raise_for_status()
        return r.json()


