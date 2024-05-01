import pygame
import math
import Colors
import time


def getDist(p1, p2):
	return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

class VirtPIR:
	def __init__(self, x, y, r):
		self.timeout = 2 # seconds
		self.sensitivity = 10 # pixels
		self.motion_detected = False
		
		self.prev_mouse_pos = pygame.mouse.get_pos()
		self.curr_distance = 0
		self.curr_mouse_pos = pygame.mouse.get_pos()
		
		self.circle_radius = r
		self.circle_center = (x, y)
		big_font = pygame.font.SysFont("arial", 40)
		self.small_font = pygame.font.SysFont("arial", 20)
		self.label = big_font.render("PIR", False, Colors.BLACK)
		self.timer_label = self.small_font.render(f"timer:{0}", False, Colors.BLACK)
		
		self.start_time = 0

	def timerElapsed(self):
		return (time.time() - self.start_time) > self.timeout
	
	def draw(self, screen):
		screen.blit(self.label, (self.circle_center[0]-self.label.get_rect().width//2, 
								 self.circle_center[0]-self.label.get_rect().width//2))
		pygame.draw.circle(screen, Colors.BLACK, self.circle_center, self.circle_radius, 2)
		screen.blit(self.timer_label, (self.circle_center[0]-20, 
					       			   self.circle_center[1]+self.circle_radius+10))
		
		if self.motion_detected:
			pygame.draw.circle(screen, Colors.GREEN, self.circle_center, self.circle_radius-10)
		
		# Mouse pointer
		if self.curr_distance <= self.circle_radius:
			pygame.draw.circle(screen, Colors.RED, self.curr_mouse_pos, 5)  # Draw a small red dot at mouse position
			

	def update(self):
		self.curr_mouse_pos = pygame.mouse.get_pos()
		self.curr_distance = getDist(self.curr_mouse_pos, self.circle_center)
		
		if self.timerElapsed():
			self.motion_detected = False
			self.timer_label = self.small_font.render(f"timer:{0}", False, Colors.BLACK)
			
			if self.curr_distance <= self.circle_radius:
				# Check if the mouse has moved
				if getDist(self.curr_mouse_pos, self.prev_mouse_pos) > self.sensitivity:
					#print("moving")
					self.motion_detected = True
					# Reset timer
					self.start_time = time.time()
		else:
			self.timer_label = self.small_font.render(f"timer:{self.timeout-(time.time() - self.start_time):.2f}", False, Colors.BLACK)
		
		self.prev_mouse_pos = self.curr_mouse_pos
