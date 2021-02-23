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
def get_index(coordinate):
    if coordinate == [5, 7]: return [0, 0]
    if coordinate == [5, 9]: return [0, 1]
    if coordinate == [7, 9]: return [0, 2]
    if coordinate == [9, 9]: return [0, 3]
    if coordinate == [9, 7]: return [0, 4]
    if coordinate == [9, 5]: return [0, 5]
    if coordinate == [7, 5]: return [0, 6]
    if coordinate == [5, 5]: return [0, 7]
    if coordinate == [3, 7]: return [1, 0]
    if coordinate == [3, 11]: return [1, 1]
    if coordinate == [7, 11]: return [1, 2]
    if coordinate == [11, 11]: return [1, 3]
    if coordinate == [11, 7]: return [1, 4]
    if coordinate == [11, 3]: return [1, 5]
    if coordinate == [7, 3]: return [1, 6]
    if coordinate == [3, 3]: return [1, 7]
    if coordinate == [1, 7]: return [2, 0]
    if coordinate == [1, 13]: return [2, 1]
    if coordinate == [7, 13]: return [2, 2]
    if coordinate == [13, 13]: return [2, 3]
    if coordinate == [13, 7]: return [2, 4]
    if coordinate == [13, 1]: return [2, 5]
    if coordinate == [7, 1]: return [2, 6]
    if coordinate == [1, 1]: return [2, 7]


def get_ui_position(position):
    if position == [0, 0]: return [5, 7]
    if position == [0, 1]: return [5, 9]
    if position == [0, 2]: return [7, 9]
    if position == [0, 3]: return [9, 9]
    if position == [0, 4]: return [9, 7]
    if position == [0, 5]: return [9, 5]
    if position == [0, 6]: return [7, 5]
    if position == [0, 7]: return [5, 7]
    if position == [1, 0]: return [3, 7]
    if position == [1, 1]: return [3, 11]
    if position == [1, 2]: return [7, 11]
    if position == [1, 3]: return [11, 11]
    if position == [1, 4]: return [11, 7]
    if position == [1, 5]: return [11, 3]
    if position == [1, 6]: return [7, 3]
    if position == [1, 7]: return [3, 3]
    if position == [2, 0]: return [1, 7]
    if position == [2, 1]: return [1, 13]
    if position == [2, 2]: return [7, 13]
    if position == [2, 3]: return [13, 13]
    if position == [2, 4]: return [13, 7]
    if position == [2, 5]: return [13, 1]
    if position == [2, 6]: return [7, 1]
    if position == [2, 7]: return [1, 1]


##------------Farbdefinition-----------------------------
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (127, 127, 127)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
scale: int = 100


##-------------- Darstellungserstellung ----------------
##Hintergrund
def drawbackground():
    pygame.draw.rect(screen, WHITE, (0,0, 14 * scale, 14 * scale))
    ##4 Quadrate
    Außen = list [(1 * scale, 1 * scale)(1 * scale, 13 * scale)(13 * scale, 13 * scale)(13 * scale, 1 * scale)]
    Mitte = list [(3 * scale, 3 * scale)(3 * scale, 11 * scale)(11 * scale, 11 * scale)(11 * scale, 3 * scale)]
    Innen = list [(5 * scale, 5 * scale)(5 * scale, 9 * scale)(9 * scale, 9)(9 * scale, 5 * scale)]

    pygame.draw.lines(screen, BLACK, closed=True, points=Außen, width=scale)
    pygame.draw.lines(screen, BLACK, closed=True, points=Mitte, width=scale)
    pygame.draw.lines(screen, BLACK, closed=True, points=Innen, width=scale)

    ## Verbindungen
    pygame.draw.line(screen, BLACK, start_pos=[(7 * scale, 1 * scale)], end_pos=[(7 * scale, 5 * scale)], width=scale)
    pygame.draw.line(screen, BLACK, start_pos=[(1 * scale, 7 * scale)], end_pos=[(5 * scale, 7 * scale)], width=scale)
    pygame.draw.line(screen, BLACK, start_pos=[(7 * scale, 13 * scale)], end_pos=[(7 * scale, 9 * scale)], width=scale)
    pygame.draw.line(screen, BLACK, start_pos=[(13 * scale, 7 * scale)], end_pos=[(9 * scale, 7 * scale)], width=scale)
    ##Leerstellen
    for i in range(2):
        for j in range(7):
            pygame.draw.circle(screen, GRAY, (get_ui_position(i, j), scale * 0, 25,))
    pygame.display.update()


## Soll nach jedem Zug aufgerufen werden, sofern nicht jedes Mal das Board komplett neu gezeichnet werden muss? Wenn nein, werden hier nur die Veraenderungen angezeigt
def updateboard(board, player):
    for i in range(2):
        for j in range(7):
            valid = get_legal_moves(player)
            for k in range(valid):
                if board[i, j] == valid:
                    pygame.draw.circle(screen, GREEN, (get_ui_position(i, j)), scale * 0, 25)
                    break
            if board[i, j] == 1:
                pygame.draw.circle(screen, YELLOW, (get_ui_position(i, j), scale * 0, 25))
                break
            if board[i, j] == -1:
                pygame.draw.circle(screen, BLUE, (get_ui_position(i, j), scale * 0, 25))
                break
            else:
                pygame.draw.circle(screen, GRAY, (get_ui_position(i, j), scale * 0, 25))
                break


## ------------------------- Initialisierungsvariabeln -------------------------------
width: int = 14 * scale
height: int = 14 * scale
size = [width, height]
screen = pygame.display.set_mode(size=size)
drawbackground()
myfont = pygame.font.SysFont("monospace", 75)
##--------------------------- Testinitialisierung -----------------------------------
def get_legal_moves (player):
    answer = list [2,5], [0,7], [1,3]
    return answer




## --------------Eventsteuerung, entnommen und angepasst aus Uebung 3 --------------
while board.pieces[3, 7] == 0:  ##piece [3,7] speichert Spielzustand
    if event.type == pygame.QUIT:
        sys.exit()
    if player_turn == TRUE:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                posy = event.pos[0]
                posx = event.pos[1]
                position = [int(math.floor(posy / scale)), int(math.floor(posx / scale))]
                # column = int(math.floor(posy / scale))
                # row = int(math.floor(posx / scale))
                valid = self.game.getValidMoves(board, player)
                for i in range(valid):
                    if position == valid(i):
                        execute_move(position)
                        updateboard(board)
                        pygame.display.update()
                        break

    # else:
    # einfach update aufrufen wenn der zug gemacht wird?
