import os


APP_NAME = os.getenv("APP_NAME", "FastAPI Backend")
DEBUG = os.getenv("DEBUG", "false").strip().lower() in {"1", "true", "yes", "on"}
