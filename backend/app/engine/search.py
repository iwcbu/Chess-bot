# backend/app/engine/search.py

import chess
import math
from .evaluation import evaluate_Claude_Shannon


def minimax(board: chess.Board, depth: int, maximizing: bool):

    if not board.is_valid():
        raise ValueError("Board not valid dawg")
    
    if depth == 0:
        return evaluate_Claude_Shannon(board)

    if maximizing:
        max = -math.inf
        if board.is_game_over():
            return max
        
        for move in list(board.legal_moves):
            try:
                board.push(move)
                score = minimax(board, depth-1, False)
            finally:
                board.pop()
            
            if score > max:
                max = score

        return max
    
    else:
        min = math.inf
        if board.is_game_over():
            return min
        for move in list(board.legal_moves):
            try:
                board.push(move)
                score = minimax(board, depth-1, True)
            finally:
                board.pop()
            
            if score < min:
                min = score
        
        return min
    

    

def choose_minimax_move(board: chess.Board, depth: int):

    if board.is_game_over():
        print("Game over son")
        return None
    
    if not board.is_valid():
        raise ValueError("Board is not valid", board.fen())

    moves = list(board.legal_moves)
    if len(moves) < 1:
        raise ValueError("Game not over but legal moves blank")
    
    best = [moves[0], -math.inf]

    for move in moves:
        board.push(move)
        try: 
            score = minimax(board, depth, maximizing=False)
        finally:
            board.pop()

        if score >= best[1]:
            best[0], best[1] = move, score
        
    return best[0]
        
        

    





def minimax_with_alpha_beta_pruning(board: chess.Board, depth: int, alpha: int, beta: int, maximizing: bool) -> float:
    
    if not board.is_valid():
        raise ValueError("Board not valid dawg")
    
    if board.is_game_over():
        if board.is_checkmate():
            return -math.inf if maximizing else math.inf
        
        return 0

    if depth < 0:
        raise ValueError("Depth too small too search")

    if depth == 0:
        return evaluate_Claude_Shannon(board)
    



    if maximizing:
        maxScore = -math.inf

        for move in list(board.legal_moves):
            try:
                board.push(move)
                score = minimax_with_alpha_beta_pruning(board, depth-1, alpha, beta, False)
            finally:
                board.pop()
            
            maxScore = max(score, maxScore)
            alpha = max(alpha, score)
            if alpha >= beta:
                break
            
        return maxScore
    
    else:
        minScore = math.inf
            
        for move in list(board.legal_moves):
            try:
                board.push(move)
                score = minimax_with_alpha_beta_pruning(board, depth-1, alpha, beta, True)
            finally:
                board.pop()
            
            minScore = min(minScore, score)
            beta = min(beta, score)
            if beta <= alpha:
                break
            
        
        return minScore
    

def choose_minimax_with_ab_move(board: chess.Board, depth: int):

    if board.is_game_over() or depth == 0:
        print("Game over son")
        return None
    
    if not board.is_valid():
        raise ValueError("Board is not valid", board.fen())

    moves = list(board.legal_moves)
    if len(moves) < 1:
        raise ValueError("Game not over but legal moves blank")
    
    if board.turn == chess.WHITE:

        best = [moves[0], -math.inf]

        for move in moves:
            board.push(move)
            try: 
                score = minimax_with_alpha_beta_pruning(board, depth-1, -math.inf, math.inf, maximizing=False)
            finally:
                board.pop()

            if best[1] < score:
                best[0], best[1] = move, score
            
        return best[0]
    
    else:
        best = [moves[0], math.inf]

        for move in moves:
            board.push(move)
            try: 
                score = minimax_with_alpha_beta_pruning(board, depth-1, -math.inf, math.inf, maximizing=True)
            finally:
                board.pop()

            if best[1] > score:
                best[0], best[1] = move, score
            
        return best[0]
        
            
    