import pygame
import numpy as np
'''GUI for the Game of Mills. 
Gets the Mapping of the field as an array.
Has a fixed conversion Array as an 2D Space on which the board is to be represented, which can be scaled as needed.
Scans the GUI for mouseclicks, and transforms them via indexation of the unscaled Array back into
the coordinates of the board which can be returned to commit the move of the player. 
Graphical Representation of both Arrays (scaled Array has same Architecture, but differing dimensions.
Ignores the additional layer of the board-Array for meta-data about the game such as stages, counters and past moves.

Author: Philipp Petermeier, https://github.com/PPetermeier
Date: 28.02.2021

Based on the implementation of mills with alphazero from Simon Schnecko.

 2,7 ------------- 2,0 ------------- 2,1
 |                 |                 |
 |    1,7 ------- 1,0 ------- 1,1    |
 |     |           |           |     |
 |     |    0,7 - 0,0 - 0,1    |     |
 |     |     |           |     |     |
 2,6 - 1,6 - 0,6         0,2 - 1,2 - 2,2
 |     |     |           |     |     |
 |     |    0,5 - 0,4 - 0,3    |     |
 |     |           |           |     |
 |    1,5 ------- 1,4 ------- 1,3    |
 |                 |                 |
 2,5 ------------- 2,4 ------------- 2,3

 1,1 ------------- 1,7 ------------- 1,13
 |                 |                 |
 |    3,3 ------- 3,7 ------- 3,11   |
 |     |           |           |     |
 |     |    5,5 - 5,7 - 5,9    |     |
 |     |     |           |     |     |
 7,1 - 7,3 - 7,5         7,9 - 7,11 - 7,13
 |     |     |           |     |     |
 |     |    9,5 - 9,7 - 9,9    |     |
 |     |           |           |     |
 |    11,3------- 11,7-------11,11   |
 |                 |                 |
 13,1 -------------13,7-------------13,13

'''
##------------ Umwandlungstabellen zwischen Index & Koordinate------------
scale: int = 100
line = int(scale / 10)


def setscale(value):
    scale = value


def getscale():
    return scale


def testboard():
    testboard = np.zeros((3, 8))
    return testboard

# ---------------Überlegungen, wie eine Schnittstellentabelle automatisiert erstellt werden kann ----------
# def write_coordinates(board):
#    coordinates = np.copy(board)
#    dimension = 1
#    for i in range(len(coordinates)):
#        dimension + 4
#    vdistance = 2, 0
#    hdistance = 0, 2
#    cdistance = 2, 0
#    anchor1 = (dimension / 2) - 2
#    anchor2 = dimension / 2
#    anchor =np.array([anchor1, anchor2])
#    anchor[0] = int(dimension / 2) - 2), int(dimension / 2)
#    counter = anchor
#    for i in range(len(coordinates)):
#        for j in range(len(coordinates[i])):
#            if i == 0 and j == 0:
#                coordinates[i[j]] = int(anchor1), int(anchor2)
#                break
#            if i > 0 == True and j == 0:
#                counter = anchor - int(i * cdistance)
#                coordinates[i[j]] = counter
#            if j == 1:
#                counter = counter + hdistance
#                coordinates[i[j]] = counter
#                break
#            if j < 4 == True:
#                counter = counter + vdistance
#                coordinates[i[j]] = counter
#                break
#            if j < 6 == True:
#                counter = counter - hdistance
#                coordinates[i[j]] = counter
#                break
#            else:
#                counter = counter - vdistance
#        vdistance[0] + 1, hdistance[1] + 1
#    return coordinates

##--------------------------Fixe Schnittstelle zwischen board und GUI ----------------------
coordinates = np.array([[(5, 7), (5, 9), (7, 9), (9, 9), (9, 7), (9, 5), (7, 5), (5, 5)],
                       [(3, 7), (3, 11), (7, 11), (11, 11), (11, 7), (11, 3), (7, 3), (3, 3)],
                        [(1, 7), (1, 13), (7, 13), (13, 13), (13, 7), (13, 1), (7, 1), (1, 1)]])

coordinates = np.roll(np.fliplr(coordinates), 7 , 1)

scaled_coordinates = coordinates * scale

def get_index(gui_position1, gui_position2):     ## Das selbsterstellte Board hat vermute ich die Reihen und Spalten vertauscht. Sollte es zu Problemen kommen, einfach im loop rows & cols miteinander vertauschen!
    gui_position1 = int(round(gui_position1/scale))
    gui_position2 = int(round(gui_position2/scale))
    search = (gui_position1, gui_position2)
    rows = coordinates.shape[0]
    cols = coordinates.shape[1]
    failure = False
    print(search)
    for i in range(rows):
        for j in range(cols):
            if np.all(coordinates[i, j] == search):
                return i, j
    return failure

def get_gui_position(index_position1, index_position2):
    gui_position = scaled_coordinates[index_position1, index_position2]
    return gui_position


##------------Farbdefinition-----------------------------
BLACK, GREEN, BLUE, GRAY, YELLOW, WHITE = (0, 0, 0), (0, 255, 0), (0, 0, 255), (127, 127, 127), (255, 255, 0), (
    255, 255, 255)
##-------------- Darstellungserstellung ----------------
def drawbackground():
    pygame.draw.rect(screen, WHITE, (0, 0, 14 * scale, 14 * scale))  # Hintergrund

def drawlines():
    for i in range(3):
        for j in range(8):
            start, finish = scaled_coordinates[i][j], scaled_coordinates[i][((j + 1) % 8)]
            pygame.draw.line(screen, BLACK, start, finish, line)
            if j % 2 == 0 and i == 0:
                start, finish = scaled_coordinates[i][j], scaled_coordinates[(i + 2)][j]
                pygame.draw.line(screen, BLACK, start, finish, line)
    pygame.display.update()

## Soll nach jedem Zug aufgerufen werden, sofern nicht jedes Mal das Board komplett neu gezeichnet werden muss? Wenn nein, werden hier nur die Veraenderungen angezeigt
def updateboard(board):
    for i in range(3):
        for j in range(8):
            # valid = get_legal_moves(player) Hier fehlt die Einbindung von legal_moves
            # if board[i, j] == valid:
            #    pygame.draw.circle(surface=screen, color=GREEN, center=(get_gui_position(i, j)), radius=(scale / 2))
            #    pygame.display.update()
            if board[i, j] == 1:
                pygame.draw.circle(surface=screen, color=YELLOW, center=(get_gui_position(i, j)), radius=(scale / 2))
                pygame.display.update()
            if board[i, j] == -1:
                pygame.draw.circle(surface=screen, color=BLUE, center=(get_gui_position(i, j)), radius=(scale / 2))
                pygame.display.update()
            if board[i, j] == 0:
                pygame.draw.circle(surface=screen, color=GRAY, center=(get_gui_position(i, j)), radius=(scale / 2))
                pygame.display.update()


## ------------------------- Initialisierungsvariabeln -------------------------------
board = testboard()
width: int = 14 * scale
height: int = 14 * scale
size = (width, height)
pygame.init()
screen = pygame.display.set_mode(size)
myfont = pygame.font.SysFont("monospace", 75)
# board = write_coordinates(board)
drawbackground()
drawlines()
updateboard(board)
pygame.display.update()
pygame.time.wait(30000)

## --------------Eventsteuerung, entnommen und angepasst aus Uebung 3 --------------
# while board.pieces[3, 7] == 0:  ##piece [3,7]: speichert Spielzustand
player_turn = True
player = 1

def set_piece(board, player, col, row):
    place = get_index(col, row)
    if place != False:
        board[place] = player
    else:
        Message = 'Du hast eine ungültige Stelle angeklickt, versuch es nochmal auf einem leeren Feld'
        print(Message)

def scanning():
    while player_turn:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                posx = event.pos[0]
                posy = event.pos[1]
                col = int(round(posx))
                row = int(round(posy))
                set_piece(board, player, col, row)
                updateboard(board)

            #position = [int(math.floor(posy / scale)), int(math.floor(posx / scale))]

            # column = int(math.floor(posy / scale))
            # row = int(math.floor(posx / scale))
            # valid = self.game.getValidMoves(board, player)
            # for i in range(valid):
            #    if position == valid(i):
            #        execute_move(position)
            #        updateboard(board)
            #        pygame.display.update()
            #        break
        pygame.display.update()

scanning()