from fastapi import FastAPI, HTTPException
from app.schemas import ChatRequest, ChatResponse
from app.openrouter_client import chat_completion, settings

app = FastAPI(title="Minerva  API", version="0.1")

@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    model = req.model or settings.OPENROUTER_MODEL

    payload = {
        "model": model,
        "messages": [m.model_dump() for m in req.messages],
        "temperature": req.temperature,
        "max_tokens": req.max_tokens,
    }

    try:
        data = await chat_completion(payload)

        # OpenAI-style response shape: choices[0].message.content
        reply = data["choices"][0]["message"]["content"]
        return ChatResponse(model=model, reply=reply)

    except KeyError:
        raise HTTPException(status_code=502, detail=f"Unexpected response shape from OpenRouter: {data}")
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"OpenRouter error: {str(e)}")
