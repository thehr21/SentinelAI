# app/main.py

from fastapi import FastAPI

app = FastAPI()

@app.get("/healthcheck")
def health_check():
    return {"status": "running"}
