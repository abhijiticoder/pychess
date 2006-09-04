import sys
from copy import deepcopy
from Utils.Piece import Piece
from Utils.Cord import Cord

class Board:
    def __init__ (self, array):
        self.data = array
    
    def move (self, move):
        board = Board(deepcopy(self.data))
        cord0, cord1 = move.cords
        board[cord1] = board[cord0]
        board[cord0] = None
        if move.enpassant:
            board[move.enpassant] = None
        if move.castling:
            board[move.castling[1]] = board[move.castling[0]]
            board[move.castling[0]] = None
        if board[cord1].sign == "p" and cord1.y in [0,7]:
            board[cord1] = Piece(board[cord1].color, move.promotion)
        return board
    
    def __getitem__(self, cord):
        if type(cord) == int:
            return self.data[cord]
        return self.data[cord.y][cord.x]
    
    def __setitem__(self, cord, piece):
        self.data[cord.y][cord.x] = piece
        
    def __delitem__(self, cord):
        self[cord] = None
        
    def __repr__ (self):
        return repr(self.data)

    def __len__ (self):
        return len(self.data)

    def __repr__ (self):
        b = ""
        for r in range(7,-1,-1):
            row = self.data[r]
            for piece in row:
                if piece:
                    sign = piece.name[:1]
                    sign = piece.color == "white" and sign.upper() or sign.lower()
                    b += sign
                else: b += "."
                b += " "
            b += "\n"
        return b

    def getCord (self, piece):
        for row in range(len(self.data)):
            for col in range(len(self.data[row])):
                if self.data[row][col] == piece:
                    return Cord (col, row)
    