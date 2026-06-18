# backend/app/tests/test_game.py

from app.engine.game import Game
import chess
import pytest

class TestGameClass:
    def test_init(self):
        game = Game()
        assert game.get_fen() == chess.Board().fen()
        assert game.draw == False

    def test_game_state(self):
        game = Game()
        state = game.get_state()

        assert "fen" in state
        assert "turn" in state
        assert "legal_moves" in state
        assert "status" in state
        assert "last_move" in state

    def test_get_legal_moves(self):
        game = Game()
        lms = game.get_legal_moves()
        assert len(lms) == 20

    
    def test_make_move(self):
        game = Game()
        starting_fen = game.get_fen()
        lms = game.get_legal_moves()
        print(len(lms))
        move = lms[0]
        game.make_move(move)

        assert game.get_last_move() == move
        assert game.get_turn() == "black"
        assert game.get_fen() != starting_fen
        
    
    def test_undo_move(self):
        game = Game()
        starting_fen = game.get_fen()

        lms = game.get_legal_moves()
        move = lms[0]

        game.make_move(move)
        ret = game.undo_move()

        assert game.get_fen() == starting_fen
        assert ret['undone_move'] == move



    
    def test_get_status(self):
        game = Game()
        assert game.get_status() == 'active'
    
    def test_checkmate_status(self):
        game = Game()

        game.make_move("f2f3")
        game.make_move("e7e5")
        game.make_move("g2g4")
        game.make_move("d8h4")

        assert game.get_status() == "checkmate"
        assert game.is_game_over() == True
    
    def test_get_fen(self):
        game = Game()
        fen = game.get_fen()
        assert fen == "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    
    def test_get_turn(self):
        game = Game()
        assert game.get_turn() == 'white'
    
    def test_get_last_move(self):
        game = Game()
        lms = game.get_legal_moves()
        move = lms[0]
        game.make_move(move)
        last_move = game.get_last_move()
        assert move == last_move
    
    def test_is_game_over(self):
        game = Game()
        assert game.is_game_over() == False


    def test_illegal_move_raises_error(self):
        game = Game()

        with pytest.raises(ValueError):
            game.make_move("e2e5")

    def test_turn_changes_after_move(self):
        game = Game()
        game.make_move("g1h3")
        
        assert game.get_turn() == 'black'

    def test_last_move_is_none_at_start(self):
        game = Game()

        assert game.get_last_move() is None

    def test_undo_with_no_moves_raises_error(self):
        game = Game()

        with pytest.raises(ValueError):
            game.undo_move()

    def test_invalid_move_format_raises_error(self):
        game = Game()

        with pytest.raises(ValueError):
            game.make_move("not-a-move")

    def test_count_pieces(self):
        game = Game()

        pieces = Game.count_pieces(game.board.fen())

        assert pieces["K"] == 1
        assert pieces["k"] == 1
        assert pieces["Q"] == 1
        assert pieces["q"] == 1
        assert pieces["R"] == 2
        assert pieces["r"] == 2
        assert pieces["N"] == 2
        assert pieces["n"] == 2
        assert pieces["B"] == 2
        assert pieces["b"] == 2
        assert pieces["P"] == 8
        assert pieces["p"] == 8
    

    def test_number_isolated_pawns(self):
        fen = 'r1bqk2r/1p3p1p/2n1p3/3pP3/1b1P4/2N2N2/PPPQ1P1P/R1B1KBR1 b KQkq - 3 8'
        bc = Game.isolated_pawn_count(fen, False)
        wc = Game.isolated_pawn_count(fen, True)

        assert bc == 2
        assert wc == 1

    
    def test_number_doubled_pawn_files(self):
        fen = 'r1bqk2r/1p3p1p/1Pnpp3/1p1pP3/1b1P4/2N2N1P/PPPQ1P1P/R1B1KBR1 b KQkq - 3 8'
        bc = Game.isolated_pawn_count(fen, False)
        wc = Game.isolated_pawn_count(fen, True)

        assert bc == 2
        assert wc == 3
        
