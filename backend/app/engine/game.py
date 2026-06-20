import chess
import math
   
PIECE_VALUES = {
    chess.PAWN: 1,
    chess.KNIGHT: 3,
    chess.BISHOP: 3,
    chess.ROOK: 5,
    chess.QUEEN: 9,
    chess.KING: 0,
}


class Game():
    def __init__(self):
        self.board = chess.Board()
        self.draw = False
        self.white_mat_score = {
            chess.PAWN: 8,
            chess.KNIGHT: 2,
            chess.BISHOP: 2,
            chess.ROOK: 2,
            chess.QUEEN: 1,
            chess.KING: 1,
        }
        self.black_mat_score = {
            chess.PAWN: 8,
            chess.KNIGHT: 2,
            chess.BISHOP: 2,
            chess.ROOK: 2,
            chess.QUEEN: 1,
            chess.KING: 1,
        }
        

    def update_board_from_fen(self, fen: str):
        self.board = chess.Board(fen=fen)

    def update_draw(self, status: bool):
        self.draw = status

    def get_material_score(self, color: bool):
        if color == chess.WHITE:
            return sum(self.white_mat_score.values())
        else:
            return sum(self.black_mat_score.values())


    def get_state(self):
        return {
            "fen": self.board.fen(),
            "turn": "white" if self.board.turn else "black",
            "legal_moves": self.get_legal_moves(),
            "status": self.get_status(),
            "last_move": self.get_last_move(),
        }
    
    def get_legal_moves(self):
        return [ move.uci() for move in self.board.legal_moves ]
    
    def get_legal_moves_from_board(board: chess.Board):
        return [ move.uci() for move in board.legal_moves ]
    
    def make_move(self, move_uci):
        if move_uci not in self.get_legal_moves():
            raise ValueError("Illegal move: " + move_uci)
        
        move = chess.Move.from_uci(move_uci)


        if self.board.is_capture(move):
            victim = self.board.piece_at(move.to_square)
            if self.board.turn == chess.WHITE:
                self.black_mat_score[victim.piece_type] -= 1
            else:
                self.white_mat_score[victim.piece_type] -= 1

        self.board.push(move)

        

        return self.get_state()
    
    def undo_move(self):
        # Returns move that was undone
        if not self.board.move_stack:
            raise ValueError("Last move does not exist")
        
        move = self.board.pop()
        print("Undid " + move.uci())


        if self.board.is_capture(move):
            victim = self.board.piece_at(move.to_square)
            if self.board.turn == chess.WHITE:
                self.black_mat_score[victim.piece_type] += 1
            else:
                self.white_mat_score[victim.piece_type] += 1

        ret = { 
            "undone_move": move.uci(),
            "state": self.get_state()
        }
        return ret

    def get_status(self):
        if self.board.is_checkmate():
            return "checkmate"
        if self.board.is_stalemate():
            return "stalemate"
        if self.board.is_check():
            return "check"
        if self.board.is_game_over(claim_draw=self.draw):
            return "game_over"
        return "active"
    
    def get_fen(self):
        return self.board.fen()
    
    def get_turn(self):
        return "white" if self.board.turn else "black"
    
    
    def get_last_move(self):
        if not self.board.move_stack:
            return None
        return self.board.move_stack[-1].uci()
    
    def is_game_over(self):
        go = self.board.is_game_over()
        return go
    
    def claim_draw(self):
        self.draw = True


    
    def is_piece(board: chess.Board, sq: chess.Square, pc: str):
        piece = board.piece_at(sq)
        if piece is None:
            return 0
        
        return 1 if piece.symbol == pc else 0
         

        

    def count_pieces(board_fen: str):
        x = board_fen.split(' ')
        sfen = x[0]
        
        seen = {
            "K": 0,
            "Q": 0,
            "R": 0,
            "B": 0,
            "N": 0,
            "P": 0,
            "k": 0,
            "q": 0,
            "r": 0,
            "b": 0,
            "n": 0,
            "p": 0,
        }

        for char in sfen:
            if not char in seen: 
                continue
            seen[char] += 1
        
        return seen


    def print_board(board_fen: str):
        x = board_fen.split(' ')
        sfen = x[0]
        board = sfen.split('/')
        res = []
        print()
        for row in board:
            p = ''
            for c in row:
                if str.isdigit(c):
                    p+= "." * int(c)
                else:
                    p+= c
            res += [p]
                
            
            print(p)
        print()

        return res
    
    def board_as_string(board_fen: str):
        x = board_fen.split(' ')
        sfen = x[0]
        board = sfen.split('/')
        res = []
        for row in board:
            p = ''
            for c in row:
                if str.isdigit(c):
                    p+= "." * int(c)
                else:
                    p+= c
            res += [p]
        return res


    def isolated_pawn_count(board_fen: str, color: bool):
        x = board_fen.split(' ')
        sfen = x[0]
        board = Game.board_as_string(sfen)
        pawn = 'P' if color else 'p'
        count = 0

        for i in range(8):
            if pawn not in board[i]:
                continue

            for j in range(8):
                pos = board[i][j]

                if pos == pawn:
                    if j > 0 and j < 7:
                        
                        leftcol = [row[j-1] for row in board]
                        rightcol = [row[j+1] for row in board]
                        
                        if pawn in leftcol or pawn in rightcol:
                            continue 
                        count += 1

                    elif j > 0:
                        leftcol = [row[j-1] for row in board]
                        if pawn not in leftcol:
                            count += 1

                    elif j < 7:
                        rightcol = [row[j+1] for row in board]
                        if pawn not in rightcol:
                            count += 1

                    else:
                        continue

        return count
    
    def doubled_pawn_count(board_fen: str, color: bool):
        x = board_fen.split(' ')
        sfen = x[0]
        board = Game.board_as_string(sfen)
        pawn = 'P' if color else 'p'
        count = 0

        for i in range(8):
            col = [row[i] for row in board]
            if pawn not in col:
                continue

            num = 0
            for piece in col:
                if piece == pawn:
                    num += 1
        
            if num > 1:
                count += 1

        return count
    
    def blocked_pawns_count(board_fen: str, color: bool):
        x = board_fen.split(' ')
        sfen = x[0]
        board = Game.board_as_string(sfen)
        pawn = 'P' if color else 'p'
        oppPieces = [ "P" ,"N", "B", "R", "Q", "K" ] if not color else [ "p", "n", "b", "r", "q", "k" ]
        forward = -1 if color else 1
        count = 0

        for i in range(8):
            if pawn not in board[i]:
                continue

            for j in range(8):
                piece = board[i][j]
                if piece == pawn:
                    if board[i+forward][j] in oppPieces:
                        count += 1
        
        return count
                



            


