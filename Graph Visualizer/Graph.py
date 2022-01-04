# Graph class

from os import X_OK
import pygame
from Node import Node
from Colors import *
import math

# number of points, index, position of center, radius of circle
def pointOnCircle(n, i, center_pos, radius):
    angle = math.radians(i*360/n)
    x = center_pos[0] + (radius*math.cos(angle))
    y = center_pos[1] + (radius*math.sin(angle))
    return x, y


class Graph:
    def __init__(self, filename):

        self.nodes = {}
        self.edges = {}
        # self.posX_counter = 10
        # self.posY_counter = 10

        self.pos_counter = 0 # For placement of nodes

        with open("graph_1.txt", 'r') as input_file:
            lines = [line for line in input_file.readlines() if line[0] != '#']
            for line in lines:
                line = line.strip(' \n').split(" ")
                # print(line)
                if line and line[0] != '#':
                    if len(line) != 4:
                        print("Error: Invalid format for line in input file.", "line: ", line)
                    else:                        
                        # check if node exists
                        if line[0] in self.edges.keys():
                            node = self.nodes[line[0]]
                        else:
                            node = Node(line[0], (0,0), 16.0, RED)
                            self.edges[line[0]] = []
                            self.pos_counter += 1

                        if line[2] in self.edges.keys():
                            other_node = self.nodes[line[2]]
                        else:
                            other_node = Node(line[2], (0,0), 16.0, RED)
                            self.edges[line[2]] = []
                            self.pos_counter += 1

                        node.addNode(line[2], line[3])
                        other_node.addNode(line[0], line[3])
                        
                        self.nodes[line[0]] = node
                        self.nodes[line[2]] = other_node
                        self.edges[line[0]].append(line[2])
                        self.edges[line[2]].append(line[0])
        
        for i in self.nodes:
            self.nodes[i].setPosition(pointOnCircle(len(self.nodes), self.pos_counter, (400, 400), 300))
            self.pos_counter += 1


    def Draw(self, window):
        for i in self.edges:
            start_pos = self.nodes[i].pos
            for j in self.edges[i]:
                end_pos = self.nodes[j].pos
                pygame.draw.aaline(window, GREEN, start_pos, end_pos)
    
        for i in self.nodes:
            self.nodes[i].Draw(window)

                    
