import Arena
from MCTS import MCTS

#from tictactoe.TicTacToePlayers import *
#from tictactoe.TicTacToeGame import TicTacToeGame
#from tictactoe.keras.NNet import NNetWrapper as NNet

from Mills.MillsPlayers import *
from Mills.MillsGame import MillsGame
from Mills.keras.NNet import NNetWrapper as NNet

import numpy as np
from utils import *

"""
use this script to play any two agents against each other, or play manually with
any agent.
"""

human_vs_cpu = False
human_vs_human = False
g = MillsGame()
#g = TicTacToeGame()
# all players
rp = RandomPlayer(g).play
hp = HumanTicTacToePlayer(g).play


if not human_vs_human:
# nnet players
    n1 = NNet(g)

    n1.load_checkpoint('./Mills/pretrained/', 'best.pth.tar')#('./pretrained_models/tictactoe/keras/','best-25eps-25sim-10epch.pth.tar')
    args1 = dotdict({'numMCTSSims': 100, 'cpuct':1.0})
    mcts1 = MCTS(g, n1, args1)
    n1p = lambda x: np.argmax(mcts1.getActionProb(x, temp=0))
else:
    n1p = rp
if human_vs_cpu:
    player2 = hp
else:
    n2 = NNet(g)
    n2.load_checkpoint('./Mills/pretrained/', 'best.pth.tar')
    args2 = dotdict({'numMCTSSims': 100, 'cpuct': 1.0})
    mcts2 = MCTS(g, n2, args2)
    n2p = lambda x: np.argmax(mcts2.getActionProb(x, temp=0))

    player2 = n2p  # Player 2 is neural network if it's cpu vs cpu.

arena = Arena.Arena(n1p, player2, g, display=MillsGame.display)

print(arena.playGames(2, verbose=True))
