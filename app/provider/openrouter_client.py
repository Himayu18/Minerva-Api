import httpx
import json
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
    return {
        "Authorization": f"Bearer {settings.OPENROUTER_API_KEY}",
        "HTTP-Referer": settings.OPENROUTER_SITE_URL,
        "X-Title": settings.OPENROUTER_APP_NAME,
        "Content-Type": "application/json",
    }

async def chat_completion(payload: dict):
    # Force streaming always
    payload = {**payload, "stream": True}

    async with httpx.AsyncClient(timeout=None) as client:
        async with client.stream(
            "POST",
            f"{BASE_URL}/chat/completions",
            headers=headers(),
            json=payload,
        ) as r:
            if r.status_code >= 400:
                body = await r.aread()
                raise RuntimeError(f"{r.status_code} {body.decode('utf-8', errors='ignore')}")

            async for line in r.aiter_lines():
                if not line:
                    continue
                if line.startswith(":"):
                    continue
                if not line.startswith("data:"):
                    continue

                data = line[len("data:"):].strip()
                if data == "[DONE]":
                    break

                event = json.loads(data)
                delta = event["choices"][0].get("delta", {})
                chunk = delta.get("content")
                if chunk:
                    yield chunk
