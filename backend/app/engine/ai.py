# backend/app/engine/ai.py

import chess
import random
import math


from .evaluation import evaluate_Claude_Shannon
from .search import choose_minimax_move, choose_minimax_with_ab_move



OPENING_LINES = {
    "ruy_lopez": [
        [
            "e2e4", "e7e5",
            "g1f3", "b8c6",
            "f1b5", "a7a6",
            "b5a4", "g8f6",
            "e1g1", "f8e7",
            "f1e1", "b7b5",
            "a4b3", "d7d6",
            "c2c3", "e8g8",
        ],

        [
            "e2e4", "e7e5",
            "g1f3", "b8c6",
            "f1b5", "g8f6",
            "e1g1", "f6e4",
            "d2d4", "e4d6",
            "b5c6", "d7c6",
            "d4e5",
        ],

        [
            "e2e4", "e7e5",
            "g1f3", "b8c6",
            "f1b5", "a7a6",
            "b5c6", "d7c6",
            "e1g1", "f7f6",
            "d2d4", "e5d4",
            "f3d4", "c6c5",
        ],

        [
            "e2e4", "e7e5",
            "g1f3", "b8c6",
            "f1b5", "a7a6",
            "b5a4", "g8f6",
            "e1g1", "f6e4",
            "d2d4", "b7b5",
            "a4b3", "d7d5",
            "d4e5", "c8e6",
        ],

        [
            "e2e4", "e7e5",
            "g1f3", "b8c6",
            "f1b5", "f7f5",
            "b1c3", "f5e4",
            "c3e4", "d7d5",
        ],

        [
            "e2e4", "e7e5",
            "g1f3", "b8c6",
            "f1b5", "d7d6",
            "d2d4", "c8d7",
            "b1c3", "g8f6",
            "e1g1", "f8e7",
        ],
    ],

    "italian_game": [ 
        [
            "e2e4", "e7e5",
            "g1f3", "b8c6",
            "f1c4", "f8c5",
            "c2c3", "g8f6",
            "d2d3", "d7d6",
            "e1g1", "e8g8",
        ],

        [
            "e2e4", "e7e5",
            "g1f3", "b8c6",
            "f1c4", "f8c5",
            "b2b4", "c5b4",
            "c2c3", "b4a5",
            "d2d4", "e5d4",
            "e1g1",
        ],

        [
            "e2e4", "e7e5",
            "g1f3", "b8c6",
            "f1c4", "g8f6",
            "f3g5", "d7d5",
            "e4d5", "c6a5",
            "c4b5", "c7c6",
            "d5c6", "b7c6",
        ],

        [
            "e2e4", "e7e5",
            "g1f3", "b8c6",
            "f1c4", "g8f6",
            "b1c3", "f8c5",
            "d2d3", "d7d6",
            "e1g1", "e8g8",
        ],

        [
            "e2e4", "e7e5",
            "g1f3", "b8c6",
            "f1c4", "g8f6",
            "d2d4", "e5d4",
            "e1g1", "f8c5",
            "e4e5", "d7d5",
            "e5f6", "d5c4",
        ],

        [
            "e2e4", "e7e5",
            "g1f3", "b8c6",
            "f1c4", "f8e7",
            "d2d4", "d7d6",
            "b1c3", "g8f6",
            "e1g1", "e8g8",
        ],
    ],

    "queens_gambit": [
        [
            "d2d4", "d7d5",
            "c2c4", "e7e6",
            "b1c3", "g8f6",
            "c1g5", "f8e7",
            "e2e3", "e8g8",
            "g1f3", "b8d7",
        ],

        [
            "d2d4", "d7d5",
            "c2c4", "d5c4",
            "e2e4", "g8f6",
            "b1c3", "e7e5",
            "g1f3", "e5d4",
            "f3d4",
        ],

        [
            "d2d4", "d7d5",
            "c2c4", "c7c6",
            "g1f3", "g8f6",
            "b1c3", "d5c4",
            "a2a4", "c8f5",
        ],

        [
            "d2d4", "d7d5",
            "c2c4", "e7e6",
            "g1f3", "g8f6",
            "b1c3", "c7c6",
            "e2e3", "b8d7",
            "f1d3", "d5c4",
            "d3c4",
        ],

        [
            "d2d4", "d7d5",
            "c2c4", "e7e6",
            "b1c3", "c7c5",
            "c4d5", "e6d5",
            "g1f3", "b8c6",
            "g2g3", "g8f6",
        ],

        [
            "d2d4", "d7d5",
            "c2c4", "e7e5",
            "d4e5", "d5d4",
            "g1f3", "b8c6",
            "g2g3", "c8e6",
        ],
    ],
    "sicilian_defense": [
        [
            "e2e4", "c7c5",
            "g1f3", "d7d6",
            "d2d4", "c5d4",
            "f3d4", "g8f6",
            "b1c3", "a7a6",
            "c1e3", "e7e5",
        ],

        [
            "e2e4", "c7c5",
            "g1f3", "d7d6",
            "d2d4", "c5d4",
            "f3d4", "g8f6",
            "b1c3", "g7g6",
            "c1e3", "f8g7",
            "f2f3", "e8g8",
        ],

        [
            "e2e4", "c7c5",
            "g1f3", "d7d6",
            "d2d4", "c5d4",
            "f3d4", "g8f6",
            "b1c3", "e7e6",
            "f1e2", "f8e7",
            "e1g1", "e8g8",
        ],

        [
            "e2e4", "c7c5",
            "g1f3", "d7d6",
            "d2d4", "c5d4",
            "f3d4", "g8f6",
            "b1c3", "b8c6",
            "c1g5", "e7e6",
            "d1d2", "f8e7",
        ],

        [
            "e2e4", "c7c5",
            "g1f3", "b8c6",
            "d2d4", "c5d4",
            "f3d4", "g7g6",
            "c2c4", "f8g7",
            "c1e3", "g8f6",
            "b1c3", "e8g8",
        ],

        [
            "e2e4", "c7c5",
            "g1f3", "b8c6",
            "d2d4", "c5d4",
            "f3d4", "g8f6",
            "b1c3", "e7e5",
            "d4b5", "d7d6",
            "c1g5", "a7a6",
            "b5a3", "b7b5",
        ],
    ],

    "caro_kann": [
        [
            "e2e4", "c7c6",
            "d2d4", "d7d5",
            "b1c3", "d5e4",
            "c3e4", "c8f5",
            "e4g3", "f5g6",
            "h2h4", "h7h6",
        ],

        [
            "e2e4", "c7c6",
            "d2d4", "d7d5",
            "e4e5", "c8f5",
            "g1f3", "e7e6",
            "f1e2", "c6c5",
            "e1g1", "b8c6",
        ],

        [
            "e2e4", "c7c6",
            "d2d4", "d7d5",
            "e4d5", "c6d5",
            "f1d3", "b8c6",
            "c2c3", "g8f6",
            "c1f4", "c8g4",
        ],

        [
            "e2e4", "c7c6",
            "d2d4", "d7d5",
            "e4d5", "c6d5",
            "c2c4", "g8f6",
            "b1c3", "e7e6",
            "g1f3", "f8b4",
        ],

        [
            "e2e4", "c7c6",
            "d2d4", "d7d5",
            "f2f3", "d5e4",
            "f3e4", "e7e5",
            "g1f3", "e5d4",
            "f1c4",
        ],

        [
            "e2e4", "c7c6",
            "b1c3", "d7d5",
            "g1f3", "c8g4",
            "h2h3", "g4f3",
            "d1f3", "e7e6",
            "d2d4",
        ],
    ],

    "kings_indian_defense": [
        [
            "d2d4", "g8f6",
            "c2c4", "g7g6",
            "b1c3", "f8g7",
            "e2e4", "d7d6",
            "g1f3", "e8g8",
            "f1e2", "e7e5",
            "e1g1", "b8c6",
        ],

        [
            "d2d4", "g8f6",
            "c2c4", "g7g6",
            "g2g3", "f8g7",
            "f1g2", "e8g8",
            "g1f3", "d7d6",
            "e1g1", "b8d7",
        ],

        [
            "d2d4", "g8f6",
            "c2c4", "g7g6",
            "b1c3", "f8g7",
            "e2e4", "d7d6",
            "f2f3", "e8g8",
            "c1e3", "e7e5",
            "g1e2",
        ],

        [
            "d2d4", "g8f6",
            "c2c4", "g7g6",
            "b1c3", "f8g7",
            "e2e4", "d7d6",
            "f2f4", "e8g8",
            "g1f3", "c7c5",
            "d4d5", "e7e6",
        ],

        [
            "d2d4", "g8f6",
            "c2c4", "g7g6",
            "b1c3", "f8g7",
            "e2e4", "d7d6",
            "f1e2", "e8g8",
            "c1g5", "c7c5",
            "d4d5", "e7e6",
        ],

        [
            "d2d4", "g8f6",
            "c2c4", "g7g6",
            "b1c3", "f8g7",
            "e2e4", "d7d6",
            "g1f3", "e8g8",
            "f1e2", "e7e5",
            "e1g1", "b8c6",
            "d4d5", "c6e7",
        ],
    ],
}


def choose_random_move(board: chess.Board):

    if board.is_game_over():
        raise ValueError("Game is over")
    
    moves = list(board.legal_moves)
    if len(moves) == 0:
        raise ValueError("Returning that there are NO legal moves in this position, but game is not over.")

    return random.choice(moves)



def choose_greedy_move(board: chess.Board):

    if board.is_game_over():
        raise ValueError("Game is over")
    
    moves = list(board.legal_moves)
    if len(moves) == 0:
        raise ValueError("Returning that there are NO legal moves in this position, but game is not over.")

    if board.turn == chess.WHITE:

        best = [-math.inf, moves[0]]

        for move in moves:
            board.push(move)
            try:
                posEval = evaluate_Claude_Shannon(board)
            finally:
                board.pop()

            if posEval > best[0]:
                best[0], best[1] = posEval, move

        
        return best[1]
    
    else:
        best = [math.inf, moves[0]]

        for move in moves:
            board.push(move)
            posEval = evaluate_Claude_Shannon(board)
            board.pop()

            if posEval < best[0]:
                best[0], best[1] = posEval, move

        
        return best[1]


def choose_expert_move(board: chess.Board, depth: int, opening: str):
    if not opening or opening not in OPENING_LINES:
        return choose_minimax_with_ab_move(board, depth)
    
    moves_set = OPENING_LINES[opening]
    move_count = len(board.move_stack)

    history = [move.uci() for move in board.move_stack]
    legal_moves = {move.uci() for move in board.legal_moves}

    for line in moves_set:
        if history == line[:move_count]:
            if move_count < len(line):
                next_move = line[move_count]

                if next_move in legal_moves:
                    return next_move
    
    return choose_minimax_with_ab_move(board, depth)



def choose_bot_move(board: chess.Board, difficulty: str, opening: str):
    match difficulty:
        case 'easy':
            return choose_greedy_move(board)
        case 'medium':
            return choose_minimax_with_ab_move(board, 2)
        case 'hard':
            return choose_minimax_with_ab_move(board, 4)
        case 'expert':
            return choose_expert_move(board, 5, opening)


