# Graph Node class

import pygame

class Node:
    def __init__(self, pos, radius, index, color):
        self.radius = radius
        self.pos = pos
        self.index = index
        self.color = color
        self.Degree = 0
        self.edges = {}
        
        
    def Draw(self, window):
        pygame.draw.circle(window, self.color, self.pos, self.radius)
        
    def Update(self):
        pass
    
    def setPosition(self, pos):
        self.pos = pos
        
    def addNode(self, index, edge_weight):
        self.edges[index] = edge_weight