import pygame.sprite as PS
import pygame.image as PI
import pygame.mixer as PM
import math

ROCKET_VELOCITY = 300

class Projectile(PS.Sprite):
    IMAGE = None
    CYCLE = 1.0
    def __init__(self):
        pass
    
    def get_head(self):
        return self.rect.centery - self.rect.height / 2

    def get_foot(self):
        return self.rect.centery + self.rect.height / 2

    def get_rit(self):
        return self.rect.centerx + self.rect.width / 2
    
    def get_lef(self):
        return self.rect.centerx - self.rect.width / 2
 
    def explode(self):
        self.kill()
    
    def get_centerx(self):
        return self.rect.centerx

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

    def update(self, time, player_group):
        if self.KILL:
            self.explode()
        hit_players = PS.spritecollide(self, player_group, False)

        if hit_players or self.get_lef() > self.surf_width or self.get_rit() < 0:
            self.KILL = True
            if hit_players:
                self.sound.play()

        if self.moving_right:
            self.image = self.IMAGE_NEG
            self.rect.centerx += math.ceil(self.vx * time)
        else:
            self.rect.centerx -= math.ceil(self.vx * time)


class Rocket(Projectile):
    def __init__(self, surf_width, surf_height, loc_x, loc_y, direction, volume):
        self.time = 0.0
        self.volume = volume

        #set speed
        self.vx = ROCKET_VELOCITY

        self.surf_width = surf_width
        self.surf_height = surf_height

        #load image
        PS.Sprite.__init__(self)
        if not Rocket.IMAGE:
            self.IMAGE = PI.load("rocket.png").convert_alpha()
            self.IMAGE_NEG = PI.load("rocket_neg.png").convert_alpha()
        self.image = self.IMAGE
        self.rect = self.image.get_rect()

        #position rocket
        self.rect.centery = loc_y
        self.rect.centerx = loc_x

        self.sound = PM.Sound("Sounds/effects/rocket.ogg")
        self.sound.set_volume(self.volume)
        
        self.KILL = False
        self.moving_right = direction

            
class  Virusbubble(Projectile):   
    def __init__(self, surf_width, surf_height, loc_x, loc_y, direction, volume):
        self.time = 0.0
        self.volume = volume

        #set speed
        self.vx = ROCKET_VELOCITY

        self.surf_width = surf_width
        self.surf_height = surf_height

        #load image
        PS.Sprite.__init__(self)
        if not Virusbubble.IMAGE:
            self.IMAGE = PI.load("enemy_animation/virus/projectile.png").convert_alpha()
            self.IMAGE_NEG = PI.load("enemy_animation/virus/projectile_neg.png").convert_alpha()
        self.image = self.IMAGE
        self.rect = self.image.get_rect()

        #position rocket
        self.rect.centery = loc_y
        self.rect.centerx = loc_x

        self.sound = PM.Sound("Sounds/effects/virus_attack.ogg")
        self.sound.set_volume(self.volume)

        self.KILL = False
        self.moving_right = direction

class  Laser(Projectile):   
    def __init__(self, surf_width, surf_height, loc_x, loc_y, direction, volume):
        self.time = 0.0
        self.volume = volume

        #set speed
        self.vx = ROCKET_VELOCITY

        self.surf_width = surf_width
        self.surf_height = surf_height

        #load image
        PS.Sprite.__init__(self)
        if not Virusbubble.IMAGE:
            self.IMAGE = PI.load("enemy_animation/spaceship/laser.png").convert_alpha()
            self.IMAGE_NEG = PI.load("enemy_animation/spaceship/laser.png").convert_alpha()
        self.image = self.IMAGE
        self.rect = self.image.get_rect()

        #position rocket
        self.rect.centery = loc_y
        self.rect.centerx = loc_x

        self.sound = PM.Sound("Sounds/effects/virus_attack.ogg")
        self.sound.set_volume(self.volume)

        self.KILL = False
        self.moving_right = direction
