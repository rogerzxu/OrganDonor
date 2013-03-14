import pygame.image as PI
import pygame.sprite as PS
import math

class Ladder(PS.Sprite):
    def __init__(self, surf_width, surf_height, loc_x, loc_y):

        self.surf_width = surf_width
        self.surf_height = surf_height

        #load image once
        PS.Sprite.__init__(self)
        self.image = self.load_image()
        self.rect = self.image.get_rect()

        self.rect.centerx = loc_x
        self.rect.centery = loc_y - self.rect.height/2

    def load_image(self):
        return PI.load("tools/ladder.png").convert_alpha()

    def get_top(self):
        return self.rect.centery - self.rect.height / 2

    def get_bot(self):
        return self.rect.centery + self.rect.height / 2

    def get_rit(self):
        return self.rect.centerx + self.rect.width / 2 

    def get_lef(self):
        return self.rect.centerx - self.rect.width / 2 

    def get_center(self):
        return self.rect.centerx 

    def get_centery(self):
        return self.rect.centery

    def scroll(self, dx, dy):
        if dx < 0:
            dx = math.floor(dx)
        elif dx > 0:
            dx = math.ceil(dx)
        self.rect.centerx -= dx

        if dy < 0:
            dy = math.floor(dy)
        elif dy > 0:
            dy = math.ceil(dy)
        self.rect.centery -= dy

class Fake_Ladder(Ladder):
    def load_image(self):
        return PI.load("tools/fake_ladder.png").convert_alpha()
