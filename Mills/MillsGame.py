from __future__ import print_function
import sys
sys.path.append('..')
from Game import Game
from .MillsLogic import Board
import numpy as np
import pygame
from Mills import GUI
"""
Game class implementation for the game of TicTacToe.
Based on the OthelloGame then getGameEnded() was adapted to new rules.

Author: Evgeny Tyurin, github.com/evg-tyurin
Date: Jan 5, 2018.

Based on the OthelloGame by Surag Nair.
"""


class MillsGame(Game):

    def __init__(self, n=3, isgui=False):
        self.n = n
        self.m = n*3-1
        self.gui = isgui
        if self.isgui:
            GUI.drawbackground()
            GUI.drawlines()
            pygame.display.update()
            pygame.time.wait(30000)


    def getInitBoard(self):
        # return initial board (numpy board)
        b = Board(self.n)
        return np.array(b.pieces)

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
        if b.get_draw_counter() >= 50:
            return 1e-4
        return b.get_win()

    def getCanonicalForm(self, board, player):
        # return state if player==1, else return -state if player==-1
        cf = np.copy(board)
        for k in range(self.n):
            for j in range(self.m):
                cf[k][j] = cf[k][j]*player
        cf[self.n][6] = cf[self.n][6]*player
        return cf

    def getSymmetries(self, board, pi):
        # mirror, rotational
        assert (len(pi) == (self.n) * (self.n * 3 - 1) + 1)  # 1 for pass
        pi_board = np.reshape(pi[:-1], (self.n, self.m))
        b = np.copy(board)
        status_board = [b[-1]]
        playing_board = b[:-1]

        symmetries = []

        for i in range(1, int((self.m / 2 + 1))):
            # rotate around
            rolling_board = np.roll(playing_board, i * 2, 1)
            roling_pi = np.roll(pi_board, i * 2, 1)
            symmetries += [(np.concatenate((rolling_board, status_board)), list(roling_pi.ravel()) + [pi[-1]])]
            # inside out
            ud_rolling_board = np.flipud(rolling_board)
            ud_rolling_pi = np.flipud(roling_pi)
            symmetries += [(np.concatenate((ud_rolling_board, status_board)), list(ud_rolling_pi.ravel()) + [pi[-1]])]
            # mirror
            mirror_board = np.roll(np.fliplr(playing_board), 1 + i * 2, 1)
            mirror_pi = np.roll(np.fliplr(pi_board), 1 + i * 2, 1)
            symmetries += [(np.concatenate((mirror_board, status_board)), list(mirror_pi.ravel()) + [pi[-1]])]
            # inside out
            ud_mirror_board = np.flipud(mirror_board)
            ud_rollingM_pi = np.flipud(mirror_pi)
            symmetries += [(np.concatenate((ud_mirror_board, status_board)), list(ud_rollingM_pi.ravel()) + [pi[-1]])]
        return symmetries

    def stringRepresentation(self, board):
        # 8x8 numpy array (canonical board)
        return board.tostring()

    @staticmethod
    def display(board):
        #print(board)
        print(" %1d ------------- %1d ------------- %1d"% (board[2][7],board[2][0],board[2][1] ))
        print(" |              |                |")
        print(" |    %1d ------- %1d ------- %1d      |"% (board[1][7],board[1][0],board[1][1] ))
        print(" |     |        |         |      |")
        print(" |     |    %1d - %1d - %1d     |      |"% (board[0][7],board[0][0],board[0][1] ))
        print(" |     |    |       |     |      |")
        print(" %1d  -  %1d -  %1d        %1d  - %1d   -  %1d"% (board[2][6],board[1][6],board[0][6],board[0][2],board[1][2],board[2][2] ))
        print(" |     |    |       |     |      |")
        print(" |     |    %1d - %1d - %1d     |      |"% (board[0][5],board[0][4],board[0][3] ))
        print(" |     |        |         |      |")
        print(" |    %1d ------- %1d ------- %1d      |"% (board[1][5],board[1][4],board[1][3] ))
        print(" |              |                |")
        print(" %1d ------------- %1d ------------- %1d"% (board[2][5],board[2][4],board[2][3] ))

        print(" %2s ------------- %2s ------------- %2s" % ("27", "20", "21"))
        print(" |                 |                |")
        print(" |    %2s ------- %2s ------- %2s      |" % ("17", "10", "11"))
        print(" |     |           |         |      |")
        print(" |     |    %2s - %2s - %2s     |      |" % ("07", "00", "01"))
        print(" |     |    |          |     |      |")
        print(" %1s  -  %1s -  %1s        %1s  - %1s   -  %1s" % ("26", "16", "06", "02", "12", "22"))
        print(" |     |    |          |     |      |")
        print(" |     |    %2s - %2s - %2s     |      |" % ("05", "04", "03"))
        print(" |     |           |         |      |")
        print(" |    %2s ------- %2s ------- %2s      |" % ("15", "14", "13"))
        print(" |                 |                |")
        print(" %2s ------------- %2s ------------- %2s" % ("25", "24", "23"))

        print(board[3])
        if(board[3][1]== 0):
            print("wähle aus:")
        if (board[3][1] == 1):
            print("bewege:")
        if (board[3][1] == 2):
            print("töte:")

        GUI.updateboard(board)

