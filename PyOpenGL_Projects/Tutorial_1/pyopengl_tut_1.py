# PyOpenGL Tutorial [https://www.youtube.com/watch?v=R4n4NyDG2hI&list=PLQVvvaa0QuDdfGpqjkEJSeWKGCP31__wD]

import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

SIM_RUN = True

# Cube
vertices = (
    ( 1,-1,-1),
    ( 1, 1,-1),
    (-1, 1,-1),
    (-1,-1,-1),
    ( 1,-1, 1),
    ( 1, 1, 1),
    (-1, 1, 1),
    (-1, -1, 1)
)

plane_vertices = (
    ( 10, -1, 5),
    ( 10, -1,-20),
    (-10, -1,-20),
    (-10, -1, 5)
)

edges = (
    (0, 1),
    (0, 3),
    (0, 4),
    (2, 1),
    (2, 3),
    (2, 6),
    (7, 3),
    (7, 4),
    (7, 6),
    (5, 1),
    (5, 4),
    (5, 6)
)

surfaces = (
    (0, 1, 2, 3),
    (2, 3, 7, 6),
    (4, 5, 6, 7),
    (4, 5, 1, 0),
    (1, 5, 6, 2),
    (4, 0, 3, 7)
)

colors = (
    (1,0,0),
    (0,1,0),
    (0,0,1),
    (1,1,0),
    (1,0,1),
    (0,1,1)
)

def Cube():
    glBegin(GL_QUADS)
    for surface in surfaces:
        x = 0
        for vertex in surface:
            glColor3fv(colors[x]) # can be outside the loop as well.
            glVertex3fv(vertices[vertex])
            x += 1
    glEnd()

    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()

def Plane():
    glBegin(GL_QUADS)
    x = 0
    for vertex in plane_vertices:
        glColor3fv(colors[x])
        glVertex3fv(vertex)
        x += 1
    glEnd()

    glBegin(GL_LINES)
    glColor3fv((0,0.9,0)) 
    for vertex in plane_vertices:
        glVertex3fv(vertex)
    glEnd()


def main():
    pygame.init()
    display = (800,600)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)

    global SIM_RUN

    move_X = 0.0
    move_Y = 0.0

    # fov, aspect ratio, z_near, z_far (for clipping plane) 
    gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)

    glTranslatef(0.0,-1.0,-10.0)

    # glRotatef(0, 0, 0, 0)

    while SIM_RUN:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                SIM_RUN = False
                break
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    move_X = 0.1
                if event.key == pygame.K_RIGHT:
                    move_X = -0.1
                if event.key == pygame.K_UP:
                    move_Y = -0.1
                if event.key == pygame.K_DOWN:
                    move_Y = 0.1
            
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    move_X = 0.0
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    move_Y = 0.0
            
            # scrolling zoom
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4: # scroll-up
                    glTranslate(0,0,0.3)
                if event.button == 5: # scroll-down
                    glTranslate(0,0,-0.3)

        # glRotatef(1, 0, 1, 0)
        glTranslate(move_X,move_Y,0)
        view_pos = glGetDoublev(GL_MODELVIEW_MATRIX)
        view_x = view_pos[3][0]
        view_y = view_pos[3][1]
        view_z = view_pos[3][2]

        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        if view_y <= 1:
            Plane()
            Cube()
        else:
            Cube()
            Plane()
        pygame.display.flip() # display.update() does not work with an OPENGL display.
        pygame.time.wait(10)

    pygame.quit()
    quit()

if __name__ == "__main__":
    main()