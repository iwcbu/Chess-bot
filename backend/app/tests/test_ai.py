# backend/app/tests/test_ai.py

from app.engine.game import Game
from app.engine.evaluation import evaluate_Claude_Shannon
from app.engine.ai import choose_greedy_move, choose_random_move
import chess


class TestBot:

    def test_random_bot_returns_legal_move(self):
        game = Game()
        random_move = choose_random_move(game.board)
        assert random_move not in game.get_legal_moves()
        
        

    def test_greedy_bot_returns_legal_move(self):
        game = Game()
        greedy_move = choose_greedy_move(game.board)
        assert greedy_move not in game.get_legal_moves()      
        

    def test_starting_evaluation_is_equal(self):
        game = Game()
        posEval = evaluate_Claude_Shannon(game.board)
        
        assert posEval == 0
        

    def test_evaluation_changes_after_capture(self):
        game = Game()
        game.update_board_from_fen('rnbqkbnr/ppp2ppp/8/3pp3/3P4/2N5/PPP1PPPP/R1BQKBNR w KQkq - 1 2')
        prevEval = evaluate_Claude_Shannon(game.board)
        
        Nd5 = chess.Move.from_uci('c3d5')
        if 'c3d5' not in game.get_legal_moves():
            raise ValueError("Ian you're stupid")
        
        game.board.push(Nd5)

        curEval = evaluate_Claude_Shannon(game.board)

        assert prevEval <= curEval



