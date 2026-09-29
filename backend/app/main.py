# backend/app/main.py

import random

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from uuid import uuid4

from app.engine.game import Game
from app.engine.ai import choose_bot_move



app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "https://chess-bot-gray.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

games: dict[str, Game] = {}

class MoveRequest(BaseModel):
    move: str

class BotMoveRequest(BaseModel):
    difficulty: str
    opening: str

@app.get("/")
async def root():
    return { "message": "Chess API running" }

@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/v1/new-game")
def new_game():
    game_id = str(uuid4())
    games[game_id] = Game()

    print("CREATED GAME:", game_id, flush=True)
    print("GAMES NOW:", list(games.keys()), flush=True)
    print("GAMES DICT ID:", id(games), flush=True)

    return {
        "game_id": game_id,
        "state": games[game_id].get_state()
    }

@app.get("/games")
def get_games_dict():
    print("CHECKING GAMES:", list(games.keys()), flush=True)
    print("GAMES DICT ID:", id(games), flush=True)

    return {
        "count": len(games),
        "game_ids": list(games.keys())
    }


@app.get("/v1/game/{game_id}")
def get_game(game_id: str):
    if game_id not in games:
        raise HTTPException(status_code=404, detail="Game not found")
    
    return games[game_id].get_state()

@app.post("/v1/game/{game_id}/move")
def make_move(game_id: str, request: MoveRequest):
    if game_id not in games:
        raise HTTPException( status_code=404, detail="Game not found" )
        
    try:
        return games[game_id].make_move(request.move)
    except ValueError:
        raise HTTPException( status_code=400, detail="Invalid move" )



@app.post( "/v1/game/{game_id}/bot-move" )
def bot_make_move( game_id: str, request: BotMoveRequest ):
    if game_id not in games:
        raise HTTPException( status_code=404, detail="Game not found" )

    game = games[game_id]

    try:
        move = choose_bot_move(
            game.board, 
            request.difficulty, 
            request.opening
        )


        if move is None:
            raise HTTPException( status_code=400, detail="No legal bot move available" )
        
        move_uci = move if type(move) == str else move.uci()
        return games[game_id].make_move(move_uci)
    
    except ValueError:
        raise HTTPException( status_code=400, detail="Bot failed to move" )



@app.post("/v1/game/{game_id}/undo")
def undo_move(game_id: str):
    if game_id not in games:
        raise HTTPException( status_code=404, detail="Game not found" )

    try:
        return games[game_id].undo_move()
    except (IndexError, ValueError):
        raise HTTPException(status_code=400, detail="No move to undo")



@app.post("/v1/game/{game_id}/reset")
def reset_game(game_id: str):
    if game_id not in games:
        raise HTTPException(status_code=404, detail="Game not found")
    
    games[game_id] = Game()
    return games[game_id].get_state()


