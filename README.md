# Minerva API

A FastAPI-based backend that provides **streaming AI chat responses** using OpenRouter.  
Designed to be consumed by web, mobile, and desktop applications.

---

## Features

- Streaming chat completions (real-time responses)
- OpenRouter model support
- Simple health check endpoint
- Environment-based configuration
- Clean and minimal project structure

---

## Tech Stack

- **Language:** Python 3.10+
- **Framework:** FastAPI
- **Server:** Uvicorn
- **HTTP Client:** httpx
- **Configuration:** Pydantic Settings (`.env`)
- **AI Provider:** OpenRouter

---

## Project Structure

```
.
├── app/
│   ├── __pycache__/          # Python bytecode cache
│   ├── main.py               # FastAPI app entry point
│   ├── openrouter_client.py  # OpenRouter API integration
│   └── schemas.py            # Request and response models
├── .env                      # Environment variables (not in git)
└── .gitignore                # Git ignore rules
```

---

## Setup & Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/minerva-api.git
cd minerva-api
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate       # Linux / macOS
venv\Scripts\activate          # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the root directory using the example below.

```env
OPENROUTER_API_KEY=your_api_key_here
OPENROUTER_MODEL=openai/gpt-4o
OPENROUTER_SITE_URL=http://localhost
OPENROUTER_APP_NAME=Minerva
```

⚠️ **Never commit your `.env` file.**

---

## Running the API

```bash
uvicorn app.main:app --reload
```

- **API Base URL:** `http://127.0.0.1:8000`
- **Swagger Docs:** `http://127.0.0.1:8000/docs`
- **ReDoc:** `http://127.0.0.1:8000/redoc`

---

## API Endpoints

### `GET /health`

Health check endpoint.

**Response:**

```json
{
  "status": "ok"
}
```

### `POST /chat`

Streams AI-generated chat responses.

**Request Body:**

```json
{
  "model": "openai/gpt-4o",
  "messages": [
    {
      "role": "user",
      "content": "Hello"
    }
  ]
}
```

**Behavior:**
- Returns responses as a stream
- Suitable for real-time chat UIs
- Frontend can consume using Fetch streams / SSE

---

## Streaming Explanation

This API uses HTTP streaming to send AI responses token-by-token instead of waiting for a full completion. This reduces perceived latency and enables responsive chat interfaces.

---

## Error Handling

- `400` – Invalid request
- `422` – Request body validation error
- `500` – Upstream or internal server error

---

## Security Notes

- Secrets are managed via environment variables
- `.env` is ignored using `.gitignore`
- Add authentication and rate limiting before deploying publicly

---

## Roadmap

- [ ] Authentication (API keys / JWT)
- [ ] Rate limiting
- [ ] Request logging
- [ ] Docker support
- [ ] Model fallback handling

---

## License

MIT License

---

## Contact

For questions or contributions, please open an issue or submit a pull request.
