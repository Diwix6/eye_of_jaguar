import cv2
import numpy as np
from picamera2 import Picamera2




cam = Picamera2()

cam.start()


while True:
        frame = cam.capture_array()

        cv2.imshow('f', frame)