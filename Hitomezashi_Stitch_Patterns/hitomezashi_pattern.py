# Hitomezashi Stitch Patterns
# [https://youtu.be/JbfhzlMk2eY]

import pygame
import random
import pathlib, os

CELL_SIZE = 10
WIDTH, HEIGHT = 1024, 576
offsetX, offsetY = 5, 5
P_WIDTH, P_HEIGHT = (WIDTH//CELL_SIZE), (HEIGHT//CELL_SIZE)
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
L_GREEN = (126,222,9)
GREY = (52,54,50)
D_GREY = (37,38,36)
RED = (200,5,5)


PREFIX = pathlib.Path(__file__).parent.resolve()


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


def createPattern(num1, num2, color=BLUE, thickness = 4, shift=1, bg_color=BLACK, showGrid=False):
    WIN.fill(bg_color)
    
    if showGrid:
        createDotGrid(P_WIDTH, P_HEIGHT, CELL_SIZE)
    
    # Horizontal
    for i, char in enumerate(num1):
        if int(char):
            for j in range(0, P_WIDTH - 1, 2):
                start = (offsetX + (j*CELL_SIZE), offsetY + (i*CELL_SIZE))
                end = (offsetX + ((j+1)*CELL_SIZE), offsetY + (i*CELL_SIZE))
                # pygame.draw.aaline(WIN, color, start, end, thickness)
                pygame.draw.line(WIN, color, start, end, thickness)
        else:
            for j in range(shift, P_WIDTH - 1, 2):
                start = (offsetX + (j*CELL_SIZE), offsetY + (i*CELL_SIZE))
                end = (offsetX + ((j+1)*CELL_SIZE), offsetY + (i*CELL_SIZE))
                # pygame.draw.aaline(WIN, color, start, end, thickness)
                pygame.draw.line(WIN, color, start, end, thickness)
    
    # Vertical
    for i, char in enumerate(num2):
        if int(char):
            for j in range(0, P_HEIGHT - 1, 2):
                start = (offsetX + (i*CELL_SIZE), offsetY + (j*CELL_SIZE))
                end = (offsetX + (i*CELL_SIZE), offsetY + ((j+1)*CELL_SIZE))
                # pygame.draw.aaline(WIN, color, start, end, thickness)
                pygame.draw.line(WIN, color, start, end, thickness)
        else:
            for j in range(shift, P_HEIGHT - 1, 2):
                start = (offsetX + (i*CELL_SIZE), offsetY + (j*CELL_SIZE))
                end = (offsetX + (i*CELL_SIZE), offsetY + ((j+1)*CELL_SIZE))
                # pygame.draw.aaline(WIN, color, start, end, thickness)
                pygame.draw.line(WIN, color, start, end, thickness)
    
    pygame.display.update()
    
    
def main():
    pygame.init()
    
    global SIM_RUN
    num1 = getRandomBinaryNum(P_HEIGHT)
    num2 = getRandomBinaryNum(P_WIDTH)
    
    print(f'num1: {num1}')
    print(f'num2: {num2}')
    
    PatternCreated = False
    
    clock = pygame.time.Clock()
    
    while SIM_RUN:
        clock.tick(FPS_MAX)
        
        if not PatternCreated:
            createPattern(num1, num2, L_GREEN, thickness=2, shift=1, bg_color=D_GREY)
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
