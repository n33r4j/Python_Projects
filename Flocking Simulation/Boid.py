# Boid Class

import pygame
import math

class Boid:
    def __init__(self, sNum, sprite, pos, angle, color):
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
        # self.rect = pygame.Rect(self.pos[0], self.pos[1], 1, 1)
    
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
    
    def rotate(self, surface, angle):
        rotated_sprite = pygame.transform.rotozoom(surface, angle, 1) # scale = 1
        rotated_rect = rotated_sprite.get_rect(center = (self.pos[0],self.pos[1]))
        return rotated_sprite, rotated_rect
    
    def setAng_Vel(self, ang_vel):
        self.ang_vel = ang_vel
        
    def setAng_Accel(self, ang_accel):
        self.ang_accel = ang_accel
    
    def Update(self):
        self.vel[0] += self.accel[0]
        self.vel[1] += self.accel[1]
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]
        
        new_angle = math.degrees(math.atan2(-self.vel[1],self.vel[0]))
        self.angle = -90.0 + new_angle
    
    def Draw(self, window):
        rotated_sprite, rotated_rect = self.rotate(self.sprite, self.angle)
        window.blit(rotated_sprite, rotated_rect)
    