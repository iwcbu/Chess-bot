


from app.engine.evaluation import eval_simplified, evaluate_Claude_Shannon
from app.engine.game import Game
import chess


def test_eval_simplified():
    game = Game()
    game.update_board_from_fen('r1bqk2r/1ppp1ppp/p1n2n2/1B2p3/4P3/2N2N2/PPPP1PPP/R1BQ1RK1 w kq - 0 6')

    evl = eval_simplified(game.board)
    evl2 = evaluate_Claude_Shannon(game.board)
    assert evl > evl2
    assert evl == evl2
