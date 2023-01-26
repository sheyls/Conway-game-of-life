import random
import pygame
import numpy as np
from sklearn import neighbors
import time



RED_P = [(205, 92, 92),(240, 128, 128), (250, 128, 114), (233, 150, 122),(233, 150, 122),(233, 150, 122), (255, 0, 0),(178, 34, 34),(139, 0, 0)]
PINK_P = [(139, 0, 0), (255, 182, 193),(255, 105, 180), (255, 20, 147),(199, 21, 133), (219, 112, 147)]
ORANGE_P = [(255, 160, 122), (255, 127, 80), (255, 99, 71), (255, 69, 0), (255, 140, 0), (255, 165, 0)]
GREEN_P = [(173, 255, 47), (127, 255, 0), (124, 252, 0), (0, 255, 0), (50, 205, 50), (152, 251, 152), (144, 238, 144),(0, 250, 154), (0, 255, 127), (60, 179, 113)]
BLUE_P = [(32, 178, 170), (0, 139, 139), (0, 139, 139),(0, 206, 209), (0, 191, 255), (127, 255, 212)]
GRAY_P = [(220, 220, 220),(169, 169, 169),(128, 128, 128), (119, 136, 153), (0, 0, 0)]

def pick_color(bg_color):
    """ 
    Create a color with the rgb agreement 
    """
    palette = BLUE_P
    color = bg_color
    index = random.randint(0, len(palette)-1)
    while color == bg_color:
        color = palette[index]
    return color


pygame.init()

bg_color = (255, 255, 255)

width, height = 1000, 1000
screen = pygame.display.set_mode((height, width))

screen.fill(bg_color)

cell_countX, cell_countY = 50, 50

cell_dimW = width / cell_countX
cell_dimH = height / cell_countY

game_state = np.zeros((cell_countX, cell_countY))

game_state[21, 21] = 1
game_state[22, 22] = 1
game_state[22, 23] = 1
game_state[21, 23] = 1
game_state[20, 23] = 1

pause = False

while True:

    new_game_state = np.copy(game_state)

    screen.fill(bg_color)
    time.sleep(0.2)

    #Mouse events
    ev = pygame.event.get()
    for event in ev:
        if event.type == pygame.KEYDOWN:
            pause = not pause

        mouse_click = pygame.mouse.get_pressed()

        if sum(mouse_click) > 0:
            posX, posY = pygame.mouse.get_pos()
            cellX, cellY = int(np.floor(posX / cell_dimW)), int(np.floor(posY / cell_dimH))
            new_game_state[cellX, cellY] = not mouse_click[2]
            
    

    for y in range(0,cell_countX):
        for x in range(0, cell_countY):
            
            if not pause:

                neighbors = game_state[(x-1) % cell_countX, (y-1) % cell_countY] + \
                            game_state[(x) % cell_countX, (y-1) % cell_countY] + \
                            game_state[(x+1) % cell_countX, (y-1) % cell_countY] + \
                            game_state[(x-1) % cell_countX, (y) % cell_countY] + \
                            game_state[(x+1) % cell_countX, (y) % cell_countY] + \
                            game_state[(x-1) % cell_countX, (y+1) % cell_countY] + \
                            game_state[(x) % cell_countX, (y+1) % cell_countY] + \
                            game_state[(x+1) % cell_countX, (y+1) % cell_countY]
                
                if game_state[x,y] == 0 and neighbors == 3:
                    new_game_state[x,y] = 1

                elif game_state[x,y] == 1 and (neighbors < 2 or neighbors > 3):
                    new_game_state[x,y] = 0

            pol = [((x) * cell_dimW, y * cell_dimH),
                    ((x+1) * cell_dimW, y * cell_dimH),
                    ((x+1) * cell_dimW, (y+1) * cell_dimH),
                    ((x) * cell_dimW, (y+1) * cell_dimH ) ]

            #Drawing
            if new_game_state[x,y] == 0:
                pygame.draw.polygon(screen, (220, 220, 220), pol, width=1)
            else:
                pygame.draw.polygon(screen, pick_color(bg_color), pol, width=0)
        
    game_state = np.copy(new_game_state)
    pygame.display.flip() 