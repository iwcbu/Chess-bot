# # backend/app/tests/test_search.py

import chess
from app.engine.game import Game
from app.engine.search import choose_minimax_move, choose_minimax_with_ab_move

# def test_minimax_returns_legal_move():
#     game = Game()
#     move = choose_minimax_move(game.board, 0)

#     assert move.uci() in game.get_legal_moves()

# def test_minimax_depth_one():
#     game = Game()
#     move = choose_minimax_move(game.board, 1)

#     assert move.uci() in game.get_legal_moves()

# def test_minimax_depth_two():
#     game = Game()
#     move = choose_minimax_move(game.board, 2)

#     assert move.uci() in game.get_legal_moves()

# def test_minimax_handles_game_over():
#     game = Game()
#     game.board.push(chess.Move.from_uci('f2f3'))
#     game.board.push(chess.Move.from_uci('e7e5'))
#     game.board.push(chess.Move.from_uci('g2g4'))
#     game.board.push(chess.Move.from_uci('d8h4'))
#     assert game.board.is_valid() == True

#     move = choose_minimax_move(game.board, 1)
    
#     assert move == None


# def test_capture_queen():
#     game = Game()
#     game.board.push(chess.Move.from_uci('e2e4'))
#     game.board.push(chess.Move.from_uci('e7e5'))
#     game.board.push(chess.Move.from_uci('g2g3'))
#     game.board.push(chess.Move.from_uci('d8h4'))

#     assert game.board.is_valid() == True

#     move = choose_minimax_move(game.board, 1)

#     assert move.uci() == 'g3h4'


# def test_one_move_checkmate():
#     game = Game()
#     game.board.push(chess.Move.from_uci('f2f3'))
#     game.board.push(chess.Move.from_uci('e7e5'))
#     game.board.push(chess.Move.from_uci('g2g4'))

#     assert game.board.is_valid() == True

#     move = choose_minimax_move(game.board, 1)

#     assert move.uci() == 'd8h4'

# def test_board_state_unchanged():
#     game = Game()
#     starting_fen = game.board.fen()

#     move = choose_minimax_move(game.board, 2)

#     assert game.board.fen() == starting_fen




# Alpha beta pruning tests


def test_abMinimax_returns_legal_move():
    game = Game()
    move = choose_minimax_with_ab_move(game.board, 1)

    assert move.uci() in game.get_legal_moves()

def test_abMinimax__depth_four():
    game = Game()
    move = choose_minimax_with_ab_move(game.board, 3)

    assert move.uci() in game.get_legal_moves()

def test_abMinimax__depth_five():
    game = Game()
    move = choose_minimax_with_ab_move(game.board, 4)

    assert move.uci() in game.get_legal_moves()

def test_abMinimax__handles_game_over():
    game = Game()
    game.board.push(chess.Move.from_uci('f2f3'))
    game.board.push(chess.Move.from_uci('e7e5'))
    game.board.push(chess.Move.from_uci('g2g4'))
    game.board.push(chess.Move.from_uci('d8h4'))
    assert game.board.is_valid() == True

    move = choose_minimax_with_ab_move(game.board, 2)
    
    assert move == None


def test_abMinimax_capture_queen():
    game = Game()
    game.board.push(chess.Move.from_uci('e2e4'))
    game.board.push(chess.Move.from_uci('e7e5'))
    game.board.push(chess.Move.from_uci('g2g3'))
    game.board.push(chess.Move.from_uci('d8h4'))

    assert game.board.is_valid() == True

    move = choose_minimax_with_ab_move(game.board, 2)

    assert move.uci() == 'g3h4'


def test_abMinimax_one_move_checkmate():
    game = Game()
    game.board.push(chess.Move.from_uci('f2f3'))
    game.board.push(chess.Move.from_uci('e7e5'))
    game.board.push(chess.Move.from_uci('g2g4'))

    assert game.board.is_valid() == True

    move = choose_minimax_with_ab_move(game.board, 2)
    game.board.push(move)

    assert game.is_game_over() == True

def test_abMinimax_board_state_unchanged():
    game = Game()
    starting_fen = game.board.fen()

    move = choose_minimax_with_ab_move(game.board, 3)

    assert game.board.fen() == starting_fen






