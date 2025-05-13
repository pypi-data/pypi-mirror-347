import os
import sys
import time
import random
from PIL import Image
import cv2
import numpy as np
import keyboard
from pathlib import Path

class ImageGame:
    def __init__(self, folder_path):
        self.folder_path = folder_path
        self.image_files = []
        self.current_image = None
        self.current_index = 0
        self.paused = False
        self.blur_level = 100
        
        # Load all image files from the folder
        self.load_images()
        
    def load_images(self):
        valid_extensions = ('.png', '.jpg', '.jpeg', '.gif', '.bmp')
        self.image_files = [f for f in os.listdir(self.folder_path) 
                           if os.path.isfile(os.path.join(self.folder_path, f)) 
                           and f.lower().endswith(valid_extensions)]
        if not self.image_files:
            print("No valid images found in the folder!")
            sys.exit(1)
            
    def countdown(self):
        for i in range(3, 0, -1):
            print(f"{i}...")
            time.sleep(1)
        print("Start!")
        
    def load_random_image(self):
        self.current_index = random.randint(0, len(self.image_files) - 1)
        self.load_current_image()
        
    def load_current_image(self):
        image_path = os.path.join(self.folder_path, self.image_files[self.current_index])
        self.current_image = cv2.imread(image_path)
        self.blur_level = 100
        
    def load_next_image(self):
        self.current_index = (self.current_index + 1) % len(self.image_files)
        self.load_current_image()
        
    def load_previous_image(self):
        self.current_index = (self.current_index - 1) % len(self.image_files)
        self.load_current_image()
        
    def show_blurred_image(self):
        if self.current_image is None:
            return
            
        height, width = self.current_image.shape[:2]
        blur_size = max(1, self.blur_level // 2)
        if blur_size % 2 == 0:
            blur_size += 1
            
        blurred = cv2.GaussianBlur(self.current_image, (blur_size, blur_size), 0)
        cv2.imshow('Image Game', blurred)
        
    def run(self):
        self.countdown()
        self.load_random_image()
        
        last_update = time.time()
        
        while True:
            if not self.paused and time.time() - last_update >= 2:
                self.blur_level = max(1, self.blur_level - 10)
                last_update = time.time()
                
            self.show_blurred_image()
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
                
            if keyboard.is_pressed('space'):
                self.paused = not self.paused
                time.sleep(0.2)  # Prevent multiple toggles
                
            if keyboard.is_pressed('o'):
                cv2.imshow('Image Game', self.current_image)
                
            if keyboard.is_pressed('right'):
                self.load_next_image()
                time.sleep(0.2)
                
            if keyboard.is_pressed('left'):
                self.load_previous_image()
                time.sleep(0.2)
                
        cv2.destroyAllWindows()

def main():
    if len(sys.argv) != 2:
        print("Usage: python script.py <folder_path>")
        sys.exit(1)
        
    folder_path = sys.argv[1]
    if not os.path.isdir(folder_path):
        print("Invalid folder path!")
        sys.exit(1)
        
    game = ImageGame(folder_path)
    game.run()

if __name__ == "__main__":
    main()