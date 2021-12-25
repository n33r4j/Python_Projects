# Virtual Environments - based on [https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/#creating-a-virtual-environment]
# On Windows:
# To Create a virtual environment: py -m venv [name of enironment or 'env' as default]
# To Activate it: .\env\Scripts\activate
# To Deactivate it: deactivate
# To confirm you're using venv: where python
# To generate a 'requirements.txt' file: pip install pipreqs
#                                        pipreqs [path to the project, '.' if you are in the project directory]

# Flocking Simulation
# (https://www.youtube.com/watch?v=mhjuuHl6qHM&list=PLRqwX-V7Uu6ZiZxtDDRCi6uhfTH4FilpH&index=179)

import pygame
import pathlib, os
from Colors import *
# from Boid import Boid
from Flock import Flock
from Video_Recorder import Video_Recorder
import random

WIDTH, HEIGHT = 1200, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flocking Simulation")

MAX_FPS = 60
SIM_RUN = True
SIM_PAUSED = False

# For recording the simulation window and generating an mp4 file.
RECORD_VIDEO = False

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
    # print(WIN.get_size())
    flock = Flock(0, BOID_SPRITE,[WIDTH/2, HEIGHT/2], showVRadius=True)
    # flock.setRandomVel()
    # flock.setPosGoal([1000,100])
    # counter = 0
    
    if RECORD_VIDEO:
        v_rec = Video_Recorder(PREFIX)
    
    while SIM_RUN:
        dt = clock.tick(MAX_FPS)
        # print(clock.get_fps())
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                SIM_RUN = False
            
            if event.type == pygame.KEYDOWN:
                Handle_Input(event)
            
            if event.type == pygame.MOUSEBUTTONUP:
                mousePos = list(pygame.mouse.get_pos())
                flock.createAddBoid(mousePos, WHITE)
                # counter += 1
            
        if not SIM_PAUSED:
            # b1.Update()
            # Draw_Window(b1)
            flock.Align(1.0)
            # flock.Cohesion(1.0)
            # flock.Separation(1.0)
            flock.Update(dt)
            Draw_Window(flock)
            
            if RECORD_VIDEO:
                v_rec.CaptureFrame(WIN)
            
            # Just using Align() seems to have the desired flocking behaviour. However,
            # adding Cohesion() breaks up this flocking behaviour.
        
    pygame.quit()
    print("Terminating Simulation...")
    
    if RECORD_VIDEO:
        v_rec.GenerateVideo(PREFIX) # Most recently captured file by default.

    
if __name__ == "__main__":
    main()