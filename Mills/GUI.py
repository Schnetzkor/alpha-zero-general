import pygame
import math
import numpy as np
import sys

# 2,7 ------------- 2,0 ------------- 2,1
# |                 |                 |
# |    1,7 ------- 1,0 ------- 1,1    |
# |     |           |           |     |
# |     |    0,7 - 0,0 - 0,1    |     |
# |     |     |           |     |     |
# 2,6 - 1,6 - 0,6         0,2 - 1,2 - 2,2
# |     |     |           |     |     |
# |     |    0,5 - 0,4 - 0,3    |     |
# |     |           |           |     |
# |    1,5 ------- 1,4 ------- 1,3    |
# |                 |                 |
# 2,5 ------------- 2,4 ------------- 2,5
#
# 1,1 ------------- 1,7 ------------- 1,13
# |                 |                 |
# |    3,3 ------- 3,7 ------- 3,11   |
# |     |           |           |     |
# |     |    5,5 - 5,7 - 5,9    |     |
# |     |     |           |     |     |
# 7,1 - 7,3 - 7,5         7,9 - 7,11 - 7,13
# |     |     |           |     |     |
# |     |    9,5 - 9,7 - 9,9    |     |
# |     |           |           |     |
# |    11,3------- 11,7-------11,11   |
# |                 |                 |
# 13,1 -------------13,7-------------13,13


##------------ Umwandlungstabellen zwischen Index & Koordinate------------
scale: int = 100
line = int(scale / 10)


def setscale(value):
    scale = value


def getscale():
    return scale


coordinates = np.array([np.array([(5, 7), (5, 9), (7, 9), (9, 9), (9, 7), (9, 5), (7, 5), (5, 5)]),
                        np.array([(3, 7), (3, 11), (7, 11), (11, 11), (11, 7), (11, 3), (7, 3), (3, 3)]),
                        np.array([(1, 7), (1, 13), (7, 13), (13, 13), (13, 7), (13, 1), (7, 1), (1, 1)])])
# coordinates[0[1]] = pos1
# coordinates[0[2]] = 7, 9
# coordinates[0[3]] = 9, 9
# coordinates[0[4]] = 9, 7
# coordinates[0[5]] = 9, 5
# coordinates[0[6]] = 7, 5
# coordinates[0[7]] = 5, 5
# coordinates[1[0]] = 3, 7
# coordinates[1[1]] = 3, 11
# coordinates[1[2]] = 7, 11
# coordinates[1[3]] = 11, 11
# coordinates[1[4]] = 11, 7
# coordinates[1[5]] = 11, 3
# coordinates[1[6]] = 7, 3
# coordinates[1[7]] = 3, 3
# coordinates[2[0]] = 1, 7
# coordinates[2[1]] = 1, 13
# coordinates[2[2]] = 7, 13
# coordinates[2[3]] = 13, 13
# coordinates[2[4]] = 13, 7
# coordinates[2[5]] = 13, 1
# coordinates[2[6]] = 7, 1
# coordinates[2[7]] = 1, 1

coordinates=coordinates*scale

print(coordinates)


# def getcoordinates(board):
#    coordinates=np.copy(board)
#    coordinates = np.zeros((3, 8))
#    coordinates[0[0]] = (5, 7)
#    coordinates[0[1]] = (5, 9)
#    coordinates[0[2]] = (7, 9)
#    coordinates[0[3]] = (9, 9)
#    coordinates[0[4]] = (9, 7)
#    coordinates[0[5]] = (9, 5)
#    coordinates[0[6]] = (7, 5)
#    coordinates[0[7]] = (5, 5)
#    coordinates[1[0]] = (3, 7)
#    coordinates[1[1]] = (3, 11)
#    coordinates[1[2]] = (7, 11)
#   coordinates[1[3]] = (11, 11)
#    coordinates[1[4]] = (11, 7)
#    coordinates[1[5]] = (11, 3)
#    coordinates[1[6]] = (7, 3)
#    coordinates[1[7]] = (3, 3)
#    coordinates[2[0]] = (1, 7)
#    coordinates[2[1]] = (1, 13)
#    coordinates[2[2]] = (7, 13)
#    coordinates[2[3]] = (13, 13)
#    coordinates[2[4]] = (13, 7)
#    coordinates[2[5]] = (13, 1)
#    coordinates[2[6]] = (7, 1)
#    coordinates[2[7]] = (1, 1)


def get_index(gui_position):
    gui_position = gui_position / scale
    indexfound = np.where(coordinates == gui_position)
    return indexfound


def get_gui_position(index_position):
    ui_position = coordinates[index_position[0], index_position[1]]
    ui_position * scale
    return ui_position


##------------Farbdefinition-----------------------------
BLACK, GREEN, BLUE, GRAY, YELLOW, WHITE = (0, 0, 0), (0, 255, 0), (0, 0, 255), (127, 127, 127), (255, 255, 0), (
    255, 255, 255)

# BLACK=(0, 0, 0)
# GREEN = (0, 255, 0)
# BLUE = (0, 0, 255)
# GRAY = (127, 127, 127)
# YELLOW = (255, 255, 0)
# WHITE = (255, 255, 255)




##-------------- Darstellungserstellung ----------------
##Hintergrund
def drawbackground():
    pygame.draw.rect(screen, WHITE, (0, 0, 14 * scale, 14 * scale))  # Hintergrund


def drawlines():
    for i in range(3):
        for j in range(8):
            start, finish = coordinates[i][j], coordinates[i][((j+1) % 8)]
            pygame.draw.line(screen, BLACK, start, finish, line)
            if j % 2 == 0 and i == 0:
                start, finish = coordinates[i][j], coordinates[(i + 2)][j]
                pygame.draw.line(screen, BLACK, start, finish, line)
    pygame.display.update()


## Soll nach jedem Zug aufgerufen werden, sofern nicht jedes Mal das Board komplett neu gezeichnet werden muss? Wenn nein, werden hier nur die Veraenderungen angezeigt
def updateboard(board, player):
    for i in (range(board)):  # -1 am Ende, Extravariabeln!
        for j in range(board[i]):
            valid = get_legal_moves(player)
            if board[i, j] == valid:
                pygame.draw.circle(surface=screen, color=GREEN, center=(get_gui_position(i, j)), radius=(scale / 2))
                pygame.display.update()
                break
            if board[i, j] == 1:
                pygame.draw.circle(surface=screen, color=YELLOW, center=(get_gui_position(i, j)), radius=(scale / 2))
                pygame.display.update()
                break
            if board[i, j] == -1:
                pygame.draw.circle(surface=screen, color=BLUE, center=(get_gui_position(i, j)), radius=(scale / 2))
                pygame.display.update()
                break
            else:
                pygame.draw.circle(surface=screen, color=GRAY, center=(get_gui_position(i, j)), radius=(scale / 2))
                pygame.display.update()
                break


## ------------------------- Initialisierungsvariabeln -------------------------------
width: int = 14 * scale
height: int = 14 * scale
size = [width, height]
screen = pygame.display.set_mode(size=size)
pygame.init()
drawbackground()
drawlines()
pygame.display.update()
pygame.time.wait(30000)
##--------------------------- Testinitialisierung -----------------------------------
# def get_legal_moves(player):
#    answer = list[2, 5], [0, 7], [1, 3]
#    return answer


## --------------Eventsteuerung, entnommen und angepasst aus Uebung 3 --------------
# while board.pieces[3, 7] == 0:  ##piece [3,7] speichert Spielzustand
#   if event.type == pygame.QUIT:
#        sys.exit()
#    if player_turn == TRUE:
#        for event in pygame.event.get():
#            if event.type == pygame.MOUSEBUTTONDOWN:
#                posy = event.pos[0]
#                posx = event.pos[1]
#                position = [int(math.floor(posy / scale)), int(math.floor(posx / scale))]
#                # column = int(math.floor(posy / scale))
#                # row = int(math.floor(posx / scale))
#                valid = self.game.getValidMoves(board, player)
#                for i in range(valid):
#                    if position == valid(i):
#                        execute_move(position)
#                        updateboard(board)
#                        pygame.display.update()
#                       break

# else:
# einfach update aufrufen wenn der zug gemacht wird?
