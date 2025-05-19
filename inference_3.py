from ultralytics import YOLO
import cv2
import requests
from picamera2 import Picamera2
from math import ceil
import pygame
from pygame.locals import *
from libcamera import Transform

def get_number(data_list):
    name_count = {}
    for item in data_list:
        name = item['name']
        name_count[name] = name_count.get(name, 0) + 1
    return name_count


def run():
    # Initialize Pygame
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("YOLO Object Detection")
    
    # Initialize camera
    cap = Picamera2()
    cap.configure(cap.create_preview_configuration(
        main={"format": 'RGB888', "size": (640, 480)},
        transform=Transform(hflip=False, vflip=True)
    ))
    cap.start()
    
    model = YOLO("inference.pt")
    
    counter = 0
    print("Script started")
    summ = {}
    clock = pygame.time.Clock()
    
    running = True
    while running:
        # Handle Pygame events
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
        
        # Read a frame from the video
        frame = cap.capture_array()
        
        # Run YOLO inference on the frame
        results = model(frame)
        counter += 1
        
        # Visualize the results on the frame
        annotated_frame = results[0].plot()
        
        # Convert frame for Pygame display
        annotated_frame = cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB)
        annotated_frame = cv2.transpose(annotated_frame)
        pygame_frame = pygame.surfarray.make_surface(annotated_frame)
        
        # Display the annotated frame
        screen.blit(pygame_frame, (0, 0))
        pygame.display.flip()
        
        # Count objects and send data periodically
        objects_in_frame = get_number(results[0].summary())
        for item, value in objects_in_frame.items():
            summ[item] = summ.get(item, 0) + value
            
        if counter == 4:
            data = {}
            for obj, value in summ.items():
                data.update({obj: ceil(value/4)})
            print('     data:', data)
            print('     summ:', summ)
            response = requests.post('http://127.0.0.1:8000/', json=data)
            counter = 0
            print('Status:', response.status_code)
            summ = {}
        
        clock.tick(30)  # Limit to 30 FPS

    # Release resources
    cap.stop()
    pygame.quit()

if __name__ == '__main__':
    run()