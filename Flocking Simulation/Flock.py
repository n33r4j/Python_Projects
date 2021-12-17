# Flock Class

# Properties:
# 1) Separation: steer to avoid crowding local flockmates.
# 2) Alignment: steer towards the average heading of local flockmates.
# 3) Cohesion: steer to move toward the average position of local flockmates.


from Boid import Boid
from Colors import *
import random


class Flock:
    def __init__(self, boidCount, boidSprite, spawnPos=[0,0], boidColor=WHITE, showVRadius=False):
        self.boids = []
        self.boidCount = boidCount
        self.posGoalSet = False
        self.posGoal = [0, 0]
        self.showVRadius = showVRadius
        for i in range(boidCount):
            #set random positions and orientations.
            pos = [random.randint(spawnPos[0] - 300, spawnPos[0] + 300), random.randint(spawnPos[1] - 50, spawnPos[1] + 50)]
            angle = 0.0
            self.boids.append(Boid(i+1, boidSprite, pos, angle, boidColor, self.showVRadius, True))
        
        print("Boid Flock initialization complete...")
    
    def setVel(self, vel):
        for boid in self.boids:
            boid.setVel(vel)
    
    def setRandomVel(self):
        for boid in self.boids:
            boid.setVel([random.uniform(-1.0, 1.0)*1.0,random.uniform(-1.0, 1.0)*1.0])
            
    def setPosGoal(self, posGoal):
        self.posGoal = posGoal
        self.posGoalSet = True
        for boid in self.boids:
            boid.setPosGoal(self.posGoal)
    
    # This should be within the Boid class to be truly decentralized.
    def Align(self):
        for boid in self.boids:
            velXSum = 0.0
            velYSum = 0.0
            neigbhorsCount = 0
            for other_boid in self.boids:
                if boid.sNum != other_boid.sNum:
                    distX = boid.pos[0] - other_boid.pos[0]
                    distY = boid.pos[1] - other_boid.pos[1]
                    if (distX**2 + distY**2)**0.5 < boid.visibleRadius:
                       velXSum += other_boid.vel[0]
                       velYSum += other_boid.vel[1]
                       neigbhorsCount += 1
            if neigbhorsCount > 0:
                # print(f'{boid.sNum}: {neigbhorsCount}')
                # ISSUE: If two boids are approaching more-or-less head on,
                # they're not corrected since align merely checks that they're
                # parallel.
                boid.accel[0] = (velXSum/neigbhorsCount) - boid.vel[0]
                boid.accel[1] = (velYSum/neigbhorsCount) - boid.vel[1]
                
                if abs(boid.accel[0]) > boid.maxAccel:
                    boid.accel[0] = (boid.accel[0]/abs(boid.accel[0]))*boid.maxAccel
                if abs(boid.accel[1]) > boid.maxAccel:
                    boid.accel[1] = (boid.accel[1]/abs(boid.accel[1]))*boid.maxAccel
                
            
    def Update(self, dt):
        for boid in self.boids:
            boid.Update(dt)
    
    def Draw(self, window):
        for boid in self.boids:
            boid.Draw(window)
    