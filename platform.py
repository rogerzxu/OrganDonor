import pygame.sprite as PS
import pygame.image as PI
import math

SPEED_MODIFIER  = 3     #The higher this number, the slower the platform moves
PLATFORM_SPEED = 1

class Platform(PS.Sprite):
    def __init__(self, surf_width, surf_height, loc_x, loc_y, movementx_pos, movementx_neg, movementy_pos, movementy_neg, idnum):

        self.iswall = False

        self.lasttime = 0

        self.idnum = idnum

        self.moving_right = False
        self.moving_down = False

        self.freeze = False

        self.movement_range_pos = movementx_pos
        self.movement_range_neg = movementx_neg
        self.movementy_pos = movementy_pos
        self.movementy_neg = movementy_neg

        self.position_pos = self.movement_range_pos/2
        self.position_neg = self.movement_range_neg/2
        self.positiony_pos = self.movementy_pos/2
        self.positiony_neg = self.movementy_neg/2
        
        self.vx = PLATFORM_SPEED
        self.vy = PLATFORM_SPEED
        
        self.surf_width = surf_width
        self.surf_height = surf_height

        self.counter = 0
        self.countery = 0

        self.swingx = False
        self.swing = False
  
        #load image once
        PS.Sprite.__init__(self)
        self.image = self.load_image()
        self.rect = self.image.get_rect()

        self.rect.centerx = loc_x
        self.rect.centery = loc_y

    def load_image(self):
        return PI.load("Levels/platform.png").convert_alpha()

    def stop(self, set_x_position):
        self.rect.centerx = set_x_position - self.rect.width / 2

    def stopy(self, set_y_position):
        self.rect.centery = set_y_position - self.rect.height / 2

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

    def get_idnum(self):
        return self.idnum

    def set_x(self, x_loc):
        self.rect.centerx = x_loc

    def set_y(self, y_loc):
        self.rect.centery = y_loc

    def set_move_x_pos(self, range_x):
        self.movement_range_pos = range_x
        self.position_pos = range_x/2

    def set_move_x_neg(self, range_x):
        self.movement_range_neg = range_x
        self.position_neg = range_x/2

    def set_move_y_pos(self, range_y):
        self.movementy_pos = range_y
        self.positiony_pos = range_y/2

    def set_move_y_neg(self, range_y):
        self.movementy_neg = range_y
        self.positiony_neg = range_y/2

    def check_movement(self):
        if self.movement_range_pos > 0 and self.movement_range_neg <= 0:
            self.moving_right = True

        if self.movementy_pos > 0 and self.movementy_neg <= 0:
            self.moving_down = True

    def set_freeze(self, set_val = False):
        self.freeze = set_val

    def is_moving_x(self):
        if self.movement_range_pos > 0 or self.movement_range_neg > 0:
            return True
        else:
            return False

    def is_moving_y(self):
        if self.movementy_pos > 0 or self.movementy_neg > 0:
            return True
        else:
            return False
        
    def get_move_down(self):
        return self.moving_down

    def get_move_right(self):
        return self.moving_right

    def get_time(self):
        return self.lasttime

    def speedx(self):
        return self.vx

    def speedy(self):
        return self.vy

    def is_wall(self):
        return self.iswall

    def get_counter(self):
        return self.counter % SPEED_MODIFIER == 0

    def get_countery(self):
        return self.countery % SPEED_MODIFIER == 0

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

    def update(self, time):
        if not self.freeze:
            
            self.lasttime = time 
            #Right movement
            if self.moving_right and self.position_neg < self.movement_range_neg/2 and self.swingx:
                if self.counter % SPEED_MODIFIER == 0:
                    self.rect.centerx += math.ceil(self.vx * time)
                    self.position_neg += math.ceil(self.vx * time)
                self.counter += 1
                
                if self.movement_range_pos <= 0 and self.position_neg >= self.movement_range_neg/2:
                    self.stop(self.rect.centerx + self.rect.width / 2)
                    self.moving_right = False
                
            elif self.moving_right and self.movement_range_pos > 0:
                self.swing = False
                if self.counter % SPEED_MODIFIER == 0:
                    self.rect.centerx += math.ceil(self.vx * time)
                    self.position_pos -= math.ceil(self.vx * time)
                self.counter += 1

                #Range-based collision detection
                if self.position_pos <= 0:
                    self.stop(self.rect.centerx + self.rect.width / 2)
                    self.moving_right = False
                    self.swingx = True

            #Left movement
            elif (not self.moving_right) and self.position_pos < self.movement_range_pos / 2 and self.swingx:
                if self.counter % SPEED_MODIFIER == 0:
                    self.rect.centerx -= math.ceil(self.vx * time)
                    self.position_pos += math.ceil(self.vx * time)
                self.counter += 1

                if self.movement_range_neg <= 0 and self.position_pos >= self.movement_range_pos / 2:
                    self.stop(self.rect.centerx + self.rect.width / 2)
                    self.moving_right = True

            elif (not self.moving_right) and self.movement_range_neg > 0:
                if self.counter % SPEED_MODIFIER == 0:
                    self.rect.centerx -= math.ceil(self.vx * time)
                    self.position_neg -= math.ceil(self.vx * time)
                self.counter += 1

                #Range-based collision detection
                if self.position_neg <= 0:
                    self.stop(self.rect.centerx + self.rect.width / 2)
                    self.moving_right = True
                    self.swingx = True
                    
            #Reset counter so it doesn't get huge out of hand
            if self.counter == SPEED_MODIFIER:
                self.counter == 0

            #Vertical Movement
            #Downward movement

            if self.moving_down and self.positiony_neg < self.movementy_neg/2 and self.swing:
                if self.countery % SPEED_MODIFIER == 0:
                    self.rect.centery += math.ceil(self.vy * time)
                    self.positiony_neg += math.ceil(self.vy * time)
                self.countery += 1

                if self.movementy_pos <= 0 and self.positiony_neg >= self.movementy_neg/2:
                    self.stopy(self.rect.centery + self.rect.height / 2)
                    self.moving_down = False
                
            elif self.moving_down and self.movementy_pos > 0:
                self.swing = False
                if self.countery % SPEED_MODIFIER == 0:
                    self.rect.centery += math.ceil(self.vy * time)
                    self.positiony_pos -= math.ceil(self.vy * time)
                self.countery += 1

                #Range-based collision detection
                if self.positiony_pos <= 0:
                    self.stopy(self.rect.centery + self.rect.height / 2)
                    self.moving_down = False
                    self.swing = True

            #Upward Movement
            elif (not self.moving_down) and self.positiony_pos < self.movementy_pos/2 and self.swing:
                if self.countery % SPEED_MODIFIER == 0:
                    self.rect.centery -= math.ceil(self.vy * time)
                    self.positiony_pos += math.ceil(self.vy * time)
                self.countery += 1

                if self.movementy_neg <= 0 and self.positiony_pos >= self.movementy_pos/2:
                    self.stopy(self.rect.centery + self.rect.height / 2)
                    self.moving_down = True
                
            elif (not self.moving_down) and self.movementy_neg > 0:
                self.swing = False
                if self.countery % SPEED_MODIFIER == 0:
                    self.rect.centery -= math.ceil(self.vy * time)
                    self.positiony_neg -= math.ceil(self.vy * time)
                self.countery += 1

                #Range-based collision detection
                if self.positiony_neg <= 0:
                    self.stopy(self.rect.centery + self.rect.height / 2)
                    self.moving_down = True
                    self.swing = True

            if self.countery == SPEED_MODIFIER:
                self.countery = 0
                
class Small_Platform(Platform):

    def load_image(self):
        return PI.load("Levels/platform_small.png").convert_alpha()

class Small_Wall(Platform):

    def load_image(self):
        self.iswall = True
        return PI.load("Levels/wall_small.png").convert_alpha()

class Large_Platform(Platform):

    def load_image(self):
        return PI.load("Levels/platform_large.png").convert_alpha()

class Large_Wall(Platform):

    def load_image(self):
        self.iswall = True
        return PI.load("Levels/wall_large.png").convert_alpha()

class Long_Platform(Platform):

    def load_image(self):
        return PI.load("Levels/platform_long.png").convert_alpha()

class Long_Wall(Platform):

    def load_image(self):
        self.iswall = True
        return PI.load("Levels/wall_long.png").convert_alpha()

class Mini_Platform(Platform):

    def load_image(self):
        return PI.load("Levels/platform_mini.png").convert_alpha()

class Bridge(Platform):

    def load_image(self):
        return PI.load("tools/bridge.png").convert_alpha()

class Fake_Bridge(Platform):

    def load_image(self):
        return PI.load("tools/fake_bridge.png").convert_alpha()

