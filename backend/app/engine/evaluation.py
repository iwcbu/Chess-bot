# backend/app/engine/evaluation.py

from app.engine.game import Game
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
        if board.is_checkmate():
            return -math.inf if board.turn == chess.WHITE else math.inf
        else:
            return 0
    
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

    mobilituScore = 0.03 * (white_mobility - black_mobility)

    white_score = materialScore + mobilituScore - pawnPosScore

    return white_score







def manhattan_distance(sq1: chess.Square, sq2: chess.Square):
    file1 = chess.square_file(sq1)
    rank1 = chess.square_rank(sq1)

    file2 = chess.square_file(sq2)
    rank2 = chess.square_rank(sq2)

    return abs(file1 - file2) + abs(rank1 - rank2)

def closeness_bonus(piece_type: chess.PieceType, distance: int):
    base = max(0, 14 - distance)

    match piece_type:
        case chess.QUEEN:
            return base * 2.5
        case chess.ROOK:
            return base * 0.5
        case chess.KNIGHT:
            return base
        case chess.BISHOP:
            return base * 0.3
        
    return 0


def king_tropism_score(board: chess.Board):
    white_king = board.king(chess.WHITE)
    black_king = board.king(chess.BLACK)

    white_king_pressure = 0
    black_king_pressure = 0

    for square, piece in board.piece_map().items():
        if piece.piece_type == chess.KING or piece.piece_type == chess.PAWN:
            continue

        if piece.color == chess.WHITE:
            distance = manhattan_distance(square, black_king)
            black_king_pressure += closeness_bonus(piece.piece_type, distance)
            
        else:
            distance = manhattan_distance(square, white_king)
            white_king_pressure += closeness_bonus(piece.piece_type, distance)
    
    return (black_king_pressure - white_king_pressure) / 100




wp_table = [
     0,  0,  0,  0,  0,  0,  0,  0,
    50, 50, 50, 50, 50, 50, 50, 50,
    10, 10, 20, 30, 30, 20, 10, 10,
    5,  5, 10, 25, 25, 10,  5,  5,
    0,  0,  0, 20, 20,  0,  0,  0,
    5, -5,-10,  0,  0,-10, -5,  5,
    5, 10, 10,-20,-20, 10, 10,  5,
    0,  0,  0,  0,  0,  0,  0,  0
]

wn_table = [
    -50,-40,-30,-30,-30,-30,-40,-50,
    -40,-20,  0,  0,  0,  0,-20,-40,
    -30,  0, 10, 15, 15, 10,  0,-30,
    -30,  5, 15, 20, 20, 15,  5,-30,
    -30,  0, 15, 20, 20, 15,  0,-30,
    -30,  5, 10, 15, 15, 10,  5,-30,
    -40,-20,  0,  5,  5,  0,-20,-40,
    -50,-40,-30,-30,-30,-30,-40,-50,
]

wb_table = [
    -20,-10,-10,-10,-10,-10,-10,-20,
    -10,  0,  0,  0,  0,  0,  0,-10,
    -10,  0,  5, 10, 10,  5,  0,-10,
    -10,  5,  5, 10, 10,  5,  5,-10,
    -10,  0, 10, 10, 10, 10,  0,-10,
    -10, 10, 10, 10, 10, 10, 10,-10,
    -10,  5,  0,  0,  0,  0,  5,-10,
    -20,-10,-10,-10,-10,-10,-10,-20,
]

wr_table = [
      0,  0,  0,  0,  0,  0,  0,  0,
    5, 10, 10, 10, 10, 10, 10,  5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    0,  0,  0,  5,  5,  0,  0,  0
]

wq_table = [
    -20,-10,-10, -5, -5,-10,-10,-20,
    -10,  0,  0,  0,  0,  0,  0,-10,
    -10,  0,  5,  5,  5,  5,  0,-10,
    -5,  0,  5,  5,  5,  5,  0, -5,
    0,  0,  5,  5,  5,  5,  0, -5,
    -10,  5,  5,  5,  5,  5,  0,-10,
    -10,  0,  5,  0,  0,  0,  0,-10,
    -20,-10,-10, -5, -5,-10,-10,-20
]

wk_table = [
    -30,-40,-40,-50,-50,-40,-40,-30,
    -30,-40,-40,-50,-50,-40,-40,-30,
    -30,-40,-40,-50,-50,-40,-40,-30,
    -30,-40,-40,-50,-50,-40,-40,-30,
    -20,-30,-30,-40,-40,-30,-30,-20,
    -10,-20,-20,-20,-20,-20,-20,-10,
    20, 20,  0,  0,  0,  0, 20, 20,
    20, 30, 10,  0,  0, 10, 30, 20
]


wk_endgame_table = [
    -50,-40,-30,-20,-20,-30,-40,-50,
    -30,-20,-10,  0,  0,-10,-20,-30,
    -30,-10, 20, 30, 30, 20,-10,-30,
    -30,-10, 30, 40, 40, 30,-10,-30,
    -30,-10, 30, 40, 40, 30,-10,-30,
    -30,-10, 20, 30, 30, 20,-10,-30,
    -30,-30,  0,  0,  0,  0,-30,-30,
    -50,-30,-30,-30,-30,-30,-30,-50
]

bp_table = [
    0,  0,  0,  0,  0,  0,  0,  0,
    5, 10, 10,-20,-20, 10, 10,  5,
    5, -5,-10,  0,  0,-10, -5,  5,
    0,  0,  0, 20, 20,  0,  0,  0,
    5,  5, 10, 25, 25, 10,  5,  5,
    10, 10, 20, 30, 30, 20, 10, 10,
    50, 50, 50, 50, 50, 50, 50, 50,
     0,  0,  0,  0,  0,  0,  0,  0
]

bn_table = [
    -50,-40,-30,-30,-30,-30,-40,-50,
    -40,-20,  0,  5,  5,  0,-20,-40,
    -30,  5, 10, 15, 15, 10,  5,-30,
    -30,  0, 15, 20, 20, 15,  0,-30,
    -30,  5, 15, 20, 20, 15,  5,-30,
    -30,  0, 10, 15, 15, 10,  0,-30,
    -40,-20,  0,  0,  0,  0,-20,-40,
    -50,-40,-30,-30,-30,-30,-40,-50
]

bb_table = [
    -20,-10,-10,-10,-10,-10,-10,-20,
    -10,  5,  0,  0,  0,  0,  5,-10,
    -10, 10, 10, 10, 10, 10, 10,-10,
    -10,  0, 10, 10, 10, 10,  0,-10,
    -10,  5,  5, 10, 10,  5,  5,-10,
    -10,  0,  5, 10, 10,  5,  0,-10,
    -10,  0,  0,  0,  0,  0,  0,-10,
    -20,-10,-10,-10,-10,-10,-10,-20
]

br_table = [
    0,  0,  0,  5,  5,  0,  0,  0,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    5, 10, 10, 10, 10, 10, 10,  5,
    0,  0,  0,  0,  0,  0,  0,  0
]

bq_table = [
    -20,-10,-10, -5, -5,-10,-10,-20
    -10,  0,  5,  0,  0,  0,  0,-10,
    -10,  5,  5,  5,  5,  5,  0,-10,
    0,  0,  5,  5,  5,  5,  0, -5,
    -5,  0,  5,  5,  5,  5,  0, -5,
    -10,  0,  5,  5,  5,  5,  0,-10,
    -10,  0,  0,  0,  0,  0,  0,-10,
    -20,-10,-10, -5, -5,-10,-10,-20,
]

bk_table = [
    20, 30, 10,  0,  0, 10, 30, 20,
    20, 20,  0,  0,  0,  0, 20, 20,
    -10,-20,-20,-20,-20,-20,-20,-10,
    -20,-30,-30,-40,-40,-30,-30,-20,
    -30,-40,-40,-50,-50,-40,-40,-30,
    -30,-40,-40,-50,-50,-40,-40,-30,
    -30,-40,-40,-50,-50,-40,-40,-30,
    -30,-40,-40,-50,-50,-40,-40,-30
]


bk_endgame_table = [
    -50,-30,-30,-30,-30,-30,-30,-50,
    -30,-30,  0,  0,  0,  0,-30,-30,
    -30,-10, 20, 30, 30, 20,-10,-30,
    -30,-10, 30, 40, 40, 30,-10,-30,
    -30,-10, 30, 40, 40, 30,-10,-30,
    -30,-10, 20, 30, 30, 20,-10,-30,
    -30,-20,-10,  0,  0,-10,-20,-30,
    -50,-40,-30,-20,-20,-30,-40,-50
]

def piece_table_score(board: chess.Board):
    
    score = 0

    for square, piece in board.piece_map().items():
        match piece.symbol():
            case "p":
                score -= bp_table[square]
            case "n":
                score -= bn_table[square]
            case "b":
                score -= bb_table[square]
            case "r":
                score -= br_table[square]
            case "q":
                score -= bq_table[square]
            case "k":
                score -= bk_table[square]
            case "P":
                score += wp_table[square]
            case "N":
                score += wn_table[square]
            case "B":
                score += wb_table[square]
            case "R":
                score += wr_table[square]
            case "Q":
                score += wq_table[square]
            case "K":
                score += wk_table[square]

    return score / 100

   
PIECE_VALUES = {
    chess.PAWN: 10,
    chess.KNIGHT: 35,
    chess.BISHOP: 33,
    chess.ROOK: 50,
    chess.QUEEN: 600,
    chess.KING: 0,
}

PIECE_VALUES_ATTACKING = {
    chess.PAWN: 1,
    chess.KNIGHT: 10,
    chess.BISHOP: 12,
    chess.ROOK: 30,
    chess.QUEEN: 70,
    chess.KING: 0
}

def check_if_mate_in_one(board: chess.Board):
    score = 0

    if board.turn == chess.WHITE:

        for move in list(board.legal_moves):
            board.push(move)
            if board.is_checkmate():
                score += 100
            board.pop()
        
        return score
    
    else:

        for move in list(board.legal_moves):
            board.push(move)
            if board.is_checkmate():
                score -= 10000
            board.pop()
        
        return score / 100






def eval_simplified(board: chess.Board):
    eval = evaluate_Claude_Shannon(board)
    print(eval)
    eval += king_tropism_score(board)
    print(eval)
    eval += piece_table_score(board)
    print(eval)
    eval += check_if_mate_in_one(board)

    return round(eval, 2)


def test_eval_simplified():
    game = Game()
    game.update_board_from_fen('r1bqk2r/1ppp1ppp/p1n2n2/1B2p3/4P3/2N2N2/PPPP1PPP/R1BQ1RK1 w kq - 0 6')
    evl = eval_simplified(game.board)
    print("test-eval: ", evl, " on fen: ", game.board.fen())

    game.update_board_from_fen('rnbqkbnr/pppp1ppp/8/4p3/5PP1/8/PPPPP2P/RNBQKBNR b KQkq g3 0 2')
    evl = eval_simplified(game.board)
    print("test-eval: ", evl, " on fen: ", game.board.fen())

def test_eval_simplified2():
    game = Game()
    evl = eval_simplified(game.board)
    print("test-eval: ", evl, " on fen: ", game.board.fen())

def test_eval_simplified3():
    game = Game()
    game.update_board_from_fen('r2qkb1r/pppn1ppp/5n2/3pN3/3PP1b1/2P5/PP1N1PPP/R1BQKB1R b KQkq - 0 7')
    evl = eval_simplified(game.board)
    print("test-eval: ", evl, " on fen: ", game.board.fen())

def test_eval_simplified4():
    game = Game()
    game.update_board_from_fen('rnb1kb1r/ppp2ppp/5n2/q3p3/1P6/P1N2N2/2PP1PPP/R1BQKB1R b KQkq - 0 6')
    evl = eval_simplified(game.board)
    print("test-eval: ", evl, " on fen: ", game.board.fen())

# test_eval_simplified()
# test_eval_simplified2()
test_eval_simplified3()
# test_eval_simplified4()
