# Pygame Video Recorder

import os
import pygame
import pickle
import cv2


class Video_Recorder:
    def __init__(self, prefix, folderName=None):
        self.path = ""
        self.videoName = ""
        if not folderName:
            unused_suffix = 1
            unused_suffix_fname = "U_SUFFIX.pickle"
            path = os.path.join(prefix, unused_suffix_fname)
            
            if os.path.exists(path):
                f = open(path, "rb")
                unused_suffix = pickle.load(f)
                f.close()
            
            self.videoName = "video_"+str(unused_suffix)
            self.path = os.path.join(prefix,"videos",self.videoName)
            
            unused_suffix += 1
            f = open(path, "wb")
            pickle.dump(unused_suffix, f)
            f.close()
                
        else:
            self.videoName = folderName
            self.path = os.path.join(prefix,"videos",folderName)
        
        print("Video frames folder path:", self.path)
        os.mkdir(self.path)
        self.frameCounter = 1
        
    def CaptureFrame(self, window):
        filename = "frame_"+str(self.frameCounter)+".jpg"
        filepath = os.path.join(self.path, filename)
        pygame.image.save(window, filepath)
        print(f'frame {self.frameCounter} saved...')
        self.frameCounter += 1
        
    def GenerateVideo(self, prefix, folderName=None):
        frame_folder = ""
        
        if not folderName:
            frame_folder = self.videoName
        else:
            frame_folder = folderName
        
        file_type = ".mp4"
        path = os.path.join(prefix,'videos',frame_folder, '.')
        print(len(os.listdir(path)),"frames found in", frame_folder)
        print("Generating video, please wait...")
        
        # height, width, layers = frame.shape()
        
        width, height = 1200, 800 # add a better way to set this.
        framerate = 30.0
        four_cc = cv2.VideoWriter_fourcc(*'mp4v')
        video = cv2.VideoWriter(os.path.join(prefix,"video_releases",frame_folder + "-release" + file_type), four_cc, framerate, (width, height)) 
        images = sorted([image for image in os.listdir(path)], key=lambda x: int(x[6:-4]))
        # for image in images:
            # print(image)
        
        for image in images:
            video.write(cv2.imread(os.path.join(path, image))) 
          
        # Deallocating memory taken for window creation (Is this required ?)
        cv2.destroyAllWindows() 
        video.release()  # releasing the video generated
        
        print("MP4 file saved to video_releases folder.")
        