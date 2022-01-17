# Boundary class

import pygame
from Colors import *

class Boundary:
    def __init__(self, pA, pB):
        self.tag = "boundary"
        self.p_A = pA
        self.p_B = pB
        self.direction = [0.0, 0.0]

    def setPoint(self, point, val):
        if point == 'A':
            self.p_A = val
        elif point == 'B':
            self.p_B = val
        else:
            print("Invalid point name. Choose 'A' or 'B'.")
        # self.direction = [(self.p_B[0] - self.p_A[0])/abs((self.p_B[0] - self.p_A[0])), (self.p_B[1] - self.p_A[1])/abs((self.p_B[1] - self.p_A[1]))]

    def draw(self, window):
        pygame.draw.line(window, RED, self.p_A, self.p_B, 3)
