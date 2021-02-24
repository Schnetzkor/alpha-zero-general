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
def get_index(x, y):
    if [x, y] == [5, 7]: return [0, 0]
    if [x, y] == [5, 9]: return [0, 1]
    if [x, y] == [7, 9]: return [0, 2]
    if [x, y] == [9, 9]: return [0, 3]
    if [x, y] == [9, 7]: return [0, 4]
    if [x, y] == [9, 5]: return [0, 5]
    if [x, y] == [7, 5]: return [0, 6]
    if [x, y] == [5, 5]: return [0, 7]
    if [x, y] == [3, 7]: return [1, 0]
    if [x, y] == [3, 11]: return [1, 1]
    if [x, y] == [7, 11]: return [1, 2]
    if [x, y] == [11, 11]: return [1, 3]
    if [x, y] == [11, 7]: return [1, 4]
    if [x, y] == [11, 3]: return [1, 5]
    if [x, y] == [7, 3]: return [1, 6]
    if [x, y] == [3, 3]: return [1, 7]
    if [x, y] == [1, 7]: return [2, 0]
    if [x, y] == [1, 13]: return [2, 1]
    if [x, y] == [7, 13]: return [2, 2]
    if [x, y] == [13, 13]: return [2, 3]
    if [x, y] == [13, 7]: return [2, 4]
    if [x, y] == [13, 1]: return [2, 5]
    if [x, y] == [7, 1]: return [2, 6]
    if [x, y] == [1, 1]: return [2, 7]


def get_ui_position(x, y):

    if [x, y] == [0, 0]: return [50, 70]
    if [x, y] == [0, 1]: return [50, 90]
    if [x, y] == [0, 2]: return [70, 90]
    if [x, y] == [0, 3]: return [90, 90]
    if [x, y] == [0, 4]: return [90, 70]
    if [x, y] == [0, 5]: return [90, 50]
    if [x, y] == [0, 6]: return [70, 50]
    if [x, y] == [0, 7]: return [50, 70]
    if [x, y] == [1, 0]: return [30, 70]
    if [x, y] == [1, 1]: return [30, 110]
    if [x, y] == [1, 2]: return [70, 110]
    if [x, y] == [1, 3]: return [110, 110]
    if [x, y] == [1, 4]: return [110, 70]
    if [x, y] == [1, 5]: return [110, 30]
    if [x, y] == [1, 6]: return [70, 30]
    if [x, y] == [1, 7]: return [30, 30]
    if [x, y] == [2, 0]: return [10, 70]
    if [x, y] == [2, 1]: return [10, 130]
    if [x, y] == [2, 2]: return [70, 130]
    if [x, y] == [2, 3]: return [130, 130]
    if [x, y] == [2, 4]: return [130, 70]
    if [x, y] == [2, 5]: return [130, 10]
    if [x, y] == [2, 6]: return [70, 10]
    if [x, y] == [2, 7]: return [10, 10]


##------------Farbdefinition-----------------------------
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (127, 127, 127)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
scale: int = 10
linien: int = scale/10
pygame.init()











##-------------- Darstellungserstellung ----------------
##Hintergrund
<<<<<<< HEAD

def drawBackground():
    pygame.draw.rect (screen, WHITE, 0, 14 * scale)
##4 Quadrate
    pygame.draw.lines (screen, BLACK, closed=True  ,points=((scale * [1,1]), (scale * [1,13]), (scale * [13,13]), (scale*[13,1])), width = scale)
    pygame.draw.lines (screen, BLACK, closed=True, points=((scale * [3,3]), (scale * [3,11]), (scale * [11,11]), (scale*[11,3])), width = scale)
    pygame.draw.lines (screen, BLACK, closed=True, points=((scale * [5,5] ),(scale * [5,9]), (scale * [9,9]), (scale*[9,5])), width = scale)
## Verbindungen
    pygame.draw.line (screen, BLACK, start_pos=(scale * [7,1]), end_pos = (scale * [7,5]) , width=scale)
    pygame.draw.line (screen, BLACK, start_pos=(scale * [1,7]), end_pos =(scale * [5,7]) , width=scale)
    pygame.draw.line (screen, BLACK, start_pos=(scale * [7,13]), end_pos =(scale * [7,9]) , width=scale)
    pygame.draw.line (screen, BLACK, start_pos=(scale * [13,7]), end_pos=(scale * [9,7]) , width=scale)
##Leerstellen
=======
def drawbackground():
    pygame.draw.rect(screen, WHITE, (0, 0, 14 * scale, 14 * scale))
    ##4 Quadrate(scale*1, scale*1) (scale*1, scale*13)(scale*13, scale*13)(scale*13, scale*1)
    ##Außen: list =(1 * scale, 1 * scale),(1 * scale, 13 * scale),(13 * scale, 13 * scale),(13 * scale, 1 * scale)
    ##Mitte = list (3 * scale, 3 * scale),(3 * scale, 11 * scale),(11 * scale, 11 * scale),(11 * scale, 3 * scale)
    ##Innen = list (5 * scale, 5 * scale),(5 * scale, 9 * scale),(9 * scale, 9),(9 * scale, 5 * scale)

    #pygame.draw.lines(surface=screen, color=BLACK, closed=True, points=Außen, width=linien)
    #pygame.draw.lines(surface=screen, color=BLACK, closed=True, points=list[(3*scale, 3*scale), (3*scale, 11*scale), (11*scale, 11*scale), (11*scale, 3*scale)], width=linien)
    #pygame.draw.lines(surface=screen, color=BLACK, closed=True, points=list[(5*scale, 5*scale), (5*scale, 9*scale), (9*scale, 9*scale), (9*scale, 5*scale)], width=linien)
    ## pygame.draw.line(surface=screen, color=BLACK, start_pos=(int(scale * 1), int(scale * 1)),end_pos=((int(scale * 13), int(scale * 1)), width(linien)))
    pygame.draw.line (screen,BLACK, (10,10), (130, 10), 10)
    pygame.draw.line(screen, BLACK, (130, 10), (130, 130), 10)
    pygame.draw.line(screen, BLACK, (130, 130), (10, 130), 10)
    pygame.draw.line(screen, BLACK, (10,  130), (10, 10), 10)

    pygame.draw.line(screen, BLACK, (30, 30), (30, 110), 10)
    pygame.draw.line(screen, BLACK, (30, 110), (110, 110), 10)
    pygame.draw.line(screen, BLACK, (110,  110), (110, 30), 10)
    pygame.draw.line(screen, BLACK, (110, 30), (30, 30), 10)
    # pygame.draw.line(surface=screen, color=BLACK, start_pos=(scale*3, scale*3), end_pos=(scale*3, scale*11), width=linien)
    # pygame.draw.line(surface=screen, color=BLACK, start_pos=(scale*3, scale*11), end_pos=(scale*11, scale*11), width=linien)
    # pygame.draw.line(surface=screen, color=BLACK, start_pos=(scale*11, scale*11), end_pos=(scale*11, scale*3), width=linien)
    # pygame.draw.line(surface=screen, color=BLACK, start_pos=(scale*11, scale*3), end_pos=(scale*3, scale*3), width=linien)
    pygame.draw.line(screen, BLACK, (50, 50), (50, 90), 10)
    pygame.draw.line(screen, BLACK, (50, 90), (90, 90), 10)
    pygame.draw.line(screen, BLACK, (90,  90), (90, 50), 10)
    pygame.draw.line(screen, BLACK, (90, 50), (50, 50), 10)
    #pygame.draw.line(surface=screen, color=BLACK, start_pos=(scale*5, scale*5), end_pos=(scale*5, scale*9), width=linien)
   # pygame.draw.line(surface=screen, color=BLACK, start_pos=(scale*5, scale*9), end_pos=(scale*9, scale*9), width=linien)
   # pygame.draw.line(surface=screen, color=BLACK, start_pos=(scale*9, scale*9), end_pos=(scale*9, scale*5), width=linien)
   # pygame.draw.line(surface=screen, color=BLACK, start_pos=(scale*9, scale*5), end_pos=(scale*5, scale*5), width=linien)
    ## Verbindungen
    pygame.draw.line(screen, BLACK, (70, 10), (70, 50), 10)
    pygame.draw.line(screen, BLACK, (10, 70), (50, 70), 10)
    pygame.draw.line(screen, BLACK, (70, 130), (70, 90), 10)
    pygame.draw.line(screen, BLACK, (130, 70), (90, 70), 10)
   # pygame.draw.line(surface=screen, color=BLACK, start_pos=(scale*7, scale*1), end_pos=(scale*7, scale*5), width=linien)
   # pygame.draw.line(surface=screen, color=BLACK, start_pos=(scale*1, scale*7), end_pos=(scale*5, scale*7), width=linien)
   # pygame.draw.line(surface=screen, color=BLACK, start_pos=(scale*7, scale*13), end_pos=(scale*7, scale*9), width=linien)
    #pygame.draw.line(surface=screen, color=BLACK, start_pos=(scale*13, scale*7), end_pos=(scale*9, scale*7), width=linien)
    ##Leerstellen
>>>>>>> 859326362b7079e68d3993c45d62d495e4f2aac6
    for i in range(2):
        for j in range(7):
            pygame.draw.circle(surface=screen, color=GRAY, center=get_ui_position(i, j), radius=(scale/2))
    pygame.display.update()


## Soll nach jedem Zug aufgerufen werden, sofern nicht jedes Mal das Board komplett neu gezeichnet werden muss? Wenn nein, werden hier nur die Veraenderungen angezeigt
def updateboard(board, player):
    for i in range(2):
        for j in range(7):
            valid = get_legal_moves(player)
            for k in range(valid):
                if board[i, j] == valid:
                    pygame.draw.circle(surface=screen, color=GREEN, center=(get_ui_position(i, j)), radius=(scale/2))
                    break
            if board[i, j] == 1:
                pygame.draw.circle(surface=screen, color=YELLOW, center=(get_ui_position(i, j)), radius=(scale/2))
                break
            if board[i, j] == -1:
                pygame.draw.circle(surface=screen, color=BLUE, center=(get_ui_position(i, j)),radius=(scale/2))
                break
            else:
                pygame.draw.circle(surface=screen, color=GRAY, center=(get_ui_position(i, j)), radius=(scale/2))
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
