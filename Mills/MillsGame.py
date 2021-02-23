from __future__ import print_function
import sys
sys.path.append('..')
from Game import Game
from .MillsLogic import Board
import numpy as np

"""
Game class implementation for the game of TicTacToe.
Based on the OthelloGame then getGameEnded() was adapted to new rules.

Author: Evgeny Tyurin, github.com/evg-tyurin
Date: Jan 5, 2018.

Based on the OthelloGame by Surag Nair.
"""


class MillsGame(Game):

    def __init__(self, n=3):
        self.n = n
        self.m = n*3-1

    def getInitBoard(self):
        # return initial board (numpy board)
        b = Board(self.n)
        return b.pieces

    def getBoardSize(self):
        # (a,b) tuple
        return self.n+1, self.n*3-1

    def getActionSize(self):
        # return number of actions
        return self.n*(self.n*3-1) + 1

    def getNextState(self, board, player, action):
        # if player takes action on board, return next (board,player)
        # action must be a valid move
        b = Board(self.n)
        b.pieces = np.copy(board)
        if action == self.n*(self.n*3-1):
            b.switch_color()
            return board, b.get_color()

        move = (int(action/self.m), action%self.m)
        b.execute_move(move, player)
        return b.pieces, b.get_color()

    def getValidMoves(self, board, player):
        # return a fixed size binary vector
        valids = [0]*self.getActionSize()
        b = Board(self.n)
        b.pieces = np.copy(board)
        legalMoves =  b.get_legal_moves()
        if len(legalMoves)==0:
            valids[-1]=1
            return np.array(valids)
        for x, y in legalMoves:
            valids[self.m*x+y]= 1
        return np.array(valids)

    def getGameEnded(self, board, player):
        # return 0 if not ended, 1 if player 1 won, -1 if player 1 lost
        # player = 1
        b = Board(self.n)
        b.pieces = np.copy(board)
        if not b.has_legal_moves():
            return -player
        return b.get_win()

    def getCanonicalForm(self, board, player):
        # return state if player==1, else return -state if player==-1
        cf = np.copy(board)
        for k in range(self.n):
            for j in range(self.m):
                cf[k][j]== cf[k][j]*player
        cf[self.n][6] = cf[self.n][6]*player
        return cf

    def getSymmetries(self, board, pi):
        # mirror, rotational
        assert(len(pi) == self.n*(self.n*3-1) + 1)  # 1 for pass
        pi_board = np.reshape(pi[:-1], (self.n, self.m))
        l = []

        for i in range(1, 5):
            for j in [True, False]:
                newB = np.rot90(board, i)
                newPi = np.rot90(pi_board, i)
                if j:
                    newB = np.fliplr(newB)
                    newPi = np.fliplr(newPi)
                l += [(newB, list(newPi.ravel()) + [pi[-1]])]
        return l

    def stringRepresentation(self, board):
        # 8x8 numpy array (canonical board)
        return board.tostring()

    @staticmethod
    def display(board):
        print(board)
