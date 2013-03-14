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
import player
import enemy
import platform
import rocket
import bone
import ladder
import layer
import trigger

WIDTH           = 800
HEIGHT          = 600
PARALLAX_RATE   = 0.5
LEFT            = -1
RIGHT           = 1
UP              = -1
DOWN            = 1
NEUTRAL         = 0

#Enemy types
ROBOTO    = 0
VIRUS     = 1
SPARKY    = 2
SPACESHIP = 3

#Deadzone boundaries
LEFT_DEADZONE_BOUND  = 390
RIGHT_DEADZONE_BOUND = 410
LOWER_DEADZONE_BOUND = 350
UPPER_DEADZONE_BOUND = 200
CENTER_X = (LEFT_DEADZONE_BOUND + RIGHT_DEADZONE_BOUND) / 2
CENTER_Y = (LOWER_DEADZONE_BOUND + UPPER_DEADZONE_BOUND) / 2

#Trigger event types
MOVE_PLAT     = 2
CREATE_PLAT   = 3
DEL_PLAT      = 4
MOVE_ENEM     = 5
CREATE_ENEM   = 6
DEL_ENEM      = 7
SET_MOTION    = 8
STOP_MOTION   = 9
RESUME_MOTION = 10
CHECKPOINT    = 11
LOAD_JUNK     = 13

class Level(object):
    platform_group = None
    trigger_group = None
    enemy_group = None
    rocket_group = None
    ladder_group = None
    landscape_offset_x = 0
    landscape_offset_y = 0
    next_platform_id = 1
    next_enemy_id = 1
    level_surface = None
    win = False
    
    def __init__(self, filename, volume):
        self.volume = volume
        self.PLAT_ON = PX.Sound("Sounds/effects/platform_on.ogg")
        self.PLAT_ON.set_volume(self.volume)
        #Layer group
        self.layer_group = []
        #Platform group
        self.platform_group = PS.Group()
        #Trigger group
        self.trigger_group = PS.Group()
        #Bones group
        self.bones_group = PS.Group()
        #Enemy group
        self.enemy_group = PS.Group()
        #Rocket group
        self.rocket_group = PS.Group()
        #Ladder group
        self.ladder_group = PS.Group()
        #Fake ladder group
        self.fake_ladders = PS.Group()
        #Fake Bridge Group
        self.fake_bridges = PS.Group()

        self.last_check = (0,0)

        self.moving_tools = False
        self.fake_toolnum = -1

        self.main_level_file = filename
        
        self.load_file(self.main_level_file + ".txt")

    def load_file(self, filename):
        file = open(filename)
        self.delimiter = '\n'
        
        while 1:
            line = file.readline().rstrip(self.delimiter)
            if not line:
                break
            if line == "Start_Location":
                self.last_check = int(file.readline().rstrip(self.delimiter)) - CENTER_X, \
                                  int(file.readline().rstrip(self.delimiter)) - CENTER_Y
                if self.last_check[0] < 0: self.last_check = 0, self.last_check[1]
                if self.last_check[1] < 0: self.last_check = self.last_check[0], 0
            if line == "Layers":
                while 1:
                    line = file.readline().rstrip(self.delimiter)
                    if line == "End Layers":
                        break
                    words = line.split()
                    self.layer_group.append(layer.Layer(PI.load(words[0]).convert_alpha(), float(words[1])))
            elif line == "Dimensions":
                self.width = int(file.readline().rstrip(self.delimiter))
                self.height = int(file.readline().rstrip(self.delimiter))
            elif line == "Enemies":
                while 1:
                    line = file.readline().rstrip(self.delimiter)
                    if line == "End Enemies":
                        break
                    words = line.split()
                    if words[0] == "Roboto" or words[0] == "Virus" or words[0] == "Sparky" or \
                       words[0] == "Virus_Melee" or words[0] == "Spaceship":
                        self.add_enemy(words)
            elif line == "Triggers":
                while 1:
                    line = file.readline().rstrip(self.delimiter)
                    if line == "End Triggers":
                        break
                    words = line.split()
                    self.add_trigger(words)
            elif line == "Platforms":
                while 1:
                    line = file.readline().rstrip(self.delimiter)
                    if line == "End Platforms":
                        break
                    words = line.split()
                    if words[0] == "Small_Platform" or words[0] == "Mini_Platform" or words[0] == "Large_Platform" or words[0] == "Long_Platform" \
                       or words[0] == "Small_Wall" or words[0] == "Large_Wall" or words[0] == "Long_Wall":
                        self.add_platform(words[0], int(words[1]), int(words[2]), int(words[3]), int(words[4]), int(words[5]), int(words[6]))
            elif line == "Bones":
                while 1:
                    line = file.readline().rstrip(self.delimiter)
                    if line == "End Bones":
                        break
                    words = line.split()
                    if words[0] == "Bone":
                        self.bones_group.add(bone.Bone(WIDTH, HEIGHT, int(words[1]) - self.landscape_offset_x, int(words[2]) - self.landscape_offset_y))
                    elif words[0] == "Calcium":
                        self.bones_group.add(bone.Calcium(WIDTH, HEIGHT, int(words[1]) - self.landscape_offset_x, int(words[2]) - self.landscape_offset_y))
                        
    def get_platforms(self):
        return self.platform_group
    def get_triggers(self):
        return self.trigger_group
    def get_enemies(self):
        return self.enemy_group
    def get_rockets(self):
        return self.rocket_group
    def get_bones(self):
        return self.bones_group
    def get_ladders(self):
        return self.ladder_group

    def get_hor_offset(self):
        return self.landscape_offset_x

    def get_ver_offset(self):
        return self.landscape_offset_y

    def get_next_platform_id(self):
        return self.self.next_platform_id

    def get_last_check(self):
        return self.last_check

    def set_last_check(self, check_pair):
        self.last_check = check_pair[0] - CENTER_X, check_pair[1] - CENTER_Y

        if self.last_check[0] < 0: self.last_check = 0, self.last_check[1]
        if self.last_check[1] < 0: self.last_check = self.last_check[0], 0

    def add_trigger(self, params):
        self.trigger_group.add(trigger.Trigger(params[0], int(params[1]), int(params[2]) - self.landscape_offset_x, \
                                               int(params[3]) - self.landscape_offset_y, int(params[4]), \
                                               int(params[5]), int(params[6]), int(params[7]), int(params[8]), \
                                               int(params[9]) ))

    def load_chunks(self):
        for this_trigger in self.trigger_group:
            if this_trigger.get_event_type() == LOAD_JUNK:
                self.load_file(self.main_level_file + "_" + str(this_trigger.get_targ_id()) + ".txt")
                this_trigger.kill()

    def add_platform(self, plat_type, x_loc, y_loc, x_move, x_move2, y_move, y_move2):
        x_loc = x_loc - self.landscape_offset_x
        y_loc = y_loc - self.landscape_offset_y

        if plat_type == "Small_Platform":
            self.platform_group.add(platform.Small_Platform(WIDTH, HEIGHT, x_loc, y_loc, x_move, x_move2, y_move, y_move2, self.next_platform_id))
        elif plat_type == "Large_Platform":
            self.platform_group.add(platform.Large_Platform(WIDTH, HEIGHT, x_loc, y_loc, x_move, x_move2, y_move, y_move2, self.next_platform_id))
        elif plat_type == "Long_Platform":
            self.platform_group.add(platform.Long_Platform(WIDTH, HEIGHT, x_loc, y_loc, x_move, x_move2, y_move, y_move2, self.next_platform_id))
        elif plat_type == "Mini_Platform":
            self.platform_group.add(platform.Mini_Platform(WIDTH, HEIGHT, x_loc, y_loc, x_move, x_move2, y_move, y_move2, self.next_platform_id))
        elif plat_type == "Small_Wall":
            self.platform_group.add(platform.Small_Wall(WIDTH, HEIGHT, x_loc, y_loc, x_move, x_move2, y_move, y_move2, self.next_platform_id))
        elif plat_type == "Large_Wall":
            self.platform_group.add(platform.Large_Wall(WIDTH, HEIGHT, x_loc, y_loc, x_move, x_move2, y_move, y_move2, self.next_platform_id))
        elif plat_type == "Long_Wall":
            self.platform_group.add(platform.Long_Wall(WIDTH, HEIGHT, x_loc, y_loc, x_move, x_move2, y_move, y_move2, self.next_platform_id))    
        else:
            return

        self.next_platform_id += 1

    def add_bridge(self, x_loc, y_loc):
        self.platform_group.add(platform.Bridge(WIDTH, HEIGHT, x_loc, y_loc, 0, 0, 0, 0, self.next_platform_id))
        self.next_platform_id += 1

    def add_enemy(self, param_array):
        x_loc = int(param_array[1]) - self.landscape_offset_x
        y_loc = int(param_array[2]) - self.landscape_offset_y
        
        if param_array[0] == "Roboto":
            self.enemy_group.add(enemy.Roboto(WIDTH, HEIGHT, x_loc, y_loc, int(param_array[3]), int(param_array[4]), self.next_enemy_id))
        elif param_array[0] == "Sparky":
            self.enemy_group.add(enemy.Sparky(WIDTH, HEIGHT, x_loc, y_loc, int(param_array[3]), int(param_array[4]), self.next_enemy_id))
        elif param_array[0] == "Virus":
            self.enemy_group.add(enemy.Virus(WIDTH, HEIGHT, x_loc, y_loc, int(param_array[3]), int(param_array[4]), self.next_enemy_id))
        elif param_array[0] == "Virus_Melee":
            self.enemy_group.add(enemy.Virus_Melee(WIDTH, HEIGHT, x_loc, y_loc, int(param_array[3]), int(param_array[4]), self.next_enemy_id))
        elif param_array[0] == "Spaceship":
            self.enemy_group.add(enemy.Spaceship(WIDTH, HEIGHT, x_loc, y_loc, int(param_array[3]), int(param_array[4]), self.next_enemy_id))
        else:
            return
        
        self.next_enemy_id += 1

    def scroll_layers(self, hor_dir, ver_dir):
        for this_layer in self.layer_group:
            this_layer.scroll(hor_dir, ver_dir)

    def handle_events(self, event_group, player):
        for this_event in event_group:
            event = this_event.get_event_type()
            if event == CHECKPOINT:
                self.last_check = (self.landscape_offset_x, self.landscape_offset_y)
            elif event == MOVE_PLAT:
                for this_platform in self.platform_group:
                    if this_platform.get_idnum() == this_event.get_targ_id():
                        this_platform.set_x(this_event.get_move_x() - self.landscape_offset_x)
                        this_platform.set_y(this_event.get_move_y() - self.landscape_offset_y)
                        this_event.set_targ_coord(this_platform.get_center() + self.landscape_offset_x, this_platform.get_centery() + self.landscape_offset_y)
            elif event == CREATE_PLAT:
                this_event.set_targ_id(self.next_platform_id)
                self.add_platform("Large_Platform", this_event.get_move_x(), this_event.get_move_y(), 0, 0, 0, 0)
            elif event == DEL_PLAT:
                for this_platform in self.platform_group:
                    if this_platform.get_idnum() == this_event.get_targ_id():
                        this_event.set_targ_coord(this_platform.get_center() + self.landscape_offset_x, this_platform.get_centery() + self.landscape_offset_y)
                        self.platform_group.remove(this_platform)
            elif event == SET_MOTION:
                for this_platform in self.platform_group:
                    if this_platform.get_idnum() == this_event.get_targ_id():
                        #This line causes problems for some reason, to be investigated
                        #this_platform.set_x(this_platform.get_center() - this_event.get_move_x() / 2)
                        #this_platform.set_y(this_platform.get_centery() + this_event.get_move_y() / 2)
                        self.PLAT_ON.play()
                        this_platform.set_move_x_pos(this_event.get_move_x_pos())
                        this_platform.set_move_x_neg(this_event.get_move_x_neg())
                        this_platform.set_move_y_pos(this_event.get_move_y_pos())
                        this_platform.set_move_y_neg(this_event.get_move_y_neg())
                        this_platform.check_movement()

            elif event == STOP_MOTION:
                for this_platform in self.platform_group:
                    if this_platform.get_idnum() == this_event.get_targ_id():
                        this_platform.set_freeze(True)

            elif event == RESUME_MOTION:
                for this_platform in self.platform_group:
                    if this_platform.get_idnum() == this_event.get_targ_id():
                        self.PLAT_ON.play()
                        this_platform.set_freeze(False)
                        
            elif event == MOVE_ENEM:
                for this_enemy in self.enemy_group:
                    if this_enemy.get_id_num() == this_event.get_targ_id():
                        this_enemy.set_x(this_event.get_move_x() - self.landscape_offset_x)
                        this_enemy.set_y(this_event.get_move_y() - self.landscape_offset_y)
            elif event == CREATE_ENEM:
                this_event.set_targ_id(self.next_enemy_id)
                perams = []
                perams.append(this_event.get_move_x() - self.landscape_offset_x)
                perams.append(this_event.get_move_y() - self.landscape_offset_y)
                perams.append(0)
                perams.append(0)
                perams.append(ROBOTO)
                self.add_enemy(perams)
            elif event == DEL_ENEM:
                for this_enemy in self.enemy_group:
                    if this_enemy.get_id_num() == this_event.get_targ_id():
                        this_event.set_targ_coord(this_enemy.get_centerx() + self.landscape_offset_x, this_enemy.get_centery() + self.landscape_offset_y)
                        self.enemy_group.remove(this_enemy)
            elif event == LOAD_JUNK: 
                self.load_file(self.main_level_file + "_" + str(this_event.get_targ_id()) + ".txt")

            this_event.invert()
            

    def draw(self, screen, player_group):
        for this_layer in self.layer_group:
            rec = PG.Rect((this_layer.get_hor_offset(), this_layer.get_ver_offset()), (800, 600))
            screen.blit(this_layer.get_surf_image(), (0, 0), rec)

        self.trigger_group.draw(screen)
        self.platform_group.draw(screen)
        self.ladder_group.draw(screen)
        self.enemy_group.draw(screen)
        self.fake_ladders.draw(screen)
        self.fake_ladders.empty()
        self.fake_bridges.draw(screen)
        self.fake_bridges.empty()

        for this_enemy in self.enemy_group:
            if  not this_enemy.is_fired():
                temp_rocket = this_enemy.add_rocket(self.volume)
                if temp_rocket:
                    self.rocket_group.add(temp_rocket)
                this_enemy.shot_rocket()
        self.rocket_group.draw(screen)
        self.bones_group.draw(screen)

        return self.win

    def move_tools(self, player_group):
        for this_player in player_group:
            if not this_player.kill_fake() == 4:
                if self.fake_toolnum == 3:
                    self.fake_ladders.add(ladder.Fake_Ladder(WIDTH, HEIGHT, this_player.get_center(), this_player.get_centery()))
                elif self.fake_toolnum == 4:
                    if this_player.get_direction():
                        self.fake_bridges.add(platform.Fake_Bridge(WIDTH, HEIGHT, this_player.get_rit() + 40, this_player.get_foot() + 10, 0, 0, 0, 0, -1))
                    else:
                        self.fake_bridges.add(platform.Fake_Bridge(WIDTH, HEIGHT, this_player.get_lef() - 40, this_player.get_foot() + 10, 0, 0, 0, 0, -1))
            else:
                self.fake_toolnum = -1

    def scroll_auto(self, dest_x, dest_y):
        scroll_dist = (dest_x - self.landscape_offset_x, dest_y - self.landscape_offset_y)
                
        self.landscape_offset_x = dest_x
        self.landscape_offset_y = dest_y
            
        #Scroll
        for this_platform in self.platform_group:
            oldpos = this_platform.get_center()
            this_platform.scroll(scroll_dist[0], scroll_dist[1])
            newpos = this_platform.get_center()
        for this_enemy in self.enemy_group:
            this_enemy.scroll(scroll_dist[0], scroll_dist[1])
        for this_rocket in self.rocket_group:
            this_rocket.scroll(scroll_dist[0], scroll_dist[1])
        for this_bone in self.bones_group:
            this_bone.scroll(scroll_dist[0], scroll_dist[1])
        for this_ladder in self.ladder_group:
            this_ladder.scroll(scroll_dist[0], scroll_dist[1])
        for this_trigger in self.trigger_group:
            this_trigger.scroll(scroll_dist[0], scroll_dist[1])
        self.scroll_layers(scroll_dist[0], scroll_dist[1])
        #this_player.set_hor_scroll(NEUTRAL)
        #this_player.set_ver_scroll(NEUTRAL)

    def update(self, elapsed, player_group):
        old_pos = 0
        new_pos = 0
        for this_player in player_group:
            tools = this_player.make_tool()
            if tools == 1:
                self.ladder_group.add(ladder.Ladder(WIDTH, HEIGHT, this_player.get_center(), this_player.get_centery()))
                self.moving_tools = False
            elif tools == 2:
                if this_player.get_direction():
                    self.add_bridge(this_player.get_rit() + 40, this_player.get_foot() + 10)
                else:
                    self.add_bridge(this_player.get_lef() - 40, this_player.get_foot() + 10)
                self.moving_tools = False
            elif tools == 3 or tools == 4:
                self.moving_tools = True
                self.fake_toolnum = tools

            if this_player.get_move_to_check():
                self.scroll_auto(self.last_check[0], self.last_check[1])
                this_player.set_move_to_check(False)

            else:
                scroll_rate_x = this_player.get_hor_scroll() * this_player.get_speedx() * elapsed
                if this_player.get_ver_scroll() < 0:
                    scroll_rate_y = this_player.get_ver_scroll()
                else:
                    scroll_rate_y = this_player.get_ver_scroll() * abs(this_player.get_speedy()) * elapsed
                    if scroll_rate_y == 0 and this_player.get_ver_scroll() != 0:
                        scroll_rate_y = this_player.get_ver_scroll()

                can_scroll_right = (this_player.get_hor_scroll() == RIGHT) and \
                                   (self.layer_group[0].get_hor_offset() / self.layer_group[0].get_par_rate() + WIDTH < self.width)
                can_scroll_left  = (this_player.get_hor_scroll() == LEFT) and \
                                   (self.layer_group[0].get_hor_offset() / self.layer_group[0].get_par_rate() > 0)
                can_scroll_down  = this_player.get_ver_scroll() >= DOWN and \
                                   self.layer_group[0].get_ver_offset() + HEIGHT < self.height
                can_scroll_up    = this_player.get_ver_scroll() <= UP and \
                                   self.layer_group[0].get_ver_offset() > 0

                if can_scroll_right or can_scroll_left:
                    #Scroll right
                    for this_platform in self.platform_group:
                        old_pos = this_platform.get_center()
                        this_platform.scroll(scroll_rate_x, NEUTRAL)
                        new_pos = this_platform.get_center()
                    for this_enemy in self.enemy_group:
                        this_enemy.scroll(scroll_rate_x, NEUTRAL)
                    for this_rocket in self.rocket_group:
                        this_rocket.scroll(scroll_rate_x, NEUTRAL)
                    for this_bone in self.bones_group:
                        this_bone.scroll(scroll_rate_x, NEUTRAL)
                    for this_ladder in self.ladder_group:
                        this_ladder.scroll(scroll_rate_x, NEUTRAL)
                    for this_trigger in self.trigger_group:
                        this_trigger.scroll(scroll_rate_x, NEUTRAL)
                    self.scroll_layers(this_player.get_hor_scroll(), NEUTRAL)
                    this_player.set_hor_scroll(NEUTRAL)
                    self.landscape_offset_x += old_pos - new_pos

                if can_scroll_up or can_scroll_down:
                    #Scroll Up
                    for this_platform in self.platform_group:
                        old_pos = this_platform.get_centery()
                        this_platform.scroll(NEUTRAL, scroll_rate_y)
                        new_pos = this_platform.get_centery()
                    for this_enemy in self.enemy_group:
                        this_enemy.scroll(NEUTRAL, scroll_rate_y)
                    for this_rocket in self.rocket_group:
                        this_rocket.scroll(NEUTRAL, scroll_rate_y)
                    for this_bone in self.bones_group:
                        this_bone.scroll(NEUTRAL, scroll_rate_y)
                    for this_ladder in self.ladder_group:
                        this_ladder.scroll(NEUTRAL, scroll_rate_y)
                    for this_trigger in self.trigger_group:
                        this_trigger.scroll(NEUTRAL, scroll_rate_y)
                    self.scroll_layers(NEUTRAL, scroll_rate_y)
                    this_player.set_ver_scroll(NEUTRAL, elapsed, scroll_rate_y)
                    self.landscape_offset_y += old_pos - new_pos

                self.handle_events(this_player.get_level_event_group(), this_player)
            
        self.platform_group.update(elapsed)
        self.enemy_group.update(elapsed, self.platform_group, player_group)
        for this_enemy in self.enemy_group:
            if this_enemy.get_dead():
                self.bones_group.add(bone.Bone(HEIGHT, WIDTH, this_enemy.get_centerx(), this_enemy.get_foot()))
        self.rocket_group.update(elapsed, player_group)
        self.bones_group.update(elapsed, player_group, self.platform_group)
        if self.moving_tools:
            self.move_tools(player_group)
        
