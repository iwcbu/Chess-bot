# backend/app/tests/test_difficulty.py

import chess
from app.engine.game import Game
from app.engine.ai import choose_bot_move
from app.engine.search import choose_minimax_move, choose_minimax_with_ab_move
from app.engine.evaluation import evaluate_Claude_Shannon

def test_easy_mode_returns_legal_move():
    game = Game()
    legal_moves = game.get_legal_moves()
    move = choose_bot_move(game.board, 'easy')

    assert move.uci() in legal_moves
    

def test_medium_mode_returns_legal_move():
    game = Game()
    legal_moves = game.get_legal_moves()
    move = choose_bot_move(game.board, 'medium')

    assert move.uci() in legal_moves
    

def test_hard_mode_returns_legal_move():
    game = Game()
    legal_moves = game.get_legal_moves()
    move = choose_bot_move(game.board, 'hard')

    assert move.uci() in legal_moves
    

def test_expert_mode_returns_legal_move():
    game = Game()
    legal_moves = game.get_legal_moves()
    move = choose_bot_move(game.board, 'expert')

    assert move.uci() in legal_moves
    

def test_alpha_beta_matches_minimax_score():
    game = Game()

    mini_move = choose_minimax_move(game.board, 1)
    ab_move = choose_minimax_with_ab_move(game.board, 1)

    game.board.push(mini_move)
    eval_from_mini = evaluate_Claude_Shannon(game.board)
    game.board.pop()

    game.board.push(ab_move)
    eval_from_ab = evaluate_Claude_Shannon(game.board)
    game.board.pop()

    assert eval_from_ab == eval_from_mini
    


    
# DEBUGGING ALPHA BETA MINIMAX

# def test_alpha_beta_picks_best_depth_1_move():
#     game = Game()
#     board = game.board

#     ab_move = choose_minimax_with_ab_move(board, 1)

#     all_scores = []

#     for move in board.legal_moves:
#         board.push(move)
#         try:
#             score = evaluate_Claude_Shannon(board)
#         finally:
#             board.pop()

#         all_scores.append(score)

#     board.push(ab_move)
#     try:
#         ab_score = evaluate_Claude_Shannon(board)
#     finally:
#         board.pop()

#     if board.turn == chess.WHITE:
#         assert ab_score == max(all_scores)
#     else:
#         assert ab_score == min(all_scores)



# def test_eval_is_white_perspective():
#     board = chess.Board()

#     # Remove black queen, so White is clearly winning
#     board.remove_piece_at(chess.D8)

#     board.turn = chess.WHITE
#     white_turn_eval = evaluate_Claude_Shannon(board)

#     board.turn = chess.BLACK
#     black_turn_eval = evaluate_Claude_Shannon(board)

#     print("White turn eval:", white_turn_eval)
#     print("Black turn eval:", black_turn_eval)

#     assert white_turn_eval > 0
#     assert black_turn_eval > 0

