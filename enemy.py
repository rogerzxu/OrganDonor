import random as R
import pygame.sprite as PS
import pygame.image as PI
import pygame.mixer as PX
import math
import rocket

WIDTH = 800
HEIGHT = 600

ENEMY_VELOCITY  = 1
HIT_VELOCITY    = 20
GRAVITY         = 4000
HEIGHT          = 600
FIRERATE        = 1.5   #The higher this number, the slower the enemy shoots
SPEED_MODIFIER  = 3     #The higher this number, the slower the enemy moves
ROBOHEALTH      = 1
DOGHEALTH       = 1
VIRUSHEALTH     = 1
SHIPHEALTH = 5

class Enemy(PS.Sprite):
    IMAGES = None
    IMAGE = None
    CYCLE = 1.0
    def __init__(self, surf_width, surf_height, loc_x, loc_y, movement_range, movementy, id_num):
        self.time = 0.0
        self.firetime = 0.0
        # Set speed
        start_dir = R.randint(0,1)
        if start_dir == 0:
            self.moving_right = False
            self.moving_down = True
        else:
            self.moving_right = True
            self.moving_down = False
        
        self.vx = ENEMY_VELOCITY
        self.vy = ENEMY_VELOCITY

        self.surf_width = surf_width
        self.surf_height = surf_height

        self.movement_range = movement_range
        self.movementy = movementy
        
        self.position = movement_range/2
        self.positiony = movementy/2
        
        self.counter = 0
        self.countery = 0

        self.id_num = id_num
  
        #load image once
        PS.Sprite.__init__(self) 
        if not Enemy.IMAGES:
          self.load_images()
        self.frame = 0
        self.IMAGE = self.IMAGES[self.frame]
        
        self.image = self.IMAGE
        self.rect = self.image.get_rect()
        
        #Randomly position enemy
        self.rect.centery = loc_y
        self.rect.centerx = loc_x

        self.grounded = False

        #initialize rockets
        self.fired = True

        self.KILL = False
        
    def get_centerx(self):
        return self.rect.centerx

    def get_centery(self):
        return self.rect.centery

    def get_head(self):
        return self.rect.centery - self.rect.height / 2

    def get_foot(self):
        return self.rect.centery + self.rect.height / 2

    def get_rit(self):
        return self.rect.centerx + self.rect.width / 2
    
    def get_lef(self):
        return self.rect.centerx - self.rect.width / 2

    def get_rocket(self):
        return self.rect.centery - 15

    def get_dead(self):
        return self.KILL

    def get_id_num(self):
        return self.id_num

    def set_x(self, x):
        self.rect.centerx = x

    def set_y(self, y):
        self.rect.centery = y

    def update_image(self):
        self.image = self.IMAGES[self.frame]

    def update_image_neg(self):
        self.image = self.NEG_IMAGES[self.frame]

    def stop(self, set_x_position):
        self.rect.centerx = set_x_position - self.rect.width / 2

    def stopy(self, set_y_position):
        self.rect.centery = set_y_position - self.rect.height / 2

    def land(self, set_grounded, set_y_position = 0):
        self.grounded = set_grounded
        if set_grounded:
            self.rect.centery = set_y_position - self.rect.height / 2 + 1

    def is_fired(self):
        return self.fired

    def shot_rocket(self):
        self.fired = True

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

    def die(self):
        if self.KILL:
            self.kill()

    def hurt(self):
        self.health -= 1
        if self.health < 1:
            self.kill()

    def player_detection(self, player_group):
       	hit_players = PS.spritecollide(self, player_group, False)
	if hit_players:
		for this_player in hit_players:
                    self.vx = ENEMY_VELOCITY
                    #Enemy reactions to player contact can cause bugs
                    self.vx = HIT_VELOCITY
                    if self.get_rit() > this_player.get_rit():
                            self.moving_right = True
                    else:
                            self.moving_right = False
	else:
		self.vx = ENEMY_VELOCITY 

    def check_firetime(self, time):
        self.firetime = self.firetime + time
        if self.firetime > FIRERATE:
            self.fired = False
            self.firetime = 0

    def load_images(self):
        pass

    def update(self):
        pass

    def rockettype(self):
        pass

    def add_rocket(self):
        pass

class Walkshoot(Enemy):
    def update(self, time, platform_group, player_group):
        if self.rect.centerx <= WIDTH + self.rect.width / 2 and \
           self.rect.centerx >= -1 * self.rect.width / 2 and \
           self.rect.centery <= HEIGHT + self.rect.height / 2 and \
           self.rect.centery >= -1 * self.rect.height / 2:
            self.die()
        
            #collision detection player
            self.player_detection(player_group)

            #Random direction
            if self.moving_right and self.grounded: #and self.rect.centerx < self.surf_width - self.rect.width/2:
                if self.counter % SPEED_MODIFIER == 0:
                    self.rect.centerx += math.ceil(self.vx * time)
                    self.position += math.ceil(self.vx * time)
                self.counter += 1

                #Reset counter so it doesn't get huge out of hand
                if self.counter == SPEED_MODIFIER:
                    self.counter = 0

                #Range-based collision detection
                if self.position >= self.movement_range:
                    self.stop(self.rect.centerx + self.rect.width / 2)
                    self.moving_right = False

                #Check rate of fire
                self.check_firetime(time)

                if self.grounded:
                    self.time = self.time + time             
                    if self.time > self.CYCLE:
                        self.time = 0.0
                    frame = int(self.time / (self.CYCLE / len(self.IMAGES)))
                    if frame != self.frame:
                        self.frame = frame
                        self.update_image_neg()

            elif self.moving_right and self.grounded:
                #self.stop(self.surf_width - self.rect.width/2)
                self.moving_right = False

            elif not self.moving_right and self.grounded: #and self.rect.centerx > self.rect.width/2:
                if self.counter % SPEED_MODIFIER == 0:
                    self.rect.centerx -= math.ceil(self.vx * time)
                    self.position -= math.ceil(self.vx * time)
                self.counter += 1

                #Reset counter so it doesn't get huge out of hand
                if self.counter == SPEED_MODIFIER:
                    self.counter = 0

                #Range-based collision detection
                if self.position <= 0:
                    self.stop(self.rect.centerx + self.rect.width / 2)
                    self.moving_right = True

                #Check rate of fire
                self.check_firetime(time)

                if self.grounded:
                    self.time = self.time + time        
                    if self.time > self.CYCLE:
                        self.time = 0.0
                    frame = int(self.time / (self.CYCLE / len(self.IMAGES)))
                    if frame != self.frame:
                        self.frame = frame
                        self.update_image()

            elif not self.moving_right and self.grounded:
               # self.stop(self.rect.width/2)
                self.moving_right = True

            if self.grounded or self.get_head() > HEIGHT:
                self.vy = 0
            else:
                self.time = self.time + time
                if self.time > self.CYCLE:
                    self.time = 0.0
                self.vy += GRAVITY * time

            self.rect.centery += self.vy * time

            #Collision detection y-axis
            hit_platforms = PS.spritecollide(self, platform_group, False)
            
            if hit_platforms:
                  for this_platform in hit_platforms:
                      if  self.rect.centery > this_platform.get_top() or self.vy < 0:
                          self.land(False)
                      else:
                          self.land(True, this_platform.get_top())

            else:
                self.land(False)


            if self.health < 1:
                self.KILL = True

class Flyshoot(Enemy):
  
  def update(self, time, platform_group, player_group):
    if self.rect.centerx <= WIDTH + self.rect.width / 2 and \
           self.rect.centerx >= -1 * self.rect.width / 2 and \
           self.rect.centery <= HEIGHT + self.rect.height / 2 and \
           self.rect.centery >= -1 * self.rect.height / 2:
        self.die()
        self.player_detection(player_group)

        #Check rate of fire
        self.check_firetime(time)
        #Right movement
        if self.moving_right:
            if self.counter % SPEED_MODIFIER == 0:
                self.rect.centerx += math.ceil(self.vx * time)
                self.position += math.ceil(self.vx * time)
            self.counter += 1

            #Reset counter so it doesn't get huge out of hand
            if self.counter == SPEED_MODIFIER:
                self.counter = 0

            #Range-based collision detection
            if self.position >= self.movement_range:
                self.stop(self.rect.centerx + self.rect.width / 2)
                self.moving_right = False

            self.time = self.time + time             
            if self.time > self.CYCLE:
                self.time = 0.0
            frame = int(self.time / (self.CYCLE / len(self.IMAGES)))
            if frame != self.frame:
                self.frame = frame
                self.update_image_neg()

        #Left movement
        elif not self.moving_right:
            if self.counter % SPEED_MODIFIER == 0:
                self.rect.centerx -= math.ceil(self.vx * time)
                self.position -= math.ceil(self.vx * time)
            self.counter += 1

            #Reset counter so it doesn't get huge out of hand
            if self.counter == SPEED_MODIFIER:
                self.counter = 0

            #Range-based collision detection
            if self.position <= 0:
                self.stop(self.rect.centerx + self.rect.width / 2)
                self.moving_right = True

            self.time = self.time + time
            if self.time > self.CYCLE:
                self.time = 0.0
            frame = int(self.time / (self.CYCLE / len(self.IMAGES)))
            if frame != self.frame:
                self.frame = -frame
                self.update_image()

        #Vertical Movement
        if self.moving_down:
            if self.countery % SPEED_MODIFIER == 0:
                self.rect.centery += math.ceil(self.vy * time)
                self.positiony += math.ceil(self.vy * time)
            self.countery += 1

            #Reset counter so it doesn't get huge out of hand
            if self.countery == SPEED_MODIFIER:
                self.countery = 0

            #Range-based collision detection
            if self.positiony >= self.movementy:
                self.stopy(self.rect.centery + self.rect.height / 2)
                self.moving_down = False
        else:
            if self.countery % SPEED_MODIFIER == 0:
                self.rect.centery -= math.ceil(self.vy * time)
                self.positiony -= math.ceil(self.vy * time)
            self.countery += 1

            #Reset counter so it doesn't get huge out of hand
            if self.countery == SPEED_MODIFIER:
                self.countery = 0

            #Range-based collision detection
            if self.positiony <= 0:
                self.stopy(self.rect.centery + self.rect.height / 2)
                self.moving_down = True

        if self.health < 1:
            self.KILL = True
            
class Walkmelee(Enemy):
    def update(self, time, platform_group, player_group):
        if self.rect.centerx <= WIDTH + self.rect.width / 2 and \
           self.rect.centerx >= -1 * self.rect.width / 2 and \
           self.rect.centery <= HEIGHT + self.rect.height / 2 and \
           self.rect.centery >= -1 * self.rect.height / 2:
            self.fired = True
            self.die()
        
            #collision detection player
            self.player_detection(player_group)

            #Random direction
            if self.moving_right and self.grounded: #and self.rect.centerx < self.surf_width - self.rect.width/2:
                if self.counter % SPEED_MODIFIER == 0:
                    self.rect.centerx += math.ceil(self.vx * time)
                    self.position += math.ceil(self.vx * time)
                self.counter += 1

                #Reset counter so it doesn't get huge out of hand
                if self.counter == SPEED_MODIFIER:
                    self.counter = 0

                #Range-based collision detection
                if self.position >= self.movement_range:
                    self.stop(self.rect.centerx + self.rect.width / 2)
                    self.moving_right = False

                if self.grounded:
                    self.time = self.time + time             
                    if self.time > self.CYCLE:
                        self.time = 0.0
                    frame = int(self.time / (self.CYCLE / len(self.IMAGES)))
                    if frame != self.frame:
                        self.frame = frame
                        self.update_image_neg()

            elif self.moving_right and self.grounded:
                #self.stop(self.surf_width - self.rect.width/2)
                self.moving_right = False

            elif not self.moving_right and self.grounded: #and self.rect.centerx > self.rect.width/2:
                if self.counter % SPEED_MODIFIER == 0:
                    self.rect.centerx -= math.ceil(self.vx * time)
                    self.position -= math.ceil(self.vx * time)
                self.counter += 1

                #Reset counter so it doesn't get huge out of hand
                if self.counter == SPEED_MODIFIER:
                    self.counter = 0

                #Range-based collision detection
                if self.position <= 0:
                    self.stop(self.rect.centerx + self.rect.width / 2)
                    self.moving_right = True


                if self.grounded:
                    self.time = self.time + time        
                    if self.time > self.CYCLE:
                        self.time = 0.0
                    frame = int(self.time / (self.CYCLE / len(self.IMAGES)))
                    if frame != self.frame:
                        self.frame = frame
                        self.update_image()

            elif not self.moving_right and self.grounded:
               # self.stop(self.rect.width/2)
                self.moving_right = True

            if self.grounded or self.get_head() > HEIGHT:
                self.vy = 0
            else:
                self.time = self.time + time
                if self.time > self.CYCLE:
                    self.time = 0.0
                self.vy += GRAVITY * time

            self.rect.centery += self.vy * time

            #Collision detection y-axis
            hit_platforms = PS.spritecollide(self, platform_group, False)
            
            if hit_platforms:
                  for this_platform in hit_platforms:
                      if  self.rect.centery > this_platform.get_top() or self.vy < 0:
                          self.land(False)
                      else:
                          self.land(True, this_platform.get_top())

            else:
                self.land(False)


            if self.health < 1:
                self.KILL = True   

class Roboto(Walkshoot):
    def load_images(self):
        self.health = ROBOHEALTH
        self.IMAGES = []
        self.NEG_IMAGES = []
        for i in range(1, 5):
            walkr = "enemy_animation/roboto/" + str(i) + ".png"
            self.IMAGES.append(PI.load(walkr).convert_alpha())
            walkl = "enemy_animation/roboto/-" + str(i) + ".png"
            self.NEG_IMAGES.append(PI.load(walkl).convert_alpha())

    def add_rocket(self, volume):
        return rocket.Rocket(self.surf_width, self.surf_height, self.get_lef(), self.get_rocket(), self.moving_right, volume)

class Virus (Flyshoot):
    def load_images(self):
        self.health = VIRUSHEALTH
        self.IMAGES = []
        self.NEG_IMAGES = []
        for i in range(1, 5):
            walkr = "enemy_animation/virus/" + str(i) + ".png"
            self.IMAGES.append(PI.load(walkr).convert_alpha())
            walkl = "enemy_animation/virus/-" + str(i) + ".png"
            self.NEG_IMAGES.append(PI.load(walkl).convert_alpha())

    def add_rocket(self, volume):
        return rocket.Virusbubble(self.surf_width, self.surf_height, self.get_lef(), self.get_rocket(), self.moving_right, volume)
        
class Virus_Melee(Virus):
    def add_rocket(self, volume):
        return

class Spaceship (Flyshoot):
    def load_images(self):
        self.health = SHIPHEALTH
        self.IMAGES = []
        self.NEG_IMAGES = []
        walkr = "enemy_animation/spaceship/1.png"
        walkl = "enemy_animation/spaceship/-1.png"
        self.IMAGES.append(PI.load(walkr).convert_alpha())
        self.NEG_IMAGES.append(PI.load(walkl).convert_alpha())
        
    def add_rocket(self, volume):
        return rocket.Laser(self.surf_width, self.surf_height, self.get_lef(), self.get_rocket(), self.moving_right, volume)
    
    def hurt(self):
        self.health -= 1
        if self.health < 1:
            self.kill()
            
class Sparky (Walkmelee):
    def load_images(self):
        self.health = DOGHEALTH
        self.IMAGES = []
        self.NEG_IMAGES = []
        for i in range (1, 6):
            walkr = "enemy_animation/sparky/" + str(i) + ".png"
            self.IMAGES.append(PI.load(walkr).convert_alpha())
            walkl = "enemy_animation/sparky/-" + str(i) + ".png"
            self.NEG_IMAGES.append(PI.load(walkl).convert_alpha())

