import pygame
from pygame.math import Vector2
import Colors

# See https://stackoverflow.com/a/49413006

class VirtServo():
	def __init__(self, x, y):
		self.starting_angle = 0 # deg
		self.target_angle = 0 # deg
		self.target_reached = True
		self.angle = 0 # deg, current
		self.max_range = 179 # deg
		self.speed = 0.5 # deg/sec
		self.direction = -1 # anticlockwise
		self.x = x
		self.y = y
		
		self.image = pygame.image.load('textures/servo_horn.png')
		self.housing_image = pygame.image.load('textures/servo_housing.png')
		
		self.orig_image = self.image
		self.center_pos = Vector2((x+25+self.image.get_rect().width//2, 
									y-50+self.image.get_rect().height//2))  # The original center position/pivot point.
		self.offset = Vector2(0, 2)
		self.pos = (x, y)
		self.rect = self.image.get_rect(center=self.center_pos)
		
		self.font = pygame.font.SysFont("arial", 20)
		self.label = self.font.render(f"servo1:{self.angle} deg", False, Colors.BLACK)
		
	def setTarget(self, angle):
		if abs(angle) <= self.max_range:
			self.target_angle = angle
			self.target_reached = False
			self.direction = -1 if ((((angle - self.angle)+180)%360) - 180) < 0 else 1
		else:
			print(f"angle:{angle} is beyond max range:+/-{self.max_range}")
		
	def rotate(self):
		self.image = pygame.transform.rotozoom(self.orig_image, -self.angle, 1)
		offset_rotated = self.offset.rotate(self.angle)
		# Create a new rect with the center of the sprite + the offset.
		self.rect = self.image.get_rect(center=self.center_pos+offset_rotated)
	
	def update(self):
		if self.angle != self.target_angle:
			if abs(self.angle) > self.max_range:
				self.angle += (360*(-1 if self.angle > 0 else 1))

			self.angle += self.speed*self.direction
			self.rotate()
		else:
			self.target_reached = True
		self.label = self.font.render(f"servo1:{self.angle} deg", False, Colors.BLACK)
		
	def draw(self, screen):
		screen.blit(self.housing_image, self.pos)
		screen.blit(self.image, self.rect)
		screen.blit(self.label, (self.pos[0]+60, self.pos[1]+80))
		pygame.draw.circle(screen, (255, 128, 0), self.center_pos, 3)
