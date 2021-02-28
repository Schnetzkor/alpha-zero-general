import numpy as np
"""
Random and Human-ineracting players for the game of TicTacToe.

Author: Simon Schnecko, github.com/Schnetzkor
Date: Jan 5, 2018.

Based on the TicTacToePlayer by Evgeny Tyurin.

"""
class RandomPlayer():
    def __init__(self, game):
        self.game = game

    def play(self, board):
        a = np.random.randint(self.game.getActionSize())
        valids = self.game.getValidMoves(board, 1)
        while valids[a]!=1:
            a = np.random.randint(self.game.getActionSize())
        print(a)
        return a


class HumanTicTacToePlayer():
    def __init__(self, game):
        self.game = game

    def play(self, board):
        # display(board)
        valid = self.game.getValidMoves(board, board[3][6])
        for i in range(len(valid)):

            if valid[i]:
                print(int(i / self.game.m), int(i%self.game.m), "; ", end="")
        while True: 
            # Python 3.x
            a = input()
            # Python 2.x 
            # a = raw_input()

            y, x = [int(x) for x in a.split(' ')]
            a = self.game.m * y + x if x!= -1 else self.game.n * (self.game.n * 3 - 1)
            if a <= self.game.m * self.game.n and valid[a]:
                break
            else:
                print('Invalid')

        return a
