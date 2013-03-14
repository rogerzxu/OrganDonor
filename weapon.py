import sys as SYS
import pygame as PG
import pygame.display as PDI
import pygame.event as PE
import pygame.font as PF
import pygame.sprite as PS
import pygame.image as PI
import pygame.time as PT
import pygame.color as PC
import pygame.mixer as PX
import math

class Weapon(PS.Sprite):
    def __init__(self):
        pass
    def damage(self):
        pass
    def num_attacks(self):
        pass
    def attack(self):
        pass
        
class Hammer(Weapon):
    DAMAGE = 1
    ATTACKS = 10
    IMAGE = None
    def __init__(self):
        Weapon.__init__(self)
    def damage(self):
        return self.DAMAGE
    def num_attacks(self):
        return self.ATTACKS
    def attack(self):
        self.ATTACKS = self.ATTACKS - 1