# Ray class

import math
import pygame
from Colors import *
from Boundary import Boundary

class Ray:
    def __init__(self, x, y, angle):
        self.tag = "ray"
        self.x = x
        self.y = y
        self.angle = angle # degrees
        self.scale = 3.0
        self.direction = [math.cos(math.radians(self.angle)), math.sin(math.radians(self.angle))]

    def cast(self, window, boundaries):
        nearest_X = None
        nearest_Y = None
        lowest_U = 100000000
        for boundary in boundaries:
            x_1 = boundary.p_A[0]
            y_1 = boundary.p_A[1]
            x_2 = boundary.p_B[0]
            y_2 = boundary.p_B[1]

            x_3 = self.x
            y_3 = self.y
            x_4 = self.x + self.direction[0]
            y_4 = self.y + self.direction[1]

            denom = ((x_1-x_2)*(y_3-y_4))-((y_1-y_2)*(x_3-x_4))
            if denom == 0:
                # Lines are parallel or colinear.
                continue
            else:
                # print("intersects")
                numer = ((x_1-x_3)*(y_3-y_4))-((y_1-y_3)*(x_3-x_4))
                t = numer/denom
                u = -(((x_1-x_2)*(y_1-y_3))-((y_1-y_2)*(x_1-x_3)))/denom
                # print(t, u)

                if t >= 0 and t <= 1 and u >= 0:
                    intersect_X = x_1 + t*(x_2-x_1)
                    intersect_Y = y_1 + t*(y_2-y_1)
                    # print(f"intersects at ({intersect_X}, {intersect_Y})")
                    if u < lowest_U:
                        lowest_U = u
                        nearest_X = intersect_X
                        nearest_Y = intersect_Y

        if nearest_X and nearest_Y:
            pygame.draw.aaline(window, GREEN, [self.x, self.y], [nearest_X, nearest_Y])
            pygame.draw.circle(window, YELLOW, [nearest_X, nearest_Y], 2.0)
            
    def setPosition(self, pos):
        self.x = pos[0]
        self.y = pos[1]

    def setAngle(self, angle):
        self.angle = angle
        self.direction = [math.cos(math.radians(self.angle)), math.sin(math.radians(self.angle))]
    
    def setAngleFromPos(self, pos):
        self.angle = math.degrees(math.atan2((pos[1] - self.y),(pos[0] - self.x)))
        self.direction = [math.cos(math.radians(self.angle)), math.sin(math.radians(self.angle))]

    def setDirection(self, pos):
        denom_X = abs(pos[0] - self.x)
        denom_Y = abs(pos[1] - self.y)
        if denom_X != 0:
            self.direction[0] = (pos[0] - self.x)/denom_X
        if denom_Y != 0:
            self.direction[1] = (pos[1] - self.y)/denom_Y
        print(self.direction)

    def draw(self, window):
        pygame.draw.circle(window, L_BLUE, [self.x, self.y], 2.0)
        pygame.draw.aaline(window, GREY, [self.x, self.y], [self.x + (self.direction[0]*self.scale), self.y + (self.direction[1]*self.scale)])

