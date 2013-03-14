import pygame.sprite as PS
import pygame.image as PI
import player

class UI(PS.Sprite):
    IMAGES = None
    health = None
    weapon_select = None
    def __init__(self, surf_width, surf_height, is_health, weapon_select, hits):
        self.health = is_health
        self.weapon_select = weapon_select
        self.hits = hits
        PS.Sprite.__init__(self)
        if not UI.IMAGES:
            self.load_images()
        self.image = self.IMAGES[0]
        self.rect = self.image.get_rect()
        self.surf_height = surf_height
        self.surf_width = surf_width
        if self.weapon_select:
            self.rect.centery = 600-(self.rect.height/2)
            self.rect.centerx = self.rect.width/2
        #initialize location of UI
        elif self.health:
            self.rect.centery = self.rect.height/2
            self.rect.centerx = self.rect.width/2
        elif self.hits:
            self.rect.centery = 600-(self.rect.height/2)
            self.rect.centerx = self.surf_width - self.rect.width/2
        else:
            self.rect.centery = self.rect.height/2
            self.rect.centerx = self.surf_width - self.rect.width/2

    def load_images(self):
        weapon_select_image = PI.load("weapon_select.png").convert_alpha()
        self.IMAGES = []
        image1 = PI.load("UI/health/5.png").convert_alpha()
        image2 = PI.load("UI/health/4.png").convert_alpha()
        image3 = PI.load("UI/health/3.png").convert_alpha()
        image4 = PI.load("UI/health/2.png").convert_alpha()
        image5 = PI.load("UI/health/1.png").convert_alpha()
        image0 = PI.load("UI/health/0.png").convert_alpha()
        bone0 = PI.load("UI/bones/0.png").convert_alpha()
        bone1 = PI.load("UI/bones/1.png").convert_alpha()
        bone2 = PI.load("UI/bones/2.png").convert_alpha()
        bone3 = PI.load("UI/bones/3.png").convert_alpha()
        bone4 = PI.load("UI/bones/4.png").convert_alpha()
        bone5 = PI.load("UI/bones/5.png").convert_alpha()
        bone6 = PI.load("UI/bones/6.png").convert_alpha()
        bone7 = PI.load("UI/bones/7.png").convert_alpha()
        bone8 = PI.load("UI/bones/8.png").convert_alpha()
        bone9 = PI.load("UI/bones/9.png").convert_alpha()
        bone10 = PI.load("UI/bones/10.png").convert_alpha()
        hammer1 = PI.load("UI/hammer/hits5.png").convert_alpha()
        hammer2 = PI.load("UI/hammer/hits4.png").convert_alpha()
        hammer3 = PI.load("UI/hammer/hits3.png").convert_alpha()
        hammer4 = PI.load("UI/hammer/hits2.png").convert_alpha()
        hammer5 = PI.load("UI/hammer/hits1.png").convert_alpha()
        hammer6 = PI.load("UI/hammer/hits0.png").convert_alpha()
        if self.weapon_select:
            self.IMAGES.append(weapon_select_image)
        elif self.hits:
            self.IMAGES.append(hammer1)
            self.IMAGES.append(hammer2)
            self.IMAGES.append(hammer3)
            self.IMAGES.append(hammer4)
            self.IMAGES.append(hammer5)
            self.IMAGES.append(hammer6)
        elif self.health:
            self.IMAGES.append(image1)
            self.IMAGES.append(image2)
            self.IMAGES.append(image3)
            self.IMAGES.append(image4)
            self.IMAGES.append(image5)
        else:
            self.IMAGES.append(bone0)
            self.IMAGES.append(bone1)
            self.IMAGES.append(bone2)
            self.IMAGES.append(bone3)
            self.IMAGES.append(bone4)
            self.IMAGES.append(bone5)
            self.IMAGES.append(bone6)
            self.IMAGES.append(bone7)
            self.IMAGES.append(bone8)
            self.IMAGES.append(bone9)
            self.IMAGES.append(bone10)


    def update(self, player):
        if self.weapon_select:
            self.image = self.IMAGES[0]
        elif self.health:
            if player.get_health() >= 5:
                self.image = self.IMAGES[0]
            elif player.get_health() == 4:
                self.image = self.IMAGES[1]
            elif player.get_health() == 3:
                self.image = self.IMAGES[2]
            elif player.get_health() == 2:
                self.image = self.IMAGES[3]
            elif player.get_health() == 1:
                self.image = self.IMAGES[4]
            elif player.get_health() == 0:
                self.image = self.IMAGES[4]
        elif self.hits:
            if player.get_weapon_index() < 0:
                self.image = self.IMAGES[5]
            elif player.get_num_attacks() == 5:
                self.image = self.IMAGES[0]
            elif player.get_num_attacks() == 4:
                self.image = self.IMAGES[1]
            elif player.get_num_attacks() == 3:
                self.image = self.IMAGES[2]
            elif player.get_num_attacks() == 2:
                self.image = self.IMAGES[3]
            elif player.get_num_attacks() == 1:
                self.image = self.IMAGES[4]
        else:
            if player.get_bones() == 0:
                self.image = self.IMAGES[0]
            elif player.get_bones() == 1:
                self.image = self.IMAGES[1]
            elif player.get_bones() == 2:
                self.image = self.IMAGES[2]
            elif player.get_bones() == 3:
                self.image = self.IMAGES[3]
            elif player.get_bones() == 4:
                self.image = self.IMAGES[4]
            elif player.get_bones() == 5:
                self.image = self.IMAGES[5]
            elif player.get_bones() == 6:
                self.image = self.IMAGES[6]
            elif player.get_bones() == 7:
                self.image = self.IMAGES[7]
            elif player.get_bones() == 8:
                self.image = self.IMAGES[8]
            elif player.get_bones() == 9:
                self.image = self.IMAGES[9]
            elif player.get_bones() == 10:
                self.image = self.IMAGES[10]
        
                
