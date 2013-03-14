import pygame.sprite as PS
import pygame.image as PI
import pygame.mixer as PM
import math
import weapon
import trigger

#Velocities
PLAYER_VELOCITY      = 100
JUMP_VEL             = -550
GRAVITY              = 1700
TERMINAL_VELOCITY    = 1000
HIT_VELOCITY 	     = 20000

#Sprite relative collision modifiers
COLLISION_MODIFIER   = 10
FEET                 = 12

#Deadzone boundaries
LEFT_DEADZONE_BOUND  = 390
RIGHT_DEADZONE_BOUND = 410
LOWER_DEADZONE_BOUND = 350
UPPER_DEADZONE_BOUND = 200
CENTER_X = (LEFT_DEADZONE_BOUND + RIGHT_DEADZONE_BOUND) / 2
CENTER_Y = (LOWER_DEADZONE_BOUND + UPPER_DEADZONE_BOUND) / 2

#Item indices
INVALID_WEAPON_INDEX = -1
HAMMER_INDEX         = 0
LADDER_INDEX         = 1
BRIDGE_INDEX         = 2
MAKE_WEAPON_INDEX    = 3
CANCEL_WEAPON_INDEX  = 4

#Item costs
HAMMER_COST          = 2
LADDER_COST          = 1
BRIDGE_COST          = 3

#Hammer attacks
MAX_HAMMER_ATTACKS   = 5

#Player health
MAX_HEALTH           = 5
MAX_CONTINUES        = 3
STARTING_BONES       = 0

#Event trigger types
NULL_TRIG    = -1
KILL         = 0
WIN          = 1
CHECKPOINT   = 11
PITFALL_TRIG = 12
LOAD_JUNK    = 13

#Scroll directions
LEFT    = -1
RIGHT   = 1
UP      = -1
DOWN    = 1
NEUTRAL = 0


class Player(PS.Sprite):
    #Initialize image once
    IMAGES = None
    IMAGE = None
    WINNER = False
    CYCLE = 1.0
    DEATHCYCLE = 2.0
    ATTCYCLE = .5
    CROUCH_CYCLE = .2
    CWALK_CYCLE = .5
    JUMP_CYCLE = 1.4
    IMMUNITY = 1.5
    COOLDOWN = 0.0
	
    def __init__(self, surf_width, surf_height, volume, level_file):
        PS.Sprite.__init__(self)
        self.volume = volume
        self.onladder = False
        self.weapons = []
        self.weaponIndex = -1
        self.load_hammer()
        if not Player.IMAGES:
            self.load_images()
			
        self.load_sounds()
		
        self.time = 0.0
        self.frame = 0
        
        self.dtime = 0.0
        self.dframe = 0
        
        self.atttime = 0.0
        self.attframe = 0
        self.attacking = False
        self.numAttacks = MAX_HAMMER_ATTACKS
        
        self.crouching = False
        self.cframe = 0
        self.ctime = 0.0
        self.cwalk_frame = 0
        self.cwalk_time = 0.0
        self.immunity = 1

        self.using = False
        
        self.finishedDie = False
        
        self.IMAGE = self.IMAGES[self.frame]
        
        self.image = self.IMAGE
        self.temp_image = None
        
        self.rect = self.image.get_rect()
        self.sound = None
        self.surf_height = surf_height
        self.surf_width = surf_width

        self.position_tool = False

        #Load start location and place player and checkpoint
        self.start_pos = (0,0)

        self.load_start_location(level_file)
        self.last_check = self.start_pos

        self.rect.centerx = self.start_pos[0]
        self.rect.centery = self.start_pos[1]

        self.move_to_check = True
        
        #Declare speed
        self.speedx = PLAYER_VELOCITY
        self.speedy = PLAYER_VELOCITY

        self.grounded = False
        self.hor_scroll = 0
        self.ver_scroll = 0

        #Player's hit points
        self.HEALTH = MAX_HEALTH
        self.continues = MAX_CONTINUES
        self.bones = STARTING_BONES
        
        self.ALIVE = True
        self.touch_enemy = False

        self.immune = False
        self.immunetime = 0.0
        self.facingRight = True

        self.oldtool = -1

        self.level_event_group = []
        self.load_progress = 0

        self.cooling = False
    
    def load_sounds(self):
        self.JUMPSOUND = PM.Sound("Sounds/effects/jump.ogg")
        self.JUMPSOUND.set_volume(self.volume)
        self.FOOTSTEPS = []
        self.FOOTSTEPS.append(PM.Sound("Sounds/effects/Footsteps1.ogg"))
        self.FOOTSTEPS.append(PM.Sound("Sounds/effects/Footsteps2.ogg"))
        self.FOOTSTEPS.append(PM.Sound("Sounds/effects/Footsteps3.ogg"))
        self.HAMMERHIT = PM.Sound("Sounds/effects/hammer_hit.ogg")
        self.HAMMERHIT.set_volume(self.volume)
        self.TAKEDAMAGE = PM.Sound("Sounds/effects/take_damage.ogg")
        self.TAKEDAMAGE.set_volume(self.volume)
        self.SOUNDINDEX = 0
        self.CHECKSOUND = PM.Sound("Sounds/effects/check_point.ogg")
        self.CHECKSOUND.set_volume(self.volume)
        self.GOCHECK = PM.Sound("Sounds/effects/restart_from_check_point_noise.ogg")
        self.GOCHECK.set_volume(self.volume)
	
    def load_hammer(self):
        self.HAMMER_RIGHT = []
    	self.HAMMER_LEFT = []
    	self.HAMMER_JUMP_RIGHT = []
    	self.HAMMER_JUMP_LEFT = []
    	self.HAMMER_ATT_RIGHT = []
    	self.HAMMER_ATT_LEFT = []
    	for i in range(1, 7):
    	    hammerr1 = "skeleton_animation/walk_hammer/"+str(i)+".png"
    	    hammerl1 = "skeleton_animation/walk_hammer/-"+str(i)+".png"
    	    hammerj1 = "skeleton_animation/skeletal_jump_hammer/"+str(i)+".png"
    	    hammerjl1 = "skeleton_animation/skeletal_jump_hammer/-"+str(i)+".png"
    	    self.HAMMER_RIGHT.append(PI.load(hammerr1).convert_alpha())
    	    self.HAMMER_LEFT.append(PI.load(hammerl1).convert_alpha())
    	    self.HAMMER_JUMP_RIGHT.append(PI.load(hammerj1).convert_alpha())
    	    self.HAMMER_JUMP_LEFT.append(PI.load(hammerjl1).convert_alpha())
    	for i in range(1, 8):
            hammerar = "skeleton_animation/attack/"+str(i)+".png"
    	    hammeral = "skeleton_animation/attack/-"+str(i)+".png"
    	    self.HAMMER_ATT_RIGHT.append(PI.load(hammerar).convert_alpha())
    	    self.HAMMER_ATT_LEFT.append(PI.load(hammeral).convert_alpha())
    	
    def load_images(self):
    	self.IMAGES = []
    	self.NEG_IMAGES = []
    	self.JUMP = []
    	self.DIE = []
    	self.CROUCH = []
    	self.CROUCH_RIGHT = []
    	self.CROUCH_LEFT = []
    	self.RECOIL = []
    	self.RECOIL_HAMMER_RIGHT = []
    	self.RECOIL_HAMMER_LEFT = []
    	for i in range(1, 6):
    	    crouch = "skeleton_animation/crouch/"+str(i)+".png"
    	    self.CROUCH.append(PI.load(crouch).convert_alpha())
    	for i in range(1, 5):
    	    crouch_r = "skeleton_animation/crouch/walk/"+str(i)+".png"
    	    crouch_l = "skeleton_animation/crouch/walk/-"+str(i)+".png"
    	    self.CROUCH_RIGHT.append(PI.load(crouch_r).convert_alpha())
    	    self.CROUCH_LEFT.append(PI.load(crouch_l).convert_alpha())
        for i in range(1, 7):
    	    walkr = "skeleton_animation/walk/"+str(i)+".png"
    	    self.IMAGES.append(PI.load(walkr).convert_alpha())
    	    walkl = "skeleton_animation/walk/-"+str(i)+".png"
    	    self.NEG_IMAGES.append(PI.load(walkl).convert_alpha())
    	    jump = "skeleton_animation/skeletal_jump/"+str(i)+".png"
    	    self.JUMP.append(PI.load(jump).convert_alpha())
    	for n in range(1, 12):
    	    die = "skeleton_animation/death/"+str(n)+".png"
    	    self.DIE.append(PI.load(die).convert_alpha())
    	#normal recoil
    	normal = "skeleton_animation/recoil/1_normal.png"
    	inverse = "skeleton_animation/recoil/1_inverse.png"
    	self.RECOIL.append(PI.load(normal).convert_alpha())
    	self.RECOIL.append(PI.load(inverse).convert_alpha())
        #right_hammer recoil
    	normal = "skeleton_animation/recoil/r_hammer_normal.png"
    	inverse = "skeleton_animation/recoil/r_hammer_inverse.png"
    	self.RECOIL_HAMMER_RIGHT.append(PI.load(normal).convert_alpha())
    	self.RECOIL_HAMMER_RIGHT.append(PI.load(inverse).convert_alpha())
    	#left_hammer recoil
    	normal = "skeleton_animation/recoil/l_hammer_normal.png"
    	inverse = "skeleton_animation/recoil/l_hammer_inverse.png"
    	self.RECOIL_HAMMER_LEFT.append(PI.load(normal).convert_alpha())
    	self.RECOIL_HAMMER_LEFT.append(PI.load(inverse).convert_alpha())

    def load_start_location(self, filename):
        file = open(filename + ".txt")
        self.delimiter = '\n'

    	while 1:
            line = file.readline().rstrip(self.delimiter)
            if not line:
                break
            if line == "Start_Location":
                self.start_pos = int(file.readline().rstrip(self.delimiter)), \
                                 int(file.readline().rstrip(self.delimiter))
                if self.start_pos[0] > CENTER_X: self.start_pos = CENTER_X, self.start_pos[1]
                if self.start_pos[1] > CENTER_Y: self.start_pos = self.start_pos[0], CENTER_Y
                break
                
    
    def update_image(self):
        self.image = self.IMAGES[self.frame]
    def update_image_neg(self):
        self.image = self.NEG_IMAGES[self.frame]
    def update_image_jump(self):
        self.image = self.JUMP[self.frame]
    def update_hammer_left(self):
        self.image = self.HAMMER_LEFT[self.frame]
    def update_hammer_right(self):
        self.image = self.HAMMER_RIGHT[self.frame]
    def update_hammer_jump_right(self):
        self.image = self.HAMMER_JUMP_RIGHT[self.frame]
    def update_hammer_jump_left(self):
        self.image = self.HAMMER_JUMP_LEFT[self.frame]
    def update_image_die(self):
        self.image = self.DIE[self.dframe]
    def update_hammer_att_left(self):
        self.image = self.HAMMER_ATT_LEFT[self.attframe]
    def update_hammer_att_right(self):
        self.image = self.HAMMER_ATT_RIGHT[self.attframe]
    def update_crouch(self):
        self.image = self.CROUCH[self.cframe]
    def update_crouch_right(self):
        self.image = self.CROUCH_RIGHT[self.cwalk_frame]
    def update_crouch_left(self):
        self.image = self.CROUCH_LEFT[self.cwalk_frame]
    def update_recoil(self):
        self.image = self.RECOIL[self.immunity]
    def update_recoil_hammer_right(self):
        self.image = self.RECOIL_HAMMER_RIGHT[self.immunity]
    def update_recoil_hammer_left(self):
        self.image = self.RECOIL_HAMMER_LEFT[self.immunity]
    def get_head(self):
        return self.rect.centery - self.rect.height / 2

    def get_foot(self):
        return self.rect.centery + self.rect.height / 2

    def get_rit(self):
        return self.rect.centerx + self.rect.width / 2
    
    def get_lef(self):
        return self.rect.centerx - self.rect.width / 2

    def lef_foot(self):
        return self.rect.centerx  - self.rect.width / 2 + FEET

    def rit_foot(self):
        return self.rect.centerx + self.rect.width / 2 - FEET

    def get_center(self):
        return self.rect.centerx
    
    def get_centery(self):
        return self.rect.centery
        
    def get_speedx(self):
        return self.speedx
        
    def get_speedy(self):
        return self.speedy

    def get_health(self):
        return self.HEALTH

    def get_continues(self):
        return self.continues

    def get_hor_scroll(self):
        return self.hor_scroll

    def get_ver_scroll(self):
        return self.ver_scroll

    def get_bones(self):
        return self.bones

    def get_using(self):
        return self.using

    def get_move_to_check(self):
        return self.move_to_check

    def get_last_check(self):
        return self.last_check

    def get_win(self):
        return self.WINNER

    def get_level_event_group(self):
        return self.level_event_group

    def get_direction(self):
        return self.facingRight

    def get_num_attacks(self):
        return self.numAttacks

    def get_weapon_index(self):
        return self.weaponIndex

    def get_load_progress(self):
        return self.load_progress

    def set_hor_scroll(self, hor_dir):
        if self.hor_scroll > 0:
            self.rect.centerx -= 1
        elif self.hor_scroll < 0:
            self.rect.centerx += 1

        self.hor_scroll = hor_dir

    def set_ver_scroll(self, ver_dir, elapsed, scrolling):
        if scrolling < 0 and self.speedy >= 0:
            self.rect.centery += 1
        elif scrolling < 0 and self.speedy < 0:
            self.rect.centery += 1
        elif scrolling > 0 and self.speedy > 0:
            self.rect.centery -= self.speedy * elapsed
        elif scrolling > 0 and self.speedy < 0:
            pass
        
        self.ver_scroll = ver_dir

    def set_move_to_check(self, setting):
        self.move_to_check = setting
    
    def setAlive(self):
        self.finishedDie = False

    def reset_continues(self):
        self.continues = MAX_CONTINUES

    def is_alive(self):
        return self.ALIVE

    def check_alive(self):
        if self.HEALTH <= 0:
            self.ALIVE = False
    
    def resurrect(self):
        self.ALIVE = True
        self.HEALTH = MAX_HEALTH
        self.finishedDie = False
        self.bones = STARTING_BONES
        
        self.touch_enemy = False

        self.immune = False
        self.immunetime = 0.0
        self.facingRight = True

        self.oldtool = -1
        self.numAttacks = 0
        self.weaponIndex = INVALID_WEAPON_INDEX
        self.attacking = False

        self.level_event_group = []
        if self.continues < 2:
            pass
            #self.load_progress -= 1#(self.continues - 2)
        
    def finishedDying(self):
        return self.finishedDie
        
    def die(self, time):
        self.dtime += time
        if self.dtime <= self.DEATHCYCLE:
            dframe = int(self.dtime / (self.DEATHCYCLE / len(self.DIE)))
            if dframe != self.dframe:
                self.dframe = dframe
                self.update_image_die()
        else:
            self.finishedDie = True

    def subtract_continue(self):
        self.continues -= 1

    def set_using(self, set_val):
        self.using = set_val

    def go_to_check(self):
        self.rect.centerx = self.last_check[0]
        self.rect.centery = self.last_check[1] - self.rect.height 

    def land(self, set_grounded, set_y_position = 0):
        self.grounded = set_grounded
        if set_grounded:
            self.rect.centery = set_y_position - self.rect.height / 2 + 1

    def stop(self, set_x_position):
        self.rect.centerx = set_x_position - self.rect.width / 2

    def animation_recoil(self):
        if(self.facingRight and self.weaponIndex == 0):
             self.update_recoil_hammer_right()
        elif(not self.facingRight and self.weaponIndex == 0):
            self.update_recoil_hammer_left()
        elif(not self.attacking):
            self.update_recoil()

    def enemy_collide(self, targ_enemies, x_plus, x_minus):
        if self.attacking and targ_enemies:
            for this_enemy in targ_enemies:
                if this_enemy.get_centerx() > self.rect.centerx:
                    if self.facingRight:
                        this_enemy.hurt()
                        self.cooling = True
                        self.attacking = False
                        self.numAttacks = self.numAttacks - 1
                    else:
                        if not self.immune:
                            self.animation_recoil()
                            self.HEALTH -= 1
                            self.TAKEDAMAGE.play()
                            self.immune = True
                        self.touch_enemy = True
                elif this_enemy.get_centerx() < self.rect.centerx:
                    if not self.facingRight:
                        this_enemy.hurt()
                        self.cooling = True
                        self.attacking = False
                        self.numAttacks = self.numAttacks - 1
                    else:
                        if not self.immune:
                            self.animation_recoil()
                            self.HEALTH -= 1
                            self.TAKEDAMAGE.play()
                            self.immune = True
                        self.touch_enemy = True
        elif targ_enemies and not self.touch_enemy:
            if not self.immune:
                self.animation_recoil()
                self.HEALTH -= 1
                self.TAKEDAMAGE.play()
                self.immune = True
            self.touch_enemy = True
	elif targ_enemies and self.touch_enemy:
            for this_enemy in targ_enemies:
                if self.get_rit() > this_enemy.get_rit():
                    x_plus = True
                    x_minus = False
		else:
		    x_plus = False
		    x_minus = True
        elif not targ_enemies:
            self.touch_enemy = False
	return x_plus, x_minus

    def rocket_collide(self, targ_rockets):
        if self.attacking and targ_rockets:
            for this_rocket in targ_rockets:
                if this_rocket.get_centerx() > self.rect.centerx:
                    if self.facingRight:
                        this_rocket.kill()
                    else:
                        if not self.immune:
                            self.animation_recoil()
                            self.HEALTH -= 1
                            self.TAKEDAMAGE.play()
                            self.immune = True
                elif this_rocket.get_centerx() < self.rect.centerx:
                    if not self.facingRight:
                        this_rocket.kill()
                    else:
                        if not self.immune:
                            self.animation_recoil()
                            self.HEALTH -= 1
                            self.TAKEDAMAGE.play()
                            self.immune = True
        elif targ_rockets:
            for this_rocket in targ_rockets:
                if not self.immune:
                    self.animation_recoil()
                    self.HEALTH -= 1
                    self.TAKEDAMAGE.play()
                    self.immune = True

    def bone_collide(self, targ_bones):
        if targ_bones:
            for this_bone in targ_bones:
                if this_bone.is_bone():
                    self.bones += 1
                else:
                    if self.HEALTH < MAX_HEALTH:
                        self.HEALTH += 1

    def collide_right(self, targ_platforms):
        collide = False
        if targ_platforms:
           for this_platform in targ_platforms:
                if self.speedy == 0 and self.get_foot() - COLLISION_MODIFIER > this_platform.get_top():
                    if self.get_lef() <= this_platform.get_rit():
                        collide = True
        return collide

    def collide_left(self, targ_platforms):
        collide = False
        if targ_platforms:
           for this_platform in targ_platforms:
                if self.speedy == 0 and self.get_foot() - COLLISION_MODIFIER > this_platform.get_top():
                    if  self.get_rit() >= this_platform.get_lef():
                        collide = True
        return collide   

    def does_land(self, targ_platforms, collide_rit, collide_lef):
        lands = False
        if targ_platforms:
            for this_platform in targ_platforms:
                if self.weaponIndex == HAMMER_INDEX and not self.facingRight:
                    if not (self.get_foot() - COLLISION_MODIFIER > this_platform.get_top() or self.speedy < 0 or this_platform.get_lef() - (COLLISION_MODIFIER * 3) > self.rit_foot() or this_platform.get_rit() - (COLLISION_MODIFIER * 3) < self.lef_foot()):
                        lands = True
                        current = this_platform 
                else:
                    if not (self.get_foot() - COLLISION_MODIFIER > this_platform.get_top() or self.speedy < 0 or this_platform.get_lef() > self.rit_foot() or this_platform.get_rit() < self.lef_foot()):
                        lands = True
                        current = this_platform
        if lands:
            self.land(lands, current.get_top())
                            
            if current.is_moving_x():
                if current.get_move_right() and not collide_rit:
                    if current.get_counter(): 
                        self.rect.centerx += math.ceil(current.speedx() * current.get_time())
                elif not current.get_move_right() and not collide_lef:
                    if current.get_counter(): 
                        self.rect.centerx -= math.ceil(current.speedx() * current.get_time())
            if current.is_moving_y():
                if current.get_move_down():
                    if current.get_counter():
                        self.rect.centery += math.ceil(current.speedy() * current.get_time())                    
        else:
            self.land(lands)
            
    def platform_collide(self, targ_platforms):
        if targ_platforms:
            collide_rit = self.collide_right (targ_platforms)
            collide_lef = self.collide_left (targ_platforms)
            for this_platform in targ_platforms:
                if (self.speedy == 0 or this_platform.is_wall() or (self.speedy > 0 and self.rect.centery + self.rect.height/2 < this_platform.get_centery())) and self.get_foot() - COLLISION_MODIFIER > this_platform.get_top():
                    if self.rect.centerx >= this_platform.get_center(): 
                        if self.rect.centerx - COLLISION_MODIFIER == this_platform.get_rit() and self.weaponIndex != HAMMER_INDEX:
                             self.rect.centerx = this_platform.get_rit() + self.rect.width/2 + 1
                        elif self.weaponIndex == HAMMER_INDEX and self.rect.centerx + COLLISION_MODIFIER == this_platform.get_rit():
                            self.rect.centerx = this_platform.get_rit() + self.rect.width/2 + 1
                    elif self.rect.centerx <= this_platform.get_center():
                        if self.rect.centerx + COLLISION_MODIFIER == this_platform.get_lef():# and self.weaponIndex != HAMMER_INDEX:
                            self.rect.centerx = this_platform.get_lef() - self.rect.width/2 - 1
##                        elif self.weaponIndex == HAMMER_INDEX and self.rect.centerx - COLLISION_MODIFIER == this_platform.get_lef():
##                            self.rect.centerx = this_platform.get_lef() - self.rect.width/2 - 1

            self.does_land(targ_platforms, collide_rit, collide_lef)
        else:
            self.land(False)

    def trigger_collide(self, targ_triggers, x_offset, y_offset):
        del(self.level_event_group[:])
        for this_trigger in targ_triggers:
            event = this_trigger.get_event_type()
            if event == KILL:
                self.HEALTH = 0
            elif event == WIN:
                self.WINNER = True
            elif event == CHECKPOINT:
                self.CHECKSOUND.play()
                self.last_check = this_trigger.get_x(), this_trigger.get_y()
                self.level_event_group.append(this_trigger)
            elif event == PITFALL_TRIG:
                self.HEALTH -= 1
                if self.HEALTH > 0:
                    #Create Player at last checkpoint
                    self.GOCHECK.play()
                    self.set_move_to_check(True)
                    self.go_to_check()
            elif event == LOAD_JUNK and this_trigger.get_targ_id() > self.load_progress:
                print "loading" + str(this_trigger.get_targ_id())
                self.load_progress += 1
                self.level_event_group.append(this_trigger)
            elif self.using and not event == NULL_TRIG:
                self.level_event_group.append(this_trigger)
        self.using = False

    def check_scroll(self):
        if self.rect.centerx >= RIGHT_DEADZONE_BOUND:
            self.hor_scroll = RIGHT
        elif self.rect.centerx <= LEFT_DEADZONE_BOUND:
            self.hor_scroll = LEFT
        else:
            self.hor_scroll = NEUTRAL

        if self.rect.centery >= LOWER_DEADZONE_BOUND:
            self.ver_scroll = DOWN
        elif self.rect.centery <= UPPER_DEADZONE_BOUND:
            self.ver_scroll = UP
        else:
            self.ver_scroll = NEUTRAL

    def handle_right(self, time, x_plus, targ_platforms):
        #The player is moving right
        
        if x_plus and self.rect.centerx < self.surf_width - self.rect.width/2:
            self.rect.centerx += math.ceil(self.speedx * time)
            if self.SOUNDINDEX == 3:
                self.SOUNDINDEX = 0
            #self.FOOTSTEPS[self.SOUNDINDEX].play()
            self.SOUNDINDEX += 1
         
            if targ_platforms:
                  for this_platform in targ_platforms:
                      if (self.get_rit() == this_platform.get_lef()) and self.get_foot() - COLLISION_MODIFIER >= this_platform.get_top() and self.grounded:
                           self.stop(this_platform.get_lef())
                         
            #Animate player
            if self.grounded:
                if self.crouching:
                    self.cwalk_time += time
                    if self.cwalk_time > self.CWALK_CYCLE:
                        self.cwalk_time = 0.0
                    cwalk_frame = int(self.cwalk_time / (self.CWALK_CYCLE / len(self.CROUCH_RIGHT)))
                    if cwalk_frame != self.cwalk_frame:
                        self.cwalk_frame = cwalk_frame
                        self.update_crouch_right()
                else:
                    self.time = self.time + time             
                    if self.time > self.CYCLE:
                        self.time = 0.0
                    frame = int(self.time / (self.CYCLE / len(self.IMAGES)))
                    if frame != self.frame:
                        self.frame = frame
                        if self.weaponIndex == 0:
                            if self.attacking:
                                self.update_hammer_att_right()
                            else:
                                self.update_hammer_right()
                        else:
                            self.update_image()
                self.facingRight = True
        
        #The player is moving left but has hit the edge of the screen
        elif x_plus:
            self.facingRight = True

    def handle_left(self, time, x_minus, targ_platforms):
        
        if x_minus and self.rect.centerx > self.rect.width/2:
            self.rect.centerx -= math.ceil(self.speedx * time)
            if self.SOUNDINDEX == 3:
                self.SOUNDINDEX = 0
            #self.FOOTSTEPS[self.SOUNDINDEX].play()
            self.SOUNDINDEX += 1
            
            if targ_platforms:
                  for this_platform in targ_platforms:
                      if (self.get_lef() == this_platform.get_rit()) and self.get_foot() - COLLISION_MODIFIER >= this_platform.get_top() and self.grounded:
                        self.stop(this_platform.get_rit())

            #Animate player
    	    if self.grounded:
    	        if self.crouching:
                    self.cwalk_time += time
                    if self.cwalk_time > self.CWALK_CYCLE:
                        self.cwalk_time = 0.0
                    cwalk_frame = int(self.cwalk_time / (self.CWALK_CYCLE / len(self.CROUCH_LEFT)))
                    if cwalk_frame != self.cwalk_frame:
                        self.cwalk_frame = cwalk_frame
                        self.update_crouch_left()
                else:
                    self.time = self.time + time        
                    if self.time > self.CYCLE:
                        self.time = 0.0
                    frame = int(self.time / (self.CYCLE / len(self.NEG_IMAGES)))
                    if frame != self.frame:
                        self.frame = frame
                        if self.weaponIndex == 0:
                            if self.attacking:
                                self.update_hammer_att_left()
                            else:
                                self.update_hammer_left()
                        else:
                            self.update_image_neg()  
            self.facingRight = False

        #The player is moving left but has hit the edge of the screen
        elif x_minus:
            self.facingRight = False

    def handle_airborne(self, time, y_plus):
        if self.grounded:
            self.speedy = 0
        elif not self.crouching or (self.crouching and not self.grounded):
            self.time = self.time + time
            if self.time > self.CYCLE:
                self.time = 0.0
            frame = int(self.time / (self.JUMP_CYCLE/ len(self.JUMP)))
    	    if frame != self.frame:
                self.frame = frame
                if self.weaponIndex == 0:
                    if self.facingRight:
                        if self.attacking and self.COOLDOWN <= self.ATTCYCLE:
                            self.update_hammer_att_right()
                        elif self.attacking and self.COOLDOWN > self.ATTCYCLE:
                            self.cooldown(time)
                        else:
                            self.update_hammer_jump_right()
                    else:
                        if self.attacking and self.COOLDOWN <= self.ATTCYCLE:
                            self.update_hammer_att_left()
                        elif self.attacking and self.COOLDOWN > self.ATTCYCLE:
                            self.cooldown(time)
                        else:
                            self.update_hammer_jump_left()
                elif self.crouching:
                    self.image = self.CROUCH[4]
                else:
                    self.update_image_jump()
            if self.speedy < TERMINAL_VELOCITY:
                self.speedy += GRAVITY * time
            else:
                self.speedy = TERMINAL_VELOCITY

        if y_plus and self.grounded and not self.crouching and not self.onladder:
            self.JUMPSOUND.play()
            self.speedy += JUMP_VEL
            self.grounded = False

        self.rect.centery += self.speedy * time
    
    def attack_left(self, time):
        
        if self.atttime <= self.ATTCYCLE:
            attframe = int(self.atttime / (self.ATTCYCLE / len(self.HAMMER_ATT_LEFT)))
            if attframe != self.attframe:
                self.attframe += 1
                self.update_hammer_att_left()
        else:
            self.attacking = False
            self.update_hammer_left()
        self.atttime += time
    
    def attack_right(self, time):
        
        if self.atttime <= self.ATTCYCLE:
            attframe = int(self.atttime / (self.ATTCYCLE / len(self.HAMMER_ATT_RIGHT)))
            if attframe != self.attframe:
                self.attframe += 1
                self.update_hammer_att_right()
        else:
            self.attacking = False
            self.update_hammer_right()
        self.atttime += time
            
    def cooldown(self, time):
        self.COOLDOWN += time
        if self.COOLDOWN >= .8:
            self.COOLDOWN = 0.0
    
    def crouch(self, time, crouch, x_pos, x_neg, y_pos):
        if self.grounded and crouch and not self.crouching:
            self.cframe = 0
            self.ctime = 0.0
            self.crouching = True
            if not self.temp_image:
                self.temp_image = self.image
        if self.crouching and not crouch:
            self.image = self.temp_image
            self.temp_image = None
            self.rect.centery -= (100 - self.rect.height)
            self.rect.height = 100
            self.crouching = False
        if self.crouching and self.grounded:
            self.ctime += time
            if self.ctime <= self.CROUCH_CYCLE:               
                cframe = int(self.ctime / (self.CROUCH_CYCLE / len(self.CROUCH)))
                if x_pos or x_neg:# or y_pos:
                    self.image = self.CROUCH[4]
                    self.ctime = 10.0
                    self.rect.centery += (self.rect.height - 60)
                    self.rect.height = 60
                if cframe != self.cframe:
                    self.cframe = cframe
                    self.update_crouch()
                    self.rect.height -= 10
                    self.rect.centery += 10
                    
    def handle_ladders(self, time, y_pos, y_neg, hit_ladders, x_pos, x_neg):
        if hit_ladders:
            if y_pos or y_neg:
                self.onladder = True
            elif self.onladder and (x_pos or x_neg):
                self.onladder = False
                self.land(False)
            for this_ladder in hit_ladders:
                if self.onladder:
                    if y_pos and self.rect.centery <= this_ladder.get_top():
                        self.onladder = False
                        self.rect.centery += JUMP_VEL*time
                    if self.get_foot() - COLLISION_MODIFIER <= this_ladder.get_top() and not y_neg and not self.weaponIndex == HAMMER_INDEX:
                        self.land(True, this_ladder.get_top())
                        self.onladder = True
                    elif self.get_foot() - COLLISION_MODIFIER <= this_ladder.get_top() and not y_neg and self.weaponIndex == HAMMER_INDEX:
                        if self.facingRight and self.get_rit() - (COLLISION_MODIFIER * 3) > this_ladder.get_lef():
                            self.land(True, this_ladder.get_top())
                            self.onladder = True
                        elif not self.facingRight and self.get_lef() + (COLLISION_MODIFIER * 3) < this_ladder.get_rit():
                            self.land(True, this_ladder.get_top())
                            self.onladder = True
                    elif self.get_rit() >= this_ladder.get_lef():
                        self.rect.centerx = this_ladder.get_center()
                        if y_pos:
                            self.rect.centery -= math.ceil(self.speedx * time)
                            self.onladder = True
                    if y_neg:
                        self.rect.centery += math.ceil(self.speedx * time)
        elif self.onladder:
            self.onladder = False
            self.land(False)

    def on_ladder(self):
        return self.onladder

    def kill_fake(self):
        return self.toolnum

    def make_tool(self):
        if not self.position_tool:
            self.position_tool = True
            if self.toolnum == LADDER_INDEX and self.bones >= LADDER_COST and self.grounded:
                self.oldtool = LADDER_INDEX
                return 3
            elif self.toolnum == BRIDGE_INDEX and self.bones >= BRIDGE_COST and self.grounded:
                self.oldtool = BRIDGE_INDEX
                return 4
        else:
            self.position_tool = False
            if self.toolnum == MAKE_WEAPON_INDEX and self.oldtool == LADDER_INDEX and \
               self.bones >= LADDER_COST and self.grounded:
                self.bones -= LADDER_COST
                return_val = self.oldtool
                self.oldtool = INVALID_WEAPON_INDEX
                return return_val
            if self.toolnum == MAKE_WEAPON_INDEX and self.oldtool == BRIDGE_INDEX and \
               self.bones >= BRIDGE_COST and self.grounded:
                self.bones -= BRIDGE_COST
                return_val = self.oldtool
                self.oldtool = INVALID_WEAPON_INDEX
                return return_val
        if self.toolnum == CANCEL_WEAPON_INDEX:
            self.position_tool = False
            self.oldtool = INVALID_WEAPON_INDEX
        return INVALID_WEAPON_INDEX
    
    def update(self, time, x_pos, x_neg, y_pos, up, selectedWeapon, attack, crouch, using, tools, current_level):
        enemy_group = current_level.get_enemies()
        rocket_group = current_level.get_rockets()
        bone_group = current_level.get_bones()
        platform_group = current_level.get_platforms()
        ladder_group = current_level.get_ladders()
        trigger_group = current_level.get_triggers()

        #Check for collisions
        hit_enemies = PS.spritecollide(self, enemy_group, False)
        hit_rockets = PS.spritecollide(self, rocket_group, False)
        hit_bones = PS.spritecollide(self, bone_group, False)
        hit_platforms = PS.spritecollide(self, platform_group, False)
        hit_ladders = PS.spritecollide(self, ladder_group, False)
        hit_triggers = PS.spritecollide(self, trigger_group, False)

        self.using = using

        #With this, cannot attack while touching a switch or checkpoint.
        #This may be unwanted. 
        #if hit_triggers:
        #    attack = False

        if not self.onladder:
            self.crouch(time, crouch, x_pos, x_neg, y_pos)
        
        if attack and not self.attacking:# and self.COOLDOWN == 0.0:
            if self.cooling:
                if self.weaponIndex == HAMMER_INDEX and self.COOLDOWN == 0.0:
                    self.atttime = 0.0
                    self.attframe = 0
                    self.attacking = True
                    self.cooling = False
                    self.HAMMERHIT.play()
            else:
                if self.weaponIndex == HAMMER_INDEX:
                    self.atttime = 0.0
                    self.attframe = 0
                    self.attacking = True
                    self.cooling = False
                    self.HAMMERHIT.play()
        if self.attacking and not crouch and self.COOLDOWN <= self.ATTCYCLE:
            if self.facingRight:
                self.attack_right(time)
            else:
                self.attack_left(time)
            self.COOLDOWN += time
        else:
            self.cooldown(time)
        #print self.attacking
        if self.numAttacks == 0:
            self.numAttacks = MAX_HAMMER_ATTACKS
            self.weaponIndex = INVALID_WEAPON_INDEX
            self.attacking = False
            if self.facingRight:
                self.update_image()
            else:
                self.update_image_neg()
        if selectedWeapon == HAMMER_INDEX and self.weaponIndex != HAMMER_INDEX and self.bones >= HAMMER_COST:
            self.weapons.append(weapon.Hammer())
            if self.facingRight:
                self.image = self.HAMMER_RIGHT[self.frame]
            else:
                self.image = self.HAMMER_LEFT[self.frame]
            self.weaponIndex = HAMMER_INDEX
            self.bones -= HAMMER_COST

        self.toolnum = tools

        #Set immune time
        self.immunetime = self.immunetime + time
        if self.immunetime > self.IMMUNITY:
            self.immune = False
            self.immunetime = 0.0

        #React to enemy collisions and update player health
        x_pos, x_neg = self.enemy_collide(hit_enemies, x_pos, x_neg)

        #React to trigger collisions
        self.trigger_collide(hit_triggers, current_level.get_hor_offset(), current_level.get_ver_offset())

        #React to rocket collisions
        self.rocket_collide(hit_rockets)

        #React to bone collisions
        self.bone_collide(hit_bones)

        #React to ladder collisions
        self.handle_ladders(time, y_pos, crouch, hit_ladders, x_pos, x_neg)

        #Handle right motion
        self.handle_right(time, x_pos, hit_platforms)

        #Handle left motion
        self.handle_left(time, x_neg, hit_platforms)

        if not self.onladder:
            #Apply gravity and jump animation
            self.handle_airborne(time, y_pos)

        #Handle collision with platforms
        hit_platforms = PS.spritecollide(self, platform_group, False)        
        self.platform_collide(hit_platforms)

        #Check to see if the player is still alive
        self.check_alive()

        #Check for scrolling
        self.check_scroll()

        return self.WINNER

    def set_sound(self, target_filename):
        self.sound = PM.Sound(target_filename)
        self.sound.set_volume(self.volume)
