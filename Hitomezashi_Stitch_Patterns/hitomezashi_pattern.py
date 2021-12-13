# Hitomezashi Stitch Patterns
# [https://youtu.be/JbfhzlMk2eY]

import pygame
import random

WIDTH, HEIGHT = 640, 640
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Hitmezashi Stitch Patterns")

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
RED = (200,5,5)

offsetX = 20
offsetY = 20


def getRandomBinaryNum(size):
    num = ""
    for i in range(size):
        num += ('1' if random.randint(0,1)==1 else '0')
        
    return num
    # return bin(random.randint(0,50000))[2:(2+size)]


def createDotGrid(width, height, cell_size):
    for i in range(height):
        for j in range(width):
            pygame.draw.circle(WIN, RED, (offsetX + (j*cell_size),offsetY + (i*cell_size)), 2.0)


def createPattern(num1, num2, color=BLUE, showGrid=False):
    WIN.fill(BLACK)
    height = 50
    width = 50
    cell_size = 12
    
    if showGrid:
        createDotGrid(width, height, cell_size)
    
    for i, char in enumerate(num1):
        if int(char):
            for j in range(0, width-1, 2):
                start = (offsetX + (j*cell_size), offsetY + (i*cell_size))
                end = (offsetX + ((j+1)*cell_size), offsetY + (i*cell_size))
                pygame.draw.aaline(WIN, color, start, end, 4)
        else:
            for j in range(1, width-1, 2):
                start = (offsetX + (j*cell_size), offsetY + (i*cell_size))
                end = (offsetX + ((j+1)*cell_size), offsetY + (i*cell_size))
                pygame.draw.aaline(WIN, color, start, end, 4)
    
    for i, char in enumerate(num2):
        if int(char):
            for j in range(0, height-1, 2):
                start = (offsetX + (i*cell_size), offsetY + (j*cell_size))
                end = (offsetX + (i*cell_size), offsetY + ((j+1)*cell_size))
                pygame.draw.aaline(WIN, color, start, end, 4)
        else:
            for j in range(1, height-1, 2):
                start = (offsetX + (i*cell_size), offsetY + (j*cell_size))
                end = (offsetX + (i*cell_size), offsetY + ((j+1)*cell_size))
                pygame.draw.aaline(WIN, color, start, end, 4)
    
    pygame.display.update()
    
    
def main():
    pygame.init()
    
    global SIM_RUN
    num1 = getRandomBinaryNum(50)
    num2 = getRandomBinaryNum(50)
    
    print(f'num1: {num1}')
    print(f'num2: {num2}')
    
    clock = pygame.time.Clock()
    
    while SIM_RUN:
        clock.tick(FPS_MAX)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                SIM_RUN = False
                
        createPattern(num1, num2, GREEN)
    
    pygame.quit()
    print("Simulation Terminated...")


if __name__ == "__main__":
    
    main()
