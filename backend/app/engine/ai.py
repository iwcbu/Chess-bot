# backend/app/engine/ai.py

import chess
import random
import math

from .evaluation import evaluate_Claude_Shannon




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



