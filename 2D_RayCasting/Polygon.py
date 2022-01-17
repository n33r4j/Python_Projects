import pygame
import random
from Boundary import Boundary

class Polygon:
    def __init__(self, vertices = []):
        self.tag = "polygon"
        self.vertices = []
        self.sides = []
        if len(vertices) == 0:
            # print("Add random vertices for polygon...")
            for i in range(random.randint(3, 3)):
                self.vertices.append([random.randint(20, 650), random.randint(20, 450)])
            # print(f"{len(self.vertices)} random vertices added...")
        
        for i, vert in enumerate(self.vertices):
            self.sides.append(Boundary(self.vertices[i],self.vertices[(i+1)%len(self.vertices)]))
            # print(f"{len(self.sides)} boundary sides created...")

    def draw(self, window):
        for side in self.sides:
            side.draw(window)


if __name__ == "__main__":
    l1 = [[1,1],[2,2],[3,3],[4,4]]
    l2 = [[5,5],[7,7],[8,8],[9,9]]
    print(l1, l2)
    l1 += l2
    print(l1)