import numpy as np

'''
Board class for the game of Mills.
Default board size is 3x8.
Board data:
#todo
  1=white(O), -1=black(X), 0=empty
  first dim is column , 2nd is row:
     pieces[0][0] is the top left square,
     pieces[2][0] is the bottom left square,
Squares are stored and manipulated as (x,y) tuples.

Author: Simon Schnecko, github.com/Schnetzkor
Date: Feb 18, 2021.

Based on the board for the game of Othello by Eric P. Nichols.

'''


# from bkcharts.attributes import color
class Board():
    # list of all 4 directions on the board, as (x,y) offsets
    __directions = [(1, 0), (0, -1), (-1, 0), (0, 1)]

    def __init__(self, n=3):
        """Set up initial board configuration.
        """

        self.n = n
        self.m = n * 3 - 1
        self.counter = 0
        # Create the empty board array.
        self.pieces = np.zeros((n, self.m), np.int8)
        self.gamestage = 0  # gamestage 0 = PlacingStage; 1 = Gamephase; 2 = Endgamephase
        self.movestage = 0  # movestage 0 = choosing square, 1 moving square, 2 kicking square
        self.last_move = 2, 7
        self.pieces[2, 7] = -1
        #self.pieces[2, 0] = 0
        #self.pieces[2, 1] = -1
        #self.pieces[2, 6] = 0
        #self.pieces[1, 0] = -1

    # add [][] indexer syntax to the Board
    def __getitem__(self, indexI, indexJ):

        return self.pieces[indexI][indexJ]

    def get_legal_moves(self, color):

        """Returns all the legal moves for the given color.
        (1 for white, -1 for black)
        @param color not used and came from previous version.

        """
        moves = set()  # stores the legal moves.
        #put square on board
        if (self.gamestage == 0 and self.movestage == 0) or (self.gamestage == 2 and self.movestage == 1):
            # returns all empty squares
            for j in range(self.n):
                for i in range(self.m):
                    if self.pieces[j][i] == 0:
                        newmove = (j, i)
                        moves.add(newmove)
        #choose square to move
        if self.gamestage >= 1 and self.movestage == 0:
            for j in range(self.n):
                for i in range(self.m):
                    if self.pieces[j][i] == color:
                        if self.gamestage == 2:
                            newmove = (j, i)
                            moves.add(newmove)
                        elif self.pieces[j][(i + 1) % self.m] == 0 or \
                                self.pieces[j][(i + self.m - 1) % self.m] == 0:
                            newmove = (j, i)
                            moves.add(newmove)
                        elif i % 2 == 0 and ((j + 1 < self.n and self.pieces[j+1][i] == 0) or
                                             (j - 1 >= 0 and self.pieces[j-1][i] == 0)):
                            newmove = (j, i)
                            moves.add(newmove)
        #moving square to
        if self.gamestage == 1 and self.movestage == 1:
            j, i = self.last_move
            if self.pieces[j][(i + 1) % self.m] == 0:
                newmove = (j, (i + 1) % self.m)
                moves.add(newmove)
            if self.pieces[j][(i + self.m - 1) % self.m] == 0:
                newmove = (j, (i + self.m - 1) % self.m)
                moves.add(newmove)
            if i % 2 == 0:
                if j + 1 < self.n and self.pieces[j + 1][i] == 0:
                    newmove = (j + 1, i)
                    moves.add(newmove)
                if j - 1 >= 0 and self.pieces[j - 1][i] == 0:
                    newmove = (j - 1, i)
                    moves.add(newmove)
        #squares possible to kick from board
        if self.movestage == 2:
            for j in range(self.n):
                for i in range(self.m):
                    newmove = j, i
                    if self.pieces[newmove] == -color and not self.is_in_mill(newmove):
                        moves.add(newmove)

        return list(moves)

    def is_in_mill(self, piece):
        j, i = piece
        color = self.pieces[piece]
        if i % 2 == 0:
            if self.pieces[j, (i+1) % self.m] == color and self.pieces[j, (i + self.m - 1) % self.m] == color:
                return True
            temp = 0
            for k in range(self.n):
                if self.pieces[k, i] == color:
                    temp = temp + 1
            if temp == self.n:
                return True
        else:
            if self.pieces[j, (i + 1) % self.m] == color and self.pieces[j, (i + 2) % self.m] == color:
                return True
            if self.pieces[j, (i + self.m - 1) % self.m] == color and \
                    self.pieces[j, (i + self.m - 2) % self.m] == color:
                return True
        return False

    def has_legal_moves(self):
        if self.movestage == 2 or self.gamestage == 2:
            return True
        isempty1 = (len(self.get_legal_moves(1)) == 0)
        isempty2 = (len(self.get_legal_moves(-1)) == 0)
        if not (isempty1 or isempty2):
            return True

        return False

    def is_win(self, color):

        return False

    def end_gamestage_zero(self):
        if self.counter == self.n**2:
            self.gamestage = 1
            self.counter = 0
        else:
            self.counter = self.counter + 1

    def execute_move(self, move, color):
        """Perform the given move on the board; 
        color gives the color pf the piece to play (1=white,-1=black)
        """
        (x, y) = move
        if self.gamestage == 0:
            if self.movestage == 0:
                self.pieces[x, y] = color
                self.end_gamestage_zero()
                if self.is_in_mill(move):
                    self.movestage = 2

        if self.movestage == 2:
            self.pieces[x, y] == 0


        if self.gamestage >= 1 and self.movestage == 0:
            self.last_move = move
            self.movestage = 1

        if self.gamestage == 1 and self.movestage == 1:
            self.pieces[self.last_move] = 0
            self.pieces[move] = color
            if self.is_in_mill(move):
                self.movestage = 2









x = Board()
y = 2, 7
print(len(x.get_legal_moves(1)))
print(x.get_legal_moves(1))
