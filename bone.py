import pygame.sprite as PS
import pygame.image as PI
import pygame.mixer as PM
import math

MAX_HEALTH = 5

class Powerup(PS.Sprite):
    IMAGE = None
    CYCLE = 1.0
    def __init__(self, surf_width, surf_height, loc_x, loc_y):
        self.time = 0.0

        self.surf_width = surf_width
        self.surf_height = surf_height

        #load image
        self.load_images()

        #position powerup
        self.rect.centery = loc_y
        self.rect.centerx = loc_x

        self.KILL = False

    def get_head(self):
        return self.rect.centery - self.rect.height / 2

    def get_foot(self):
        return self.rect.centery + self.rect.height / 2

    def get_rit(self):
        return self.rect.centerx + self.rect.width / 2
    
    def get_lef(self):
        return self.rect.centerx - self.rect.width / 2

    def load_images(self):
        pass

    def is_bone(self):
        return self.bone

    def explode(self):
        self.kill()

    def react(self, player):
        pass

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

    def update(self, time, player_group, platform_group):
        if self.KILL:
            self.explode()
        hit_players = PS.spritecollide(self, player_group, False)
        hit_platforms = PS.spritecollide(self, platform_group, False)

        if hit_players:
            for this_player in hit_players:
                self.react(this_player)

        if hit_platforms:
            for this_platform in hit_platforms:
                self.rect.centery = (this_platform.get_top() - self.rect.height/4)

class Bone(Powerup):
    def load_images(self):
        PS.Sprite.__init__(self)
        if not Bone.IMAGE:
            self.IMAGE = PI.load("UI/bones/1.png").convert_alpha()
        self.image = self.IMAGE
        self.rect = self.image.get_rect()
        self.bone = True

    def react(self, player):
        self.KILL = True

class Calcium(Powerup):
    def load_images(self):
        PS.Sprite.__init__(self)
        if not Bone.IMAGE:
            self.IMAGE = PI.load("tools/calcium.png").convert_alpha()
        self.image = self.IMAGE
        self.rect = self.image.get_rect()
        self.bone = False

    def react(self, player):
        if player.get_health() < MAX_HEALTH:
            self.KILL = True

