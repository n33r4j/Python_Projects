# Graph Node class

import pygame

class Node:
    def __init__(self, index, pos, radius, color, value = 0):
        self.radius = radius
        self.pos = pos
        self.index = index
        self.value = value
        self.color = color
        self.inEdges = {} # indices of start nodes and their weight.
        self.outEdges = {} # indices of end nodes and their weight.
        self.degree = len(self.inEdges) + len(self.outEdges)
        
        
    def Draw(self, window):
        pygame.draw.circle(window, self.color, self.pos, self.radius)
        
    def Update(self):
        pass
    
    def getDegree(self):
        return self.degree

    def setPosition(self, pos):
        self.pos = pos
    
    def setColor(self, color):
        self.color = color

    def addNode(self, index, edge_weight):
        self.outEdges[index] = edge_weight
