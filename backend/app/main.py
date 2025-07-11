# app/main.py
from app.models.log_model import Base
from app.core.database import engine
from fastapi import FastAPI
from app.api import log_routes
app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.get("/healthcheck")
def health_check():
    return {"status": "running"}

app.include_router(log_routes.router)