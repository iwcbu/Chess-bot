# backend/app/main.py

from fastapi import FastAPI
import chess

b = chess.Board()

app = FastAPI()

@app.get("/")
async def root():
    return "Welcome to the backrooms"

@app.get("/api/v1")
async def apiroot():
    return {"message": "Hello World"}

@app.get("/api/v1/health")
def health_check():
    return {"status": "ok"}

@app.get("/api/v1/game")
def game():
    return {"status": "in progress"}
