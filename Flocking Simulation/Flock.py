# Flock Class

from Boid import Boid
from Colors import *
import random


class Flock:
    def __init__(self, boidCount, boidSprite, spawnPos=[0,0], boidColor=WHITE):
        self.boids = []
        self.boidCount = boidCount
        for i in range(boidCount):
            #set random positions and orientations.
            pos = [random.randint(spawnPos[0] - 50, spawnPos[0] + 50), random.randint(spawnPos[1] - 50, spawnPos[1] + 50)]
            angle = 0.0
            self.boids.append(Boid(i, boidSprite, pos, angle, boidColor))
        
        print("Boid Flock initialization complete...")
    
    def setVel(self, vel):
        for boid in self.boids:
            boid.setVel(vel)
    
    def Update(self):
        for boid in self.boids:
            boid.Update()
    
    def Draw(self, window):
        for boid in self.boids:
            boid.Draw(window)
    