import numpy as np
import pygame as pg
from pygame.locals import *
import sys
BG = (25, 25, 25)
CellBorder = (128, 128, 128)
LifeCell = (255, 0, 0)

ticks = 60

ancho = 800
alto = 800

nombre = '==> Life Game <=='

nxC = 50
nyC = 50
dimCW = ancho / nxC
dimCH = alto / nyC


pg.init()

gameState = np.zeros((nxC, nyC))

gameState[3,3] = 1
gameState[3,4] = 1
gameState[3,5] = 1
gameState[3,6] = 1
gameState[3,7] = 1

screen = pg.display.set_mode((ancho, alto))
pg.display.set_caption(nombre)

actions = {
    'escape': True,
}

clock = pg.time.Clock()
clock.tick(1)


def events():
    for event in pg.event.get():

        if event.type == 'QUIT':
            return True

        if event.type == KEYDOWN:
            key = pg.key.name(event.key)
            return actions.get(key)
        
        mouseClick = pg.mouse.get_pressed()
        if sum(mouseClick) > 0:
            posX, posY = pg.mouse.get_pos()
            celX, celY = int(np.floor(posX / dimCW)), int(np.floor(posY / dimCH))
            print(f'Clicked:\tposX = {celX}\tposY = {celY}')
            gameState[celX, celY] = 1

    return False

done = False

while not done:
    screen.fill(BG)
    state = np.copy(gameState)
    done = events()

    for y in range(0, nxC):
        for x in range(0, nyC):

            # Calculate the number of closes neighboards
            n_neigh = state[(x - 1) % nxC, (y - 1) % nyC] + \
                state[(x) % nxC, (y - 1) % nyC] + \
                state[(x + 1) % nxC, (y - 1) % nyC] + \
                state[(x - 1) % nxC, (y) % nyC] + \
                state[(x + 1) % nxC, (y) % nyC] + \
                state[(x - 1) % nxC, (y + 1) % nyC] + \
                state[(x) % nxC, (y + 1) % nyC] + \
                state[(x + 1) % nxC, (y + 1) % nyC]

            # Rule #1
            if state[x, y] == 0 and n_neigh == 3:
                state[x, y] = 1

            elif state[x, y] == 1 and (n_neigh < 2 or n_neigh > 3):
                state[x, y] = 0

            # Creating the polygon of each cell to draw
            poly = [((x) * dimCW, y * dimCH),
                    ((x + 1) * dimCW, y * dimCH),
                    ((x + 1) * dimCW, (y + 1) * dimCH),
                    ((x) * dimCW, (y + 1) * dimCH)]

            # Draw the cell for each pair of x and y
            if state[x, y] == 0:
                pg.draw.polygon(screen, (CellBorder), poly, 1)
            else:
                pg.draw.polygon(screen, (LifeCell), poly, 0)

    gameState = state
    # Update on the screen
    pg.display.flip()

pg.quit()
sys.exit()
