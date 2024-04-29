# Based on (https://gadget-geek-prashant.blogspot.com/2015/07/writing-python-module-to-simulate-lcd.html#.VZ-5gHWlyko)

import pygame
import Colors

class VirtLCD():
	def __init__(self, x, y, chars=16, lines=2):
		
		self.char_w = 12
		self.line_h = 20
		self.chars = chars
		self.lines = lines
		self.scrolling = False

		self.marginX = 8
		self.marginY = 4
		self.size = [self.char_w*chars, self.line_h*lines]
		self.data = [""*chars]*lines
		self.x = x
		self.y = y
		
		self.font = pygame.font.SysFont("consolas", 20)
		self.label = self.font.render(f"LCD {chars}x{lines}", False, Colors.BLACK)

	def setData(self, data):
		# Add checks, scrolling, padding etc here
		self.data = data
	
	def update(self, screen):
		pygame.draw.rect(screen, Colors.BLACK, (self.x, 
							self.y, 
							self.size[0], 
							self.size[1]+(self.marginY*self.lines)))
		screen.blit(self.label, (self.x+(self.size[0]//2)-(self.label.get_rect().width//2), 
					 self.y+(self.size[1]+20)-(self.label.get_rect().height//2)))
		
		for i, line_data in enumerate(self.data):
			line = self.font.render(line_data, 2, Colors.GREEN)
			screen.blit(line, (self.x+self.marginX, 
					   self.y+(self.line_h*i)+(self.marginY*(i+1))))
