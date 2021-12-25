# Boid Class


import pygame
import math

class Boid:
    def __init__(self, sNum, sprite, pos, angle, color, showVRadius = False, wrapScreen=False):
        self.pos = pos
        # self.pos = pygame.math.Vector2(x, y)
        self.vel = [0.0, 0.0]
        self.accel = [0.0, 0.0]
        self.angle = angle      # heading
        self.ang_vel = 0.0      # heading
        self.ang_accel = 0.0      # heading
        self.color = color
        self.sNum = sNum        # serial number
        self.sprite = sprite
        self.rect = self.sprite.get_rect()
        self.wrap = wrapScreen
        
        self.posGoalSet = False
        self.posGoal = [0,0]
        self.maxVel = 0.3 # 0.3 is good
        self.maxAccel = 0.02 # How quickly it can turn, 0.02 is good
        
        self.visibleRadius = 60.0 # 60.0 is a good value.
        self.showVRadius = showVRadius
        self.separationThreshold = 10.0
    
    def setPos(self, pos):
        self.pos = pos
        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]
        
    def setVel(self, vel):
        self.vel = vel
        
    def setAccel(self, accel):
        self.accel = accel
        
    def setAngle(self, angle):
        self.angle = angle
    
    def setPosGoal(self, posGoal):
        self.posGoal = posGoal
        self.posGoalSet = True
    
    def rotate(self, surface, angle):
        rotated_sprite = pygame.transform.rotozoom(surface, angle, 1) # scale = 1
        rotated_rect = rotated_sprite.get_rect(center = (self.pos[0],self.pos[1]))
        return rotated_sprite, rotated_rect
    
    def setAng_Vel(self, ang_vel):
        self.ang_vel = ang_vel
        
    def setAng_Accel(self, ang_accel):
        self.ang_accel = ang_accel
    
    def setVisibleRadius(self, radius):
        self.visibleRadius = radius
    
    def Update(self, dt):
        if self.posGoalSet:
            x = self.posGoal[0] - self.pos[0]
            y = self.posGoal[1] - self.pos[1]
            norm = ((x*x)+(y*y))**0.5
            self.accel[0] = float(x)/norm * self.maxVel
            self.accel[1] = float(y)/norm * self.maxVel
            # if x == 0 and y == 0:
                # self.posGoalSet = False
                # self.accel = [0,0]
            
        self.vel[0] += self.accel[0]
        self.vel[1] += self.accel[1]
        
        if abs(self.vel[0]) > self.maxVel:
            self.vel[0] = (self.vel[0]/abs(self.vel[0]))*self.maxVel
        if abs(self.vel[1]) > self.maxVel:
            self.vel[1] = (self.vel[1]/abs(self.vel[1]))*self.maxVel
            
        self.accel[0] = 0.0
        self.accel[1] = 0.0
        
        self.pos[0] += (self.vel[0]*dt)
        self.pos[1] += (self.vel[1]*dt)
        
        # Wrap around
        if self.wrap:
            self.pos[0] %= 1200
            self.pos[1] %= 800
        
        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]
        
        new_angle = math.degrees(math.atan2(-self.vel[1],self.vel[0]))
        self.angle = -90.0 + new_angle
    
    def Draw(self, window):
        if self.showVRadius:
            wSize = window.get_size()
            surface = pygame.Surface(wSize, pygame.SRCALPHA)
            visionCircleColor = (100,100,100,50)
            pygame.draw.circle(surface, visionCircleColor,self.pos, self.visibleRadius)
            window.blit(surface, surface.get_rect())
        
        rotated_sprite, rotated_rect = self.rotate(self.sprite, self.angle)
        window.blit(rotated_sprite, rotated_rect)
    