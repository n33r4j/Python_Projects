# Test Script

# import pygame, sys
import os
import pickle
# from PIL import Image
import cv2

# def rotate(surface, angle):
    # rotated_sprite = pygame.transform.rotozoom(surface, angle, 1)
    # rotated_rect = rotated_sprite.get_rect(center = (300,300))
    # return rotated_sprite, rotated_rect

# pygame.init()
# clock = pygame.time.Clock()
# screen = pygame.display.set_mode((600,600))

PREFIX = os.path.dirname(__file__)
# # print(PREFIX)
# image_path = os.path.join(PREFIX, "assets", "boid_v1.png")
# boid_image = pygame.image.load(image_path)
# # If for some reason, the image background is showing even though it is
# # transparent, pass a second argument 'pygame.SRCALPHA' during creation
# # of the surface.
# boid_rect = boid_image.get_rect(center=(300,300))

# angle = 0

# FPSs = [10, 30, 60, 90, 120]
# fps_ind = 1

# while True:
    # dt = clock.tick(FPSs[fps_ind])
    
    # for event in pygame.event.get():
        # if event.type == pygame.QUIT:
            # pygame.quit()
            # sys.exit()
        
        # if event.type == pygame.KEYDOWN:
            # if event.key == pygame.K_f:
                # fps_ind += 1
                # fps_ind %= 5
                # print("FPS is", FPSs[fps_ind])
        
    # angle += 0.5*dt
    # screen.fill((0,0,0))
    # # print(pygame.time.get_ticks())
    # boid_image_rotated, boid_rect = rotate(boid_image, angle)
    
    # # boid_image = pygame.transform.rotozoom(boid_image, angle, 1)
    # # boid_image = pygame.transform.rotate(boid_image, angle)
    # # Calling transform.rotate returns a lower quality image every time.
    # # So if called multiple times, the image would look terrible and pygame 
    # # might crash.
    # # With transform.rotozoom, the quality is a bit better but simulation
    # # still slows down and pygame might crash.
    # # To fix this, we need to write a function that always rotates the 
    # # image from its starting orientation(i.e. 0 deg) to a desired orientation.
    # # Explained well in this video -> [https://www.youtube.com/watch?v=eGsMMpAglIg]
    # # boid_rect = boid_image.get_rect(center = (300,300))
    # # screen.blit(boid_image, boid_rect)
   
    # screen.blit(boid_image_rotated, boid_rect)
    # pygame.display.flip()
    
if __name__ == "__main__":
    # num = 24
    # pickle_filename = "num.pickle"
    # path = os.path.join(PREFIX, pickle_filename)
    # f = open(path, "wb")
    # pickle.dump(num, f)
    # f.close()
    
    # f = open(path, "rb")
    # r_num = pickle.load(f)
    # print(r_num)
    frame_folder = 'video_3'
    file_type = ".mp4"
    path = os.path.join(PREFIX,'videos',frame_folder, '.')
    print(len(os.listdir(path)),"frames found.")
    
    # frame = cv2.imread(os.path.join(path, file))
    # height, width, layers = frame.shape()
    
    width, height = 1200, 800
    framerate = 30.0
    four_cc = cv2.VideoWriter_fourcc(*'mp4v')
    video = cv2.VideoWriter(os.path.join(PREFIX,"video_releases",frame_folder + "-release" + file_type), four_cc, framerate, (width, height)) 
    images = sorted([image for image in os.listdir(path)], key=lambda x: int(x[6:-4]))
    # for image in images:
        # print(image)
    
    for image in images:
        video.write(cv2.imread(os.path.join(path, image))) 
      
    # Deallocating memory taken for window creation (Is this required ?)
    cv2.destroyAllWindows() 
    video.release()  # releasing the video generated
    
    