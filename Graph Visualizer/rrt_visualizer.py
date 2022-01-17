# RRT Visualizer


import os, pathlib
import pygame
import random
import math
from Graph import Graph
from Colors import *


WIDTH, HEIGHT = 800, 800
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("RRT Visualizer")

FPS_MAX = 100
SIM_RUN = True
SIM_PAUSED = False

start_pos = [20, 20]
goal_pos = [450, 760]
curr_pos = start_pos

map = [[0 for i in range(WIDTH)] for j in range(HEIGHT)]

PREFIX = pathlib.Path(__file__).parent.resolve()

def draw(graph):
    window.fill(BLACK)

    graph.Draw(window)

    pygame.display.update()

def EuclidDist(start, goal):
    return ((start[0]-goal[0])**2+(start[1]-goal[1])**2)**0.5

def RRT(step):
    global curr_pos
    # While a step in random direction is a wall,
    #   Get new random direction

    while True:
        angle = random.random()*2*math.pi
        new_X = round(curr_pos[0] + (math.cos(angle)*step))
        new_Y = round(curr_pos[1] + (math.sin(angle)*step))
        if new_X >= WIDTH or new_X < 0 or new_Y >= HEIGHT or new_Y < 0:
            continue
        new_pos = [new_X, new_Y]
        if map[new_pos[0]][new_pos[1]] == 0:
            map[new_pos[0]][new_pos[1]] == 1
            break

    
    # window.fill(BLACK)
    pygame.draw.aaline(window, GREEN, curr_pos, new_pos)
    pygame.draw.circle(window, RED, new_pos, 2.0)
    pygame.display.update()

    curr_pos = new_pos
    # Join previous node to current node
    # Draw node in current position

def main():
    pygame.init()
    global SIM_RUN
    global SIM_PAUSED
    
    clock = pygame.time.Clock()

    while SIM_RUN:
        clock.tick(FPS_MAX)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                SIM_RUN = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    SIM_PAUSED = not SIM_PAUSED
        
        if not SIM_PAUSED:
            RRT(20)


    pygame.quit()
    print("Simulation Terminated...")


if __name__ == "__main__":
    main()

