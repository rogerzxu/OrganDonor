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
import ui
import rocket
import level

#Variables
WIDTH       = 800
HEIGHT      = 600
INTERVAL    = .004

#Item indices
INVALID_WEAPON_INDEX = -1
HAMMER_INDEX         = 0
LADDER_INDEX         = 1
BRIDGE_INDEX         = 2
MAKE_WEAPON_INDEX    = 3
CANCEL_WEAPON_INDEX  = 4

#Menu Screens

#Initialize                                                                                                                   
PG.init()

#Screen Size                                                                                                                  
screen = PDI.set_mode((WIDTH, HEIGHT), PG.FULLSCREEN)


#TODO: Change to title picture when picture available
TITLE = PI.load("menu-screen/play.png").convert_alpha()
#TODO: Change to high scores picture when picture available
HIGH_SCORES = PI.load("menu-screen/highscore_menu.png").convert_alpha()
BRIGHT_MENU = PI.load("menu-screen/brightness_menu.png").convert_alpha()
VOLUME_MENU = PI.load("menu-screen/volume_menu.png").convert_alpha()
PLAY = PI.load("menu-screen/play.png").convert_alpha()
BRIGHT = PI.load("menu-screen/brightness.png").convert_alpha()
VOLUME = PI.load("menu-screen/volume.png").convert_alpha()
QUIT = PI.load("menu-screen/quit.png").convert_alpha()
SCORES = PI.load("menu-screen/high_score.png").convert_alpha()
WIN = PI.load("menu-screen/win.png").convert_alpha()
LOSE = PI.load("menu-screen/lose.png").convert_alpha()
CONTINUE = "menu-screen/lose"

LEVEL0 = "Levels/level_zero"
LEVEL1 = "Levels/level_one"
LEVEL2 = "Levels/level_two"
LEVEL3 = "Levels/level_three"
LEVEL4 = "Levels/level_four"

FIRST_LEVEL = LEVEL0

HIGHSONG = "Sounds/Music/high_score.ogg"
SONG0 = "Sounds/Music/intro.ogg"
SONG1 = "Sounds/Music/game_song_1.ogg"

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

class Globals(object):
    STATE = None
    RUNNING = True
    ALIVE = True
    VOLUME = 0.5
    BRIGHTNESS = 1.0
    LEVEL = None
    LASTLEVEL = None
    CURRENTSONG = SONG1
    LASTCHECK = (0, 0)

class State(object):
    def __init__(self):
        pass
    def render(self):
        pass
    def update(self, time):
        pass
    def event(self, event):
        pass

class Title(State):
    IMAGES = []
    IMAGES.append(PI.load("intro-screen/001.png"))
    IMAGES.append(PI.load("intro-screen/002.png"))
    IMAGES.append(PI.load("intro-screen/003.png"))
    IMAGES.append(PI.load("intro-screen/004.png"))
    IMAGES.append(PI.load("intro-screen/005.png"))
    IMAGES.append(PI.load("intro-screen/006.png"))
    IMAGES.append(PI.load("intro-screen/007.png"))
    IMAGES.append(PI.load("intro-screen/008.png"))
    IMAGES.append(PI.load("intro-screen/009.png"))
    IMAGES.append(PI.load("intro-screen/010.png"))
    IMAGES.append(PI.load("intro-screen/011.png"))
    IMAGES.append(PI.load("intro-screen/012.png"))
    image = IMAGES[0]

    CURRENT = 0
    CYCLE = 1.0
    CLOCK = PT.Clock()
    
    def __init__(self):
        self.sound = PX.Sound("Sounds/effects/string break.ogg")
        self.sound.set_volume(Globals.VOLUME)
        State.__init__(self)
        self.time = 0.0
        self.frame = 0
        
    def render(self):
        lasttime = PT.get_ticks()
        if not PX.music.get_busy():
            PX.music.load(SONG0)
            PX.music.set_volume(Globals.VOLUME)
            PX.music.play(0, 0.0)

        self.image = self.IMAGES[self.CURRENT]
        screen.blit(self.image, (0, 0))
        PDI.flip()

        self.CLOCK.tick()

        elapsed = (PT.get_ticks() - lasttime) / 1000.0

        self.time = self.time + elapsed
        
        if self.time > Title.CYCLE:
            self.time = 0.0
        frame = int(self.time / (Title.CYCLE / len(Title.IMAGES)))
        if frame != self.frame:
            self.frame = frame
            self.update_image()
    
    def event(self, event):
        if event.type == PG.KEYDOWN:
            Globals.STATE = Menu()
            
    def update_image(self):
        if self.CURRENT > 10:
            self.CURRENT = 0
            self.sound.play()
        else:
            self.CURRENT = self.CURRENT + 1

class Menu(State):
    IMAGE = PLAY
    def __init__(self):
        self.sound = PX.Sound("Sounds/effects/clang.ogg")
        self.sound.set_volume(Globals.VOLUME)
        State.__init__(self)
    def render(self):
        screen.blit(self.IMAGE, (0, 0))
        PDI.flip()
        if not PX.music.get_busy():
            PX.music.load(SONG0)
            PX.music.set_volume(Globals.VOLUME)
            PX.music.play(0, 0.0)
    def event(self, event):
        if event.type == PG.KEYDOWN and event.key == PG.K_ESCAPE:
            if Globals.LEVEL:
                PX.music.load(SONG1)
                PX.music.set_volume(Globals.VOLUME)
                PX.music.play(0, 0.0)
                Globals.STATE = Globals.LEVEL
        if self.IMAGE == PLAY:
            if event.type == PG.KEYDOWN and event.key == PG.K_LEFT:
                self.sound.play()
                self.IMAGE = VOLUME
            elif event.type == PG.KEYDOWN and event.key == PG.K_RIGHT:
                self.sound.play()
                self.IMAGE = SCORES
            elif event.type == PG.KEYDOWN and event.key == PG.K_RETURN:
                #Reset Music
                if PX.music.get_busy():
                    PX.music.stop()
                Globals.STATE = Game(FIRST_LEVEL, None)
        elif self.IMAGE == QUIT:
            if event.type == PG.KEYDOWN and event.key == PG.K_LEFT:
                self.sound.play()
                self.IMAGE = SCORES
            elif event.type == PG.KEYDOWN and event.key == PG.K_RIGHT:
                self.sound.play()
                self.IMAGE = BRIGHT
            elif event.type == PG.KEYDOWN and event.key == PG.K_RETURN:
                Globals.RUNNING = False
        elif self.IMAGE == SCORES:
            if event.type == PG.KEYDOWN and event.key == PG.K_LEFT:
                self.sound.play()
                self.IMAGE = PLAY
            elif event.type == PG.KEYDOWN and event.key == PG.K_RIGHT:
                self.sound.play()
                self.IMAGE = QUIT
            elif event.type == PG.KEYDOWN and event.key == PG.K_RETURN:
                #Reset Music
                if PX.music.get_busy():
                    PX.music.stop()
                Globals.STATE = High_Scores()
        elif self.IMAGE == BRIGHT:
            if event.type == PG.KEYDOWN and event.key == PG.K_LEFT:
                self.sound.play()
                self.IMAGE = QUIT
            elif event.type == PG.KEYDOWN and event.key == PG.K_RIGHT:
                self.sound.play()
                self.IMAGE = VOLUME
            elif event.type == PG.KEYDOWN and event.key == PG.K_RETURN:
                Globals.STATE = Bright_Menu()
        elif self.IMAGE == VOLUME:
            if event.type == PG.KEYDOWN and event.key == PG.K_LEFT:
                self.sound.play()
                self.IMAGE = BRIGHT
            elif event.type == PG.KEYDOWN and event.key == PG.K_RIGHT:
                self.sound.play()
                self.IMAGE = PLAY
            elif event.type == PG.KEYDOWN and event.key == PG.K_RETURN:
                Globals.STATE = Volume_Menu()
               
class High_Scores(State):
    IMAGE = HIGH_SCORES
    def __init__(self):
        self.sound = PX.Sound("Sounds/effects/Beeps.ogg")
        self.sound.set_volume(Globals.VOLUME)
        self.sound.play()
        State.__init__(self)
    def render(self):
        screen.blit(self.IMAGE, (0, 0))
        PDI.flip()
        if not PX.music.get_busy():
            PX.music.load(HIGHSONG)
            PX.music.play(0, 0.0)
    def event(self, event):
        if event.type == PG.KEYDOWN and event.key == PG.K_ESCAPE:
            #Reset Music
            if PX.music.get_busy():
                PX.music.stop()
            Globals.STATE = Menu()

class Bright_Menu(State):
    IMAGE = BRIGHT_MENU
    def __init__(self):
        self.sound = PX.Sound("Sounds/effects/Beeps.ogg")
        self.sound.set_volume(Globals.VOLUME)
        self.sound.play()
        State.__init__(self)
    def render(self):
        screen.blit(self.IMAGE, (0, 0))
        PDI.flip()
    def event(self, event):
        if event.type == PG.KEYDOWN and event.key == PG.K_ESCAPE:
            Globals.STATE = Menu()
        elif event.type == PG.KEYDOWN and event.key == PG.K_RIGHT:
            Globals.BRIGHTNESS += 0.1
            PDI.set_gamma(Globals.BRIGHTNESS)
        elif event.type == PG.KEYDOWN and event.key == PG.K_LEFT:
            if Globals.BRIGHTNESS > 0.0:
                Globals.BRIGHTNESS -= 0.1
                PDI.set_gamma(Globals.BRIGHTNESS)

class Volume_Menu(State):
    IMAGE = VOLUME_MENU
    def __init__(self):
        self.sound = PX.Sound("Sounds/effects/Beeps.ogg")
        self.sound.set_volume(Globals.VOLUME)
        State.__init__(self)
    def render(self):
        screen.blit(self.IMAGE, (0, 0))
        PDI.flip()
    def event(self, event):
        if event.type == PG.KEYDOWN and event.key == PG.K_ESCAPE:
            Globals.STATE = Menu()
        elif event.type == PG.KEYDOWN and event.key == PG.K_RIGHT:
            if Globals.VOLUME < 1.0:
                Globals.VOLUME += 0.1
                self.sound.set_volume(Globals.VOLUME)
                PX.music.set_volume(Globals.VOLUME)
                self.sound.play()
        elif event.type == PG.KEYDOWN and event.key == PG.K_LEFT:
            if Globals.VOLUME > 0.0:
                Globals.VOLUME -= 0.1
                self.sound.set_volume(Globals.VOLUME)
                PX.music.set_volume(Globals.VOLUME)
                self.sound.play()
            
class Win(State):
    IMAGE = WIN
    def __init__(self, level_num):
        self.sound = PX.Sound("Sounds/effects/win_sound.ogg")
        self.sound.set_volume(Globals.VOLUME)
        self.sound.play()
        self.level_num = level_num
        State.__init__(self)
    def render(self):
        if PX.music.get_busy():
            PX.music.stop()
        screen.blit(self.IMAGE, (0, 0))
        PDI.flip()
    def event(self, event):
        if event.type == PG.KEYDOWN:
            if self.level_num == LEVEL0:
                Globals.STATE = Game(LEVEL1, None)
            elif self.level_num == LEVEL1:
                Globals.STATE = Game(LEVEL2, None)
            elif self.level_num == LEVEL2:
                Globals.STATE = Game(LEVEL3, None)
            elif self.level_num == LEVEL3:
                Globals.STATE = Game(LEVEL4, None)
            else:
                Globals.STATE = Menu()
            
class Lose(State):
    IMAGE = LOSE
    def __init__(self, this_player):
        self.sound = PX.Sound("Sounds/effects/lose.ogg")
        self.sound.set_volume(Globals.VOLUME)
        self.sound.play()
        self.curr_player = this_player
        State.__init__(self)
    def render(self):
        if PX.music.get_busy():
            PX.music.stop()
        CONT_IMAGE = PI.load(CONTINUE + str(self.curr_player.get_continues()) + ".png").convert_alpha()
        screen.blit(self.IMAGE, (0, 0))
        screen.blit(CONT_IMAGE, (0, 0))
        PDI.flip()
    def event(self, event):
        if event.type == PG.KEYDOWN and event.key == PG.K_y and self.curr_player.get_continues() > 0:
            self.curr_player.subtract_continue()
            Globals.STATE = Game(Globals.LASTLEVEL, self.curr_player)
        elif event.type == PG.KEYDOWN and (event.key == PG.K_y or event.key == PG.K_n):
            Globals.STATE = Game(Globals.LASTLEVEL, None)
        elif event.type == PG.KEYDOWN and event.key == PG.K_ESCAPE:
            Globals.STATE = Menu()
            
class Game(State):
    player_group = None
    current_level = None
##    enemy_group = None
##    platform_group = None
    #Player movement bools
    PLAYER_X_POS = False
    PLAYER_X_NEG = False
    PLAYER_Y_POS = False
    PLAYER_Y_NEG = False
    SELECTEDWEAPON = -1
    ATTACK = False
    CROUCH = False
    USING = False
    TOOLS = -1
    scroll = 0

    def __init__(self, level_name, existing_player):
        #Make a new player
        if existing_player == None:
            self.new_player = player.Player(WIDTH, HEIGHT, Globals.VOLUME, level_name)
        else:
            self.new_player = existing_player
            self.new_player.resurrect()
            print "Continuing"
            
        Globals.ALIVE = True
        #Sound
        self.new_player.set_sound("Sounds/effects/sound.ogg")
        #Player group
        self.player_group = PS.Group()
        self.player_group.add(self.new_player)
        #UI group
        self.health_ui = ui.UI(WIDTH, HEIGHT, True, False, False)
        self.bones_ui = ui.UI(WIDTH, HEIGHT, False, False, False)
        self.weapon_ui = ui.UI(WIDTH, HEIGHT, False, True, False)
        self.hits_ui = ui.UI(WIDTH, HEIGHT, False, False, True)
        self.ui_group = PS.Group()
        self.ui_group.add(self.health_ui)
        self.ui_group.add(self.bones_ui)
        self.ui_group.add(self.weapon_ui)
        self.ui_group.add(self.hits_ui)
        #Set the level
        self.level_num = level_name
        print "Loading stage..."
        self.current_level = level.Level(level_name, Globals.VOLUME)
        Globals.LASTLEVEL = level_name

        #Load any progress the player has made through the level
        i = 1
        while i<= self.new_player.get_load_progress():
            self.current_level.load_file(level_name + "_" +  str(i) + ".txt")
            print "Loading stage part " + str(i)
            i = i+1

        #Move the player to the last checkpoint
        if existing_player:
            #self.new_player.set_move_to_check(True)
            self.current_level.set_last_check(Globals.LASTCHECK)
            self.current_level.scroll_auto(Globals.LASTCHECK[0], \
                                           Globals.LASTCHECK[1])
            self.new_player.go_to_check()
    def render(self):
        #Music
        if not PX.music.get_busy():
            if Globals.CURRENTSONG == HIGHSONG:
                PX.music.load(HIGHSONG)
                Globals.CURRENTSONG = SONG1
            elif Globals.CURRENTSONG == SONG1:
                PX.music.load(SONG1)
                Globals.CURRENTSONG = SONG0
            elif Globals.CURRENTSONG == SONG0:
                PX.music.load(SONG0)
                Globals.CURRENTSONG = HIGHSONG
            PX.music.set_volume(Globals.VOLUME)
            PX.music.play(0, 0.0)
        lasttime = PT.get_ticks()
        #screen.fill(BLACK)
        self.current_level.draw(screen, self.player_group)
            
        self.player_group.draw(screen)
        self.ui_group.draw(screen)
        
        clock.tick()
        PDI.flip()
        elapsed = (PT.get_ticks() - lasttime) / 1000.0
        if elapsed > 2.0:
            elapsed = 2.0

        #Update Player and Enemy
        while elapsed >= 0 and Globals.ALIVE:
            self.player_group.update(INTERVAL, self.PLAYER_X_POS, self.PLAYER_X_NEG, self.PLAYER_Y_POS, \
                                     self.PLAYER_Y_NEG, self.SELECTEDWEAPON, self.ATTACK, self.CROUCH, \
                                     self.USING, self.TOOLS, self.current_level)
            Globals.ALIVE = self.new_player.is_alive()
            self.current_level.update(INTERVAL, self.player_group)
            self.ui_group.update(self.new_player)
            elapsed -= INTERVAL
            if self.new_player.get_win():
                Globals.STATE = Win(self.level_num)
            self.USING = False
        
        #Reset jump status
        for this_player in self.player_group:
            if not this_player.on_ladder():
                self.PLAYER_Y_POS = False

        #Reset ladder status
        self.TOOLS = -1

        #Check to see if the player is alive
        if not Globals.ALIVE:
            while elapsed >= 0:
                self.new_player.die(INTERVAL)
                elapsed -= INTERVAL
            if self.new_player.finishedDying():
                #Reset Music
                if PX.music.get_busy():
                    PX.music.stop()
                Globals.LASTCHECK = self.current_level.get_last_check()
                Globals.STATE = Lose(self.new_player)
        
    def event(self, event):
        if event.type == PG.KEYDOWN and event.key == PG.K_ESCAPE:
            #Reset Music
            if PX.music.get_busy():
                PX.music.stop()
            Globals.LEVEL = self
            Globals.STATE = Menu()
        elif event.type == PG.KEYDOWN and event.key == PG.K_RIGHT: self.PLAYER_X_POS = True
        elif event.type == PG.KEYDOWN and event.key == PG.K_LEFT: self.PLAYER_X_NEG = True
        elif event.type == PG.KEYDOWN and event.key == PG.K_UP: self.PLAYER_Y_POS = True
        elif event.type == PG.KEYDOWN and event.key == PG.K_SPACE: self.PLAYER_Y_POS = True
        elif event.type == PG.KEYDOWN and event.key == PG.K_DOWN: self.CROUCH = True
        elif event.type == PG.KEYUP and event.key == PG.K_RIGHT: self.PLAYER_X_POS = False
        elif event.type == PG.KEYUP and event.key == PG.K_LEFT: self.PLAYER_X_NEG = False
        elif event.type == PG.KEYUP and event.key == PG.K_UP: self.PLAYER_Y_POS = False
        elif event.type == PG.KEYUP and event.key == PG.K_DOWN: self.CROUCH = False
        elif event.type == PG.KEYDOWN and event.key == PG.K_1: self.TOOLS = LADDER_INDEX
        elif event.type == PG.KEYUP and event.key == PG.K_1: self.TOOLS = INVALID_WEAPON_INDEX
        elif event.type == PG.KEYDOWN and event.key == PG.K_2: self.SELECTEDWEAPON = HAMMER_INDEX
        elif event.type == PG.KEYUP and event.key == PG.K_2: self.SELECTEDWEAPON = INVALID_WEAPON_INDEX
        elif event.type == PG.KEYDOWN and event.key == PG.K_3: self.TOOLS = BRIDGE_INDEX
        elif event.type == PG.KEYUP and event.key == PG.K_3: self.TOOLS = INVALID_WEAPON_INDEX
        elif event.type == PG.KEYDOWN and event.key == PG.K_q: self.TOOLS = CANCEL_WEAPON_INDEX
        elif event.type == PG.KEYUP and event.key == PG.K_q: self.TOOLS = INVALID_WEAPON_INDEX
##        elif event.type == PG.KEYDOWN and event.key == PG.K_LCTRL: self.ATTACK = True
##        elif event.type == PG.KEYUP and event.key == PG.K_LCTRL: self.ATTACK = False
        elif event.type == PG.KEYDOWN and event.key == PG.K_z:
            self.USING = True
            self.ATTACK = True
            self.TOOLS = MAKE_WEAPON_INDEX
        elif event.type == PG.KEYUP and event.key == PG.K_z:
            self.TOOLS = INVALID_WEAPON_INDEX
            self.ATTACK = False
        

Globals.STATE = Title()

#Clock
clock = PT.Clock()

#Main loop
while Globals.RUNNING:

    Globals.STATE.render()
    
    for event in PE.get():
        #Quit
        if event.type == PG.QUIT: Globals.RUNNING = False
        else:
            Globals.STATE.event(event)
            
