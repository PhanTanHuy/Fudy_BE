from fastapi import FastAPI

from app.api.router import api_router
from app.core.config import APP_NAME, DEBUG

app = FastAPI(title=APP_NAME, debug=DEBUG)
app.include_router(api_router)
