# Flocking Simulation
# (https://www.youtube.com/watch?v=mhjuuHl6qHM&list=PLRqwX-V7Uu6ZiZxtDDRCi6uhfTH4FilpH&index=179)

import pygame
import pathlib, os
from Colors import *
# from Boid import Boid
from Flock import Flock
import random

WIDTH, HEIGHT = 1200, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flocking Simulation")

MAX_FPS = 60
SIM_RUN = True
SIM_PAUSED = False

PREFIX = pathlib.Path(__file__).parent.resolve()

# Sprite
BOID_IMAGE = pygame.image.load(os.path.join(PREFIX,"assets","boid_green.png"))
BOID_SIZE = 24.0
BOID_SPRITE = pygame.transform.scale(BOID_IMAGE, (BOID_SIZE, BOID_SIZE))

# Draw stuff on the main window
def Draw_Window(flock):
    WIN.fill(BLACK)
    # Add code here
    # boid.Draw(WIN)
    flock.Draw(WIN)
    pygame.display.update()

# Handle Keyboard Input
def Handle_Input(event):
    global SIM_RUN
    global SIM_PAUSED
    
    if event.key == pygame.K_p:
        SIM_PAUSED = not SIM_PAUSED
        
    if event.key == pygame.K_q:
        SIM_RUN = False
        


def main():
    pygame.init()
    
    global SIM_RUN
    
    clock = pygame.time.Clock()
    
    # b1 = Boid(1, BOID_SPRITE, [WIDTH/2.0, HEIGHT/2.0], 0.0, GREEN)
    # b1.setVel([-1.0,0.0])
    # b1.setVel([random.uniform(-1.0, 1.0),random.uniform(-1.0, 1.0)])
    
    flock = Flock(10, BOID_SPRITE,[WIDTH/2, HEIGHT/2])
    flock.setVel([random.uniform(-1.0, 1.0),random.uniform(-1.0, 1.0)])
    # flock.setPosGoal([1000,100])
    
    while SIM_RUN:
        clock.tick(MAX_FPS)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                SIM_RUN = False
            
            if event.type == pygame.KEYDOWN:
                Handle_Input(event)
            
            if event.type == pygame.MOUSEBUTTONUP:
                mousePos = pygame.mouse.get_pos()
                flock.setPosGoal(mousePos)
            
        if not SIM_PAUSED:
            # b1.Update()
            # Draw_Window(b1)
            flock.Update()
            Draw_Window(flock)
            
        
    pygame.quit()
    print("Terminating Simulation...")

    
if __name__ == "__main__":
    main()