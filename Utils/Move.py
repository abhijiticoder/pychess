from Utils.Cord import Cord

class Move:
    enpassant = None # None, Cord
    castling = None # None, (rook cord0, rook cord1)
    promotion = None # "q", "r", "b", "k"

    def _get_cords (self):
        return (self.cord0, self.cord1)
    cords = property(_get_cords)
    
    def __init__ (self, history, move, promotion="q"):
        """(board, notat) or
           (board, (cord0, cord1), [promotion]) or
           (board, (strcord1, strcord2), [promotion])
           Promotion will be set to None, if not aplieable"""
        
        self.number = number = len(history) -1
        board = history[-1]
        
        if type(move) in (list, tuple):
            if type(move[0]) == str:
                self.cord0, self.cord1 = [Cord(a) for a in move]
            else: self.cord0, self.cord1 = move
            if board[self.cord0].sign == "k":
                r = self.cord0.y
                if self.cord0.x - self.cord1.x == -2:
                    self.castling = (Cord(7,r),Cord(5,r))
                elif self.cord0.x - self.cord1.x == 2:
                    self.castling = (Cord(0,r),Cord(3,r))
            elif board[self.cord0].sign == "p" and self.cord0.y in [3,4]:
                if self.cord0.x != self.cord1.x and board[self.cord1] == None:
                    self.enpassant = Cord(self.cord1.x, self.cord0.y)
        
        else:
            notat = move
            notat = notat.strip().lower()
            if notat.endswith("+"):
                notat = notat[:-1]
            color = number % 2 == 0 and "white" or "black"
            
            if notat.startswith("o-o"):
                if color == white:
                    row = "1"
                else: row = "8"
                self.cord0 = Cord("e"+row)
                if notat == "o-o":
                    self.cord1 = Cord("g"+row)
                    self.castling = (Cord("h"+row), Cord("f"+row))
                else:
                    self.cord1 = Cord("c"+row)
                    self.castling = (Cord("a"+row), Cord("d"+row))
    
            elif "x" in notat:
                since, then = notat.split("x")
                self.cord1 = Cord(then)
                if not since[0] in "abcdefgh":
                    pass #TODO: Most first have a working validator
        
        if self.cord1.y in (0,7) and board[self.cord0].sign == "p":
            self.promotion = promotion

    def algNotat (self, history):
        board = history[-1]
        
        c0, c1 = self.cords
        if board[c0].sign == "k":
            if c0.x - c1.x == 2:
                return "o-o-o"
            elif c0.x - c1.x == -2:
                return "o-o"
        
        part0 = part1 = ""
        
        if board[c0].sign != "p":
            part0 += board[c0].sign.upper()
        
        part1 = str(c1)
        
        if board[c1] != None:
            part1 = "x" + part1
            if board[c0].sign == "p":
                part0 += c0.cx
                
        notat = part0 + part1
        if board[c0].sign == "p" and c1.y in [0,7]:
            notat += self.promotion
        
        from Utils.validator import willChess
        opcolor = board[c0].color == "white" and "black" or "white"
        if willChess(history, self, opcolor):
            notat += "+"
            
        return notat
    
    def __repr__ (self):
        s = str(self.cord0) + str(self.cord1) 
        if self.promotion:
            return s + self.promotion
        return s