import pygame.image as PI
import math
import pygame.sprite as PS

NULL_TRIG     = -1
KILL          = 0
WIN           = 1
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
PITFALL_TRIG  = 12
LOAD_JUNK     = 13

SWITCH_ON_FILE = "Levels/Switch_on.png"
SWITCH_OFF_FILE = "Levels/Switch_off.png"
FLOAT_ON_FILE = "Levels/float_switch_on.png"
FLOAT_OFF_FILE = "Levels/float_switch_off.png"
CHECK_OFF_FILE = "Levels/check_off.png"
CHECK_ON_FILE = "Levels/check_on.png"

class Trigger(PS.Sprite):
    image = None
    image_file = None
    event_type = 0
    targ_item_id = 0
    targ_item_x = 0
    targ_item_y = 0
    targ_move_x = 0
    targ_move_y = 0
    id_num = 0

    def __init__(self, filename, event_type, loc_x, loc_y, item_id = 0, item_move_x_pos = 0, item_move_x_neg = 0, item_move_y_pos = 0, item_move_y_neg = 0, idnum = 0):
        PS.Sprite.__init__(self)
        if not self.image:
            self.image = PI.load(filename).convert_alpha()
        self.rect = self.image.get_rect()
        self.image_file = filename

        self.event_type = event_type
        self.targ_item_id = item_id
        self.targ_move_x_pos = item_move_x_pos
        self.targ_move_x_neg = item_move_x_neg
        self.targ_move_y_pos = item_move_y_pos
        self.targ_move_y_neg = item_move_y_neg

        self.rect.centerx = loc_x
        self.rect.centery = loc_y

        self.targ_move_x = self.targ_move_x_pos - self.targ_move_x_neg
        self.targ_move_y = self.targ_move_y_pos - self.targ_move_y_neg

        self.id_num = idnum

    def get_top(self):
        return self.rect.centery - self.rect.height / 2

    def get_bot(self):
        return self.rect.centery + self.rect.height / 2

    def get_rit(self):
        return self.rect.centerx + self.rect.width / 2
    
    def get_lef(self):
        return self.rect.centerx - self.rect.width / 2

    def get_x(self):
        return self.rect.centerx

    def get_y(self):
        return self.rect.centery

    def get_targ_id(self):
        return self.targ_item_id

    def get_move_x(self):
        return self.targ_move_x

    def get_move_x_pos(self):
        return self.targ_move_x_pos

    def get_move_x_neg(self):
        return self.targ_move_x_neg
    
    def get_move_y(self):
        return self.targ_move_y

    def get_move_y_pos(self):
        return self.targ_move_y_pos

    def get_move_y_neg(self):
        return self.targ_move_y_neg
    
    def get_event_type(self):
        return self.event_type

    def get_id(self):
        return self.id_num

    def set_targ_id(self, targ_id):
        self.targ_item_id = targ_id

    def set_targ_coord(self, x, y):
        self.targ_move_x = x
        self.targ_move_y = y

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

    def invert_image(self):
        if self.image_file == SWITCH_ON_FILE:
            self.image = PI.load(SWITCH_OFF_FILE).convert_alpha()
            self.image_file = SWITCH_OFF_FILE
        elif self.image_file == SWITCH_OFF_FILE:
            self.image = PI.load(SWITCH_ON_FILE).convert_alpha()
            self.image_file = SWITCH_ON_FILE
        if self.image_file == FLOAT_ON_FILE:
            self.image = PI.load(FLOAT_OFF_FILE).convert_alpha()
            self.image_file = FLOAT_OFF_FILE
        elif self.image_file == FLOAT_OFF_FILE:
            self.image = PI.load(FLOAT_ON_FILE).convert_alpha()
            self.image_file = FLOAT_ON_FILE
        elif self.image_file == CHECK_ON_FILE:
            self.image = PI.load(CHECK_OFF_FILE).convert_alpha()
            self.image_file = CHECK_OFF_FILE
        elif self.image_file == CHECK_OFF_FILE:
            self.image = PI.load(CHECK_ON_FILE).convert_alpha()
            self.image_file = CHECK_ON_FILE

    def invert(self):
        if not self.event_type == NULL_TRIG:
            self.invert_image()
        
        if self.event_type == MOVE_PLAT:
            pass
        elif self.event_type == CREATE_PLAT:
            self.event_type = DEL_PLAT
        elif self.event_type == DEL_PLAT:
            self.event_type = CREATE_PLAT
        elif self.event_type == MOVE_ENEM:
            pass
        elif self.event_type == CREATE_ENEM:
            self.event_type = DEL_ENEM
        elif self.event_type == DEL_ENEM:
            self.event_type = CREATE_ENEM
        elif self.event_type == SET_MOTION:
            self.event_type = STOP_MOTION
        elif self.event_type == STOP_MOTION:
            self.event_type = RESUME_MOTION
        elif self.event_type == RESUME_MOTION:
            self.event_type = STOP_MOTION
        elif self.event_type == CHECKPOINT:
            self.event_type = NULL_TRIG
        elif self.event_type == LOAD_JUNK:
            self.event_type = NULL_TRIG

    def update(self, elapsed):
        pass
