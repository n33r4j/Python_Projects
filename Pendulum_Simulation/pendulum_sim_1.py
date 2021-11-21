# Pygame Pendulum Simulation

import pygame
import os
import math
from Pendulum import Pendulum

WIDTH, HEIGHT = 600, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pendulum Simulation 1")

FPS_MAX = 60
ZOOMED = False
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

# Draw stuff in the main window
def draw_window(pendulums, textsurface):
    WIN.fill(BLACK)
    
    linePos = 500
    for line in textsurface:
        WIN.blit(line, (50,linePos))
        linePos += 20
    
    for pendulum in pendulums:
        pendulum.Draw(WIN)
    
    pygame.display.update()

    
# Handling keyboard input
def handle_input(event):
    global SIM_RUN
    global SIM_PAUSED
    
    if event.key == pygame.K_p:
        SIM_PAUSED = not SIM_PAUSED
    
    if event.key == pygame.K_q:
        SIM_RUN = False

# Simulation
def main():
    pygame.init()
    
    clock = pygame.time.Clock()
    
    myfont = pygame.font.SysFont('Arial', 20, bold=True)
    
    pendulums = []
    arm_length = 270
    
    for i in range(50):
        pendulums.append(Pendulum((WIDTH/2, 300), arm_length, 5))
        pendulums[i].setAngle(175.0)
        arm_length -= 5
    
    print("[O] Starting Simulation...")
    
    
    while SIM_RUN:
        clock.tick(FPS_MAX)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if event.type == pygame.KEYDOWN:
                handle_input(event)
        
        if not SIM_PAUSED:
            currTime = pygame.time.get_ticks()
            
            # textsurface_1 = myfont.render('X pos: '+str(round(p1.bob_pos[0],2)), True, GREEN)
            # textsurface_2 = myfont.render('Y pos: '+str(round(p1.bob_pos[1],2)), True, GREEN)
            # textsurface_3 = myfont.render('Angle: '+str(round(math.degrees(p1.angle),2)), True, GREEN)
            # textsurface_4 = myfont.render('Time(s): '+str(currTime/1000.0), True, GREEN)
            
            for p in pendulums:
                p.Update(1.0, 0.003)
            
            # draw_window([p1,p2,p3,p4,p5], [textsurface_1, textsurface_2, textsurface_3, textsurface_4])
            draw_window(pendulums, [])
        
    pygame.quit()
    
    print("[X] Exiting game...")
    

if __name__ == "__main__":
    main()