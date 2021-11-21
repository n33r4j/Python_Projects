# Pendulum class

import pygame
import math

class Pendulum:
    def __init__(self, anchor_pos, arm_length, bob_radius, arm_color=(5,200,5), bob_color=(200,5,5), show_trail=False):
        self.anchor_pos = anchor_pos
        self.arm_length = arm_length
        self.arm_color = arm_color
        self.bob_radius = bob_radius
        self.bob_color = bob_color
        self.bob_pos = (anchor_pos[0],anchor_pos[1] + arm_length)
        self.show_trail = show_trail
        self.bob_pos = (0,0)
        self.arm_thickness = 1
        self.anchor_marker_size = 4
        self.angle = 0.0 #pointing down
        self.angular_velocity = 0.0
        self.angular_acceleration = 0.0

    def Update(self, gravity, drag):
        self.angular_acceleration = -gravity * math.sin(self.angle)/self.arm_length
        self.angular_velocity += self.angular_acceleration
        self.angular_velocity *= (1.0 - drag)
        self.angle += self.angular_velocity
        self.bob_pos = (self.anchor_pos[0]+(self.arm_length*math.sin(self.angle)),
                        self.anchor_pos[1]+(self.arm_length*math.cos(self.angle)))
    
    def Draw(self, window):
        #anti-aliased line
        pygame.draw.aaline(window, self.arm_color, self.anchor_pos, self.bob_pos, self.arm_thickness)
        
        if(self.show_trail):
            pygame.draw.circle()
        
        pygame.draw.circle(window, (255,255,5), self.anchor_pos, self.anchor_marker_size)
        pygame.draw.circle(window, self.bob_color, self.bob_pos, self.bob_radius)
    
    def setAngle(self, angle):
        self.angle = math.radians(angle)
    
    def setAngularVelocity(self, ang_vel):
        self.angular_velocity = ang_vel
    