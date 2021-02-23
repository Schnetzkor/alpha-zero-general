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


    def __init__(self, n=3):
        """Set up initial board configuration.
        """

        self.n = n
        self.m = n * 3 - 1

        # Create the empty board array.
        self.pieces = np.zeros((n + 1, self.m), np.int8)

        # n, 0 gamestage 0 = PlacingStage; 1 = Gamephase; 2 = Endgamephase
        # n, 1 movestage 0 = choosing square, 1 moving square, 2 kicking square
        # n, 2 #placecounter
        # n, 3 #drawcounter
        # n, 4 n, 5 = lastmove
        # n, 6 = color
        # n, 7 = wining variable


    # add [][] indexer syntax to the Board
    def __getitem__(self, index):

        return self.pieces[index]

    def get_gamestage(self, color):
        self.determine_status()
        return self.pieces[self.n][0]

    def get_movestage(self):
        return self.pieces[self.n][1]

    def get_place_counter(self):
        return self.pieces[self.n][2]

    def get_draw_counter(self):
        return self.pieces[self.n][3]

    def get_last_move(self):
        return self.pieces[self.n][4], self.pieces[self.n][5]

    def get_color(self):
        return self.pieces[self.n][6]

    def get_win(self):
        return self.pieces[self.n][7]




    def end_placingstage(self):
        self.pieces[self.n][0] = 1

    def set_movestage(self, i):
        self.pieces[self.n][1] = i

    def set_win(self, i):
        self.pieces[self.n][3] = i

    def setlastmove(self, k, j):
        self.pieces[self.n][4] = k
        self.pieces[self.n][5] = j

    def determine_status(self):
        temp = 0
        temp2 = 0
        color = self.getColor()
        for j in range(self.n):
            for i in range(self.m):
                if self.pieces[j][i] == color:
                    temp = temp + 1
                if self.pieces[j][i] == -color:
                    temp2 = temp2 + 1

        if temp2 < 3:
            self.set_win(color)
        elif self.counter == 50:
            self.set_win(1e-4)
        elif temp == 3:
            self.pieces[self.n][0] = self.pieces[self.n][0] * 2
        else:
            self.pieces[self.n][0] = 1


    def get_legal_moves(self, color):

        """Returns all the legal moves for the given color.
        (1 for white, -1 for black)
        @param color not used and came from previous version.

        """
        gamestage = self.get_gamestage()
        movestage = self.get_movestage()

        moves = set()  # stores the legal moves.
        #put square on board
        if (gamestage == 0 and movestage == 0) or (gamestage == 2 and movestage == 1):
            # returns all empty squares
            for j in range(self.n):
                for i in range(self.m):
                    if self.pieces[j][i] == 0:
                        newmove = (j, i)
                        moves.add(newmove)
        #choose square to move
        if gamestage >= 1 and movestage == 0:
            for j in range(self.n):
                for i in range(self.m):
                    if self.pieces[j][i] == color:
                        if self[self.gamestageIndex] == 2:
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
        if gamestage == 1 and movestage == 1:
            j, i = self.get_last_move()
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
        if movestage == 2:
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
            if self.pieces[j][(i+1) % self.m] == color and self.pieces[j][(i + self.m - 1) % self.m] == color:
                return True
            temp = 0
            for k in range(self.n):
                if self.pieces[k][ i] == color:
                    temp = temp + 1
            if temp == self.n:
                return True
        else:
            if self.pieces[j][(i + 1) % self.m] == color and self.pieces[j][(i + 2) % self.m] == color:
                return True
            if self.pieces[j][(i + self.m - 1) % self.m] == color and \
                    self.pieces[j][(i + self.m - 2) % self.m] == color:
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
            self.is_win(color)


        if self.movestage == 2:
            self.pieces[x, y] = 0
            self.is_win(color)


        if self.gamestage >= 1 and self.movestage == 0:
            self.last_move = move
            self.movestage = 1
            self.is_win(color)

        if self.gamestage == 1 and self.movestage == 1:
            self.pieces[self.last_move] = 0
            self.pieces[move] = color
            if self.is_in_mill(move):
                self.movestage = 2
            self.is_win(color)
            return













