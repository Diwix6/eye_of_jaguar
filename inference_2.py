import cv2
from picamera2 import Picamera2
import pygame
from pygame.locals import *
from libcamera import Transform

def run():
    # Инициализация Pygame
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("Raspberry Pi Camera Feed")
    
    # Инициализация камеры
    picam2 = Picamera2()
    picam2.configure(picam2.create_preview_configuration(main={"format": 'RGB888', "size": (640, 480)}, transform=Transform(hflip=False, vflip=True)))  # Переворачиваем по горизонтали и вертикали

    picam2.start()
    
    clock = pygame.time.Clock()  # Для контроля FPS
    
    running = True
    while running:
        # Обработка событий Pygame
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
        
        # Получение кадра с камеры
        frame = picam2.capture_array()
        
        # Конвертация кадра для Pygame
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.transpose(frame)
        pygame_frame = pygame.surfarray.make_surface(frame)
        
        # Отображение кадра
        screen.blit(pygame_frame, (0, 0))
        pygame.display.flip()
        
        clock.tick(30)  # Ограничение FPS до 30 кадров в секунду
    
    # Освобождение ресурсов
    picam2.stop()
    pygame.quit()

if __name__ == '__main__':
    run()