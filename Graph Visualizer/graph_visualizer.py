# Graph Visualizer

import pygame
from Node import Node

WIDTH, HEIGHT = 600, 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Graph Visualizer")

FPS_MAX = 60
SIM_RUN = True
SIM_PAUSED = False


# Color definitions
WHITE = (255,255,255)
BLACK = (0, 0, 0)
YELLOW = (255,255,5)
D_BLUE = (5, 5, 80)
BLUE = (5,5,255)
GREEN = (5,200,5)
RED = (200,5,5)

def draw_window(nodes):
    window.fill(BLACK)
    
    for node in nodes:
        node.Draw(window)
    
    pygame.display.update()


def main():
    pygame.init()
    clock = pygame.time.Clock()
    global SIM_RUN
    
    graph_nodes = []
    
    for i in range(1):
        graph_nodes.append(Node((300,300), 20, i, RED))
    
    print("Starting Simulation...")
    
    while SIM_RUN:
        clock.tick(FPS_MAX)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                SIM_RUN = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                graph_nodes[0].setPosition(mouse_pos)
            
        if not SIM_PAUSED:
            currTime = pygame.time.get_ticks()
            
            draw_window(graph_nodes)
    
    pygame.quit()
    print("Simulation Terminated...")
    
    

if __name__ == "__main__":
    main()