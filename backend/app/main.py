# backend/app/main.py

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.engine.game import Game
from app.engine.ai import choose_bot_move

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

game = Game()

class MoveRequest(BaseModel):
    move: str

class BotMoveRequest(BaseModel):
    difficulty: str

@app.get("/")
async def root():
    return { "message": "Chess API running" }

@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/game")
def get_game():
    return game.get_state()



@app.post("/api/v1/game/move")
def make_move(request: MoveRequest):
    try:
        return game.make_move(request.move)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid move")



@app.post("/api/v1/game/bot-move")
def bot_make_move(request: BotMoveRequest):
    try:
        move = choose_bot_move(game.board, request.difficulty)
        if move is None:
            raise HTTPException(status_code=400, detail="No legal bot move available")
        
        return game.make_move(move)
    
    except ValueError:
        raise HTTPException(status_code=400, detail="Bot failed to move")



@app.post("/api/v1/game/undo")
def undo_move():
    try:
        game.undo_move()
    except IndexError:
        raise HTTPException(status_code=400, detail="No move to undo")



@app.post("/api/v1/game/reset")
def reset_game():
    global game 
    game = Game()
    return game.get_state()



