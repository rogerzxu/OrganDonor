import pygame.image as PI
import math
import pygame.sprite as PS

HEALTH = "calcium.png"

class Power_up(PS.Sprite)
    image = None
    def __init__(self, filename, event_type, loc_x, loc_y):
        if not self.image:
            self.image = PI.load(filename).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.centerx = loc_x
        self.rect.centery = loc_y
