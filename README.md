# FastAPI Backend

## Run locally

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
```

The API documentation is available at `http://127.0.0.1:8000/docs`.
