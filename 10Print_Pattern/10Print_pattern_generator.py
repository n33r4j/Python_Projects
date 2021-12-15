# 10Print Pattern Generator

import pygame
import random
import os, pathlib

WIDTH, HEIGHT = 800, 450
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("10Print Pattern Generation")

BORDER = pygame.Rect(WIDTH/2 - 5, 0, 10, HEIGHT)
FPS_MAX = 60

SIM_RUN = True

# Color definitions
WHITE = (255,255,255)
BLACK = (0, 0, 0)
YELLOW = (255,255,5)
D_BLUE = (5, 5, 80)
BLUE = (5,5,255)
GREEN = (5,200,5)
L_GREEN = (126,222,9)
GREY = (52,54,50)
D_GREY = (37,38,36)
RED = (200,5,5)


PREFIX = pathlib.Path(__file__).parent.resolve()

# Does not work on Windows console by default.
def drawPatternInConsole(width, height):
    for i in range(height):
        for j in range(width):
            print("\u27cd " if random.randint(0,1) else "\u27cb ", end="")
        print()


def drawPattern(size, color, thickness, bg_color):
    WIN.fill(bg_color)
    
    width, height = WIDTH//size, HEIGHT//size
    
    for i in range(height):
        for j in range(width):
            if random.randint(0,1):
                start = (j*size, i*size)
                end = ((j+1)*size, (i+1)*size)
            else:
                start = (j*size, (i+1)*size)
                end = ((j+1)*size, i*size)
                
            # pygame.draw.aaline(WIN, color, start, end, thickness)
            pygame.draw.line(WIN, color, start, end, thickness)
            pygame.display.update()
            
    


def main():
    pygame.init()
    
    global SIM_RUN
    
    PatternCreated = False
    
    clock = pygame.time.Clock()
    
    while SIM_RUN:
        clock.tick(FPS_MAX)
        
        if not PatternCreated:
            drawPattern(10, BLACK, thickness=8, bg_color=RED)
            PatternCreated = True
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                SIM_RUN = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    filename = input("Type \"c\" to go back \n or Save file as(filename + .png/.jpg): ")
                    if filename.lower() != "c":
                        path = os.path.join(PREFIX, filename)
                        # print(path)
                        pygame.image.save(WIN, path)
                        print("Image Saved")
                    else:
                        print("Saving cancelled...")
    
    pygame.quit()
    print("Simulation Terminated...")
    
    
if __name__ == "__main__":
    main()