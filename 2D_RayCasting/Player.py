
from Ray import Ray

class Player:
    def __init__(self, pos, eyes):
        self.pos = pos
        self.rays = []
        self.eyes = eyes
        for i in range(self.eyes):
            self.rays.append(Ray(self.pos[0], self.pos[1], i*(360/self.eyes)))

    def setPosition(self, pos):
        self.pos = pos
        for ray in self.rays:
            ray.setPosition(pos)

    def getRays(self):
        return self.rays