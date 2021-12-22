# Flock Class

# Properties:
# 1) Separation: steer to avoid crowding local flockmates.
# 2) Alignment: steer towards the average heading of local flockmates.
# 3) Cohesion: steer to move toward the average position of local flockmates.

# Fixes/Improvements:
# - Taking a snapshot of all positions/velocities and using them to do the updates.
#   This should prevent any circular/spiraling update behaviours.
# - Performing the updates within each boid class. This would be more realistic.
# - To have it work faster for a larger number of boids, consider optimization 
#   techniques like using a quadtree.
# - Consider limiting the view of each boid to a section of the circle.
# - 

from Boid import Boid
from Colors import *
import random


class Flock:
    def __init__(self, boidCount, boidSprite, spawnPos=[0,0], boidColor=WHITE, showVRadius=False):
        self.boids = []
        self.boidCount = boidCount
        self.boidSprite = boidSprite
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
    
    # Create a new boid at position with random unit velocity.
    def createAddBoid(self, pos, color):
        self.boids.append(Boid(self.boidCount+1, self.boidSprite, pos, 0.0, color, self.showVRadius, True))
        self.boidCount += 1
        # self.boids[self.boidCount-1].setVel(vel)
        self.boids[self.boidCount-1].setVel([random.uniform(-1.0, 1.0)*1.0,random.uniform(-1.0, 1.0)*1.0])
    
    # This should be within the Boid class to be truly decentralized.
    def Align(self, alignmentForce):
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
                # they're not corrected sometimes ??
                avg_velX = velXSum/neigbhorsCount
                avg_velY = velYSum/neigbhorsCount
                if abs(avg_velX) != 0:
                    boid.accel[0] += ((avg_velX*alignmentForce)/abs(avg_velX)) - boid.vel[0]
                if abs(avg_velY) != 0:
                    boid.accel[1] += ((avg_velY*alignmentForce)/abs(avg_velY)) - boid.vel[1]
                
                if abs(boid.accel[0]) > boid.maxAccel:
                    boid.accel[0] = (boid.accel[0]/abs(boid.accel[0]))*boid.maxAccel*alignmentForce
                if abs(boid.accel[1]) > boid.maxAccel:
                    boid.accel[1] = (boid.accel[1]/abs(boid.accel[1]))*boid.maxAccel*alignmentForce
                
                
    def Cohesion(self, cohesionForce):
        for boid in self.boids:
            posXSum = 0.0
            posYSum = 0.0
            neigbhorsCount = 0
            for other_boid in self.boids:
                if boid.sNum != other_boid.sNum:
                    distX = boid.pos[0] - other_boid.pos[0]
                    distY = boid.pos[1] - other_boid.pos[1]
                    if (distX**2 + distY**2)**0.5 < boid.visibleRadius:
                       # Relative position
                       posXSum += (other_boid.pos[0] - boid.pos[0])
                       posYSum += (other_boid.pos[1] - boid.pos[1])
                       neigbhorsCount += 1
            if neigbhorsCount > 0:
                boid.accel[0] += ((posXSum*cohesionForce)/neigbhorsCount) - boid.vel[0]
                boid.accel[1] += ((posYSum*cohesionForce)/neigbhorsCount) - boid.vel[1]
                
                if abs(boid.accel[0]) > boid.maxAccel:
                    boid.accel[0] = (boid.accel[0]/abs(boid.accel[0]))*boid.maxAccel
                if abs(boid.accel[1]) > boid.maxAccel:
                    boid.accel[1] = (boid.accel[1]/abs(boid.accel[1]))*boid.maxAccel
    
    
    def Separation(self, separationForce):
        for boid in self.boids:
            repelX_Sum = 0.0
            repelY_Sum = 0.0
            neigbhorsCount = 0
            for other_boid in self.boids:
                if boid.sNum != other_boid.sNum:
                    distX = boid.pos[0] - other_boid.pos[0]
                    distY = boid.pos[1] - other_boid.pos[1]
                    dist = (distX**2 + distY**2)**0.5
                    if dist < boid.visibleRadius and dist < boid.separationThreshold:
                       # Relative position
                       repelX_Sum += ((-separationForce)/(other_boid.pos[0] - boid.pos[0]))
                       repelY_Sum += ((-separationForce)/(other_boid.pos[1] - boid.pos[1]))
                       neigbhorsCount += 1
            if neigbhorsCount > 0:
                boid.accel[0] += (repelX_Sum/neigbhorsCount)
                boid.accel[1] += (repelY_Sum/neigbhorsCount)
                
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
    