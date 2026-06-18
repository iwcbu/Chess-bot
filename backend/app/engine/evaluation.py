# backend/app/engine/evaluation.py

from .game import Game
import chess
import math


def mobility_count(board: chess.Board, color):
    temp = board.copy(stack=False)
    temp.turn = color
    return len(list(temp.legal_moves))

def evaluate_Claude_Shannon(board: chess.Board):

    if not board.is_valid():
        raise ValueError("Invalid board")
    
    if board.is_game_over():
        return -math.inf if board.turn == chess.WHITE else math.inf
    
    fen = board.fen()
    pc = Game.count_pieces(fen)

    materialScore = ( 
        200 * (pc["K"] - pc["k"]) 
        + 9 * (pc["Q"] - pc["q"]) 
        + 5 * (pc["R"] - pc["r"]) 
        + 3 * (pc["B"] - pc["b"] + pc["N"] - pc["n"]) 
        + (pc["P"] - pc["p"]) 
    )

    white_pawn_weakness = (
        Game.isolated_pawn_count(fen, chess.WHITE)
        + Game.doubled_pawn_count(fen, chess.WHITE)
        + Game.blocked_pawns_count(fen, chess.WHITE)
    )

    black_pawn_weakness = (
        Game.isolated_pawn_count(fen, chess.BLACK)
        + Game.doubled_pawn_count(fen, chess.BLACK)
        + Game.blocked_pawns_count(fen, chess.BLACK)
    )

    pawnPosScore = 0.5 * (white_pawn_weakness - black_pawn_weakness)

    white_mobility = mobility_count(board, chess.WHITE)
    black_mobility = mobility_count(board, chess.BLACK)

    mobilituScore = 0.1 * (white_mobility - black_mobility)

    white_score = materialScore + mobilituScore - pawnPosScore

    return white_score if board.turn == chess.WHITE else -white_score

