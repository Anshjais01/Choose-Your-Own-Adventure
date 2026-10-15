## Run locally

1. Copy `.env.example` to `.env`.
2. Put your OpenAI API key in `backend/.env` as `OPENAI_API_KEY`.
3. Start the API from this directory:

```powershell
uv run python .\main.py
```

The key is read by the backend only. Do not add it to frontend environment variables or commit `.env`.
