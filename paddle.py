import settings
import pygame
pygame.init()


class Paddle:
    COLOR = settings.WHITE

    def __init__(self, x, y, width, height):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.width = width
        self.height = height

    def draw(self, win):
        pygame.draw.rect(win, self.COLOR, (self.x, self.y, self.width, self.height))

    def move(self, up=True):
        if up:
            self.y -= settings.VEL
        else:
            self.y += settings.VEL
    
    def reset(self):
        self.x = self.original_x
        self.y = self.original_y