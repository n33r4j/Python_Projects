
import os, pathlib
import pygame
from Graph import Graph
from Colors import *


WIDTH, HEIGHT = 800, 800
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Graph Visualizer")

FPS_MAX = 60
SIM_RUN = True
SIM_PAUSED = False

PREFIX = pathlib.Path(__file__).parent.resolve()

def draw(graph):
    window.fill(BLACK)

    graph.Draw(window)

    pygame.display.update()


def main():
    pygame.init()
    global SIM_RUN
    
    clock = pygame.time.Clock()

    graph_1_filename = os.path.join(PREFIX, "graph_1.txt")
    g1 = Graph(graph_1_filename)
    # print(g1.edges)

    while SIM_RUN:
        clock.tick(FPS_MAX)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                SIM_RUN = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

        draw(g1)


    pygame.quit()
    print("Simulation Terminated...")


if __name__ == "__main__":
    
    main()

