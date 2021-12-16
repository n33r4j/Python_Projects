# Test Script

import pygame, sys
import os

def rotate(surface, angle):
    rotated_sprite = pygame.transform.rotozoom(surface, angle, 1)
    rotated_rect = rotated_sprite.get_rect(center = (300,300))
    return rotated_sprite, rotated_rect

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((600,600))

PREFIX = os.path.dirname(__file__)
# print(PREFIX)
image_path = os.path.join(PREFIX, "assets", "boid_v1.png")
boid_image = pygame.image.load(image_path)
# If for some reason, the image background is showing even though it is
# transparent, pass a second argument 'pygame.SRCALPHA' during creation
# of the surface.
boid_rect = boid_image.get_rect(center=(300,300))

angle = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
    angle += 0.5
    screen.fill((0,0,0))
    
    boid_image_rotated, boid_rect = rotate(boid_image, angle)
    
    # boid_image = pygame.transform.rotozoom(boid_image, angle, 1)
    # boid_image = pygame.transform.rotate(boid_image, angle)
    # Calling transform.rotate returns a lower quality image every time.
    # So if called multiple times, the image would look terrible and pygame 
    # might crash.
    # With transform.rotozoom, the quality is a bit better but simulation
    # still slows down and pygame might crash.
    # To fix this, we need to write a function that always rotates the 
    # image from its starting orientation(i.e. 0 deg) to a desired orientation.
    # Explained well in this video -> [https://www.youtube.com/watch?v=eGsMMpAglIg]
    # boid_rect = boid_image.get_rect(center = (300,300))
    # screen.blit(boid_image, boid_rect)
   
    screen.blit(boid_image_rotated, boid_rect)
    pygame.display.flip()
    clock.tick(60)
    
    