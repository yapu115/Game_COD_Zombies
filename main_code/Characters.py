from typing import Any
from funciones import *
from os.path import isfile, join
import pygame

class Player(pygame.sprite.Sprite):
    BLOCK_COLOR = (255, 0, 0)
    GRAVITY = 1
    SPRITES = load_sprite_sheets("MainCharacters", "Nikolai", 27, 58, True)
    ANIMATION_DELAY = 5

    def __init__(self, x, y, width, height):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.x_vel = 0
        self.y_vel = 0
        self.mask = None
        self.direction = "left"
        self.animation_count = 0
        self.fall_count = 0
        self.jump_count = 0
        self.sprite = ""
        #self.arm_sprite = insertar_imagen(r"SpriteSheets\MainCharacters\Nikolai\hand.png", 45, 14)
        #self.arm_rect = insertar_rect(self.arm_sprite, self.rect.x + 10, self.rect.y + 50)
        self.looking_up = False
        self.looking_down = False

    def jump(self):
        self.y_vel = -self.GRAVITY * 8
        self.animation_count = 0
        self.jump_count += 1
        if self.jump_count == 1:
            self.fall_count = 0

    def move(self, dx, dy): # Displaysment in x and displaysment in y
        self.rect.x += dx
        self.rect.y += dy
    
    def move_left(self, vel):
        self.x_vel = -vel
        if self.direction != "left":
            self.direction = "left"
            self.animation_count = 0

    def move_right(self, vel):
        self.x_vel = vel
        if self.direction != "right":
            self.direction = "right"
            self.animation_count = 0

    def loop(self, fps):
        self.y_vel += min(1, (self.fall_count / fps) * self.GRAVITY) # la cuenta simboliza la cantidad de tiempo que llevo cayendo
        self.move(self.x_vel, self.y_vel)

        self.fall_count += 1
        self.update_sprite()

    def landed(self):
        self.fall_count = 0 # Le sacamos la gravedad de caida
        self.y_vel = 0
    
    def hit_head(self):
        self.fall_count = 0
        self.y_vel *= -1 

    def update_sprite(self):
        sprite_sheet = "stay"
        if self.x_vel != 0:
            sprite_sheet = "walk"
        
        sprite_sheet_name = sprite_sheet + "_" + self.direction
        sprites = self.SPRITES[sprite_sheet_name]

        sprite_index = (self.animation_count // self.ANIMATION_DELAY) % len(sprites) # Para regular la cantidad de tiempo que pasa entre frame y frame
        self.sprite = sprites[sprite_index]
        self.animation_count += 1 
        self.update()
        self.update_arm()

    def update_arm(self):
        self.arm_sprite = insertar_imagen(r"SpriteSheets\MainCharacters\Nikolai\hand.png", 45, 14)
        #self._front_arm = insertar_imagen(r"SpriteSheets\MainCharacters\Nikolai\front_arm.png", 45, 14)
        #self.back_arm = insertar_imagen(r"SpriteSheets\MainCharacters\Nikolai\back_arm.png", 45, 14)

        if self.direction == "right":
            self.arm_rect = insertar_rect(self.arm_sprite, self.rect.x + 45, self.rect.y + 50)
        else: 
            self.arm_sprite = pygame.transform.flip(self.arm_sprite, True, False)
            self.arm_rect = insertar_rect(self.arm_sprite, self.rect.x + 10, self.rect.y + 50)

        if self.looking_up:                         # Esto se puede automatizar con parametros de entrada como el self.angulo para que on hayan tantos ifs
            if self.direction == "right":
                self.arm_sprite = pygame.transform.rotate(self.arm_sprite, self.angulo)
                self.arm_rect.y = self.rect.y + 15 
            else:
                self.arm_sprite = pygame.transform.rotate(self.arm_sprite, -self.angulo)
                self.arm_rect.y = self.rect.y  + 15

        elif self.looking_down:
            if self.direction == "right":
                self.arm_sprite = pygame.transform.rotate(self.arm_sprite, self.angulo)
            else:
                self.arm_sprite = pygame.transform.rotate(self.arm_sprite, -self.angulo)
            

    def update(self):
        self.rect = self.sprite.get_rect(topleft=(self.rect.x, self.rect.y)) # Se ajusta constantemente el rectangulo en la sprite
        self.mask = pygame.mask.from_surface(self.sprite) # Lo que permite el mask es que las colisionen funcionen con los pixeles del personaje y no con las del rectangulo

    def draw(self, window, offset_x, offset_y):
        window.blit(self.sprite, (self.rect.x - offset_x, self.rect.y - offset_y))
        window.blit(self.arm_sprite, (self.arm_rect.x - offset_x, self.arm_rect.y - offset_y))
    



class Zombie(pygame.sprite.Sprite):
    BLOCK_COLOR = (255, 0, 0)
    GRAVITY = 1
    SPRITES = load_sprite_sheets("MainCharacters", "zombies", 41, 55, True)
    ANIMATION_DELAY = 5

    def __init__(self, x, y, width, height):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.x_vel = 0
        self.y_vel = 0
        self.mask = None
        self.direction = "left"
        self.animation_count = 0
        self.fall_count = 0
        self.jump_count = 0
        self.sprite = ""
        self.attack = False


    def move(self, dx, dy): # Displaysment in x and displaysment in y
        if self.attack is False:
            self.rect.x += dx
        self.rect.y += dy
    
    def move_left(self, vel):
        self.x_vel = -vel
        if self.direction != "left":
            self.direction = "left"
            self.animation_count = 0

    def move_right(self, vel):
        self.x_vel = vel
        if self.direction != "right":
            self.direction = "right"
            self.animation_count = 0

    def loop(self, fps):
        self.y_vel += min(1, (self.fall_count / fps) * self.GRAVITY) # la cuenta simboliza la cantidad de tiempo que llevo cayendo
        self.move(self.x_vel, self.y_vel)

        self.fall_count += 1
        self.update_sprite()

    def landed(self):
        self.fall_count = 0 # Le sacamos la gravedad de caida
        self.y_vel = 0
    
    def hit_head(self):
        self.fall_count = 0
        self.y_vel *= -1 

    def update_sprite(self):
        sprite_sheet = "walk"

        sprite_sheet_name = sprite_sheet + "_" + self.direction
        sprites = self.SPRITES[sprite_sheet_name]

        sprite_index = (self.animation_count // self.ANIMATION_DELAY) % len(sprites) # Para regular la cantidad de tiempo que pasa entre frame y frame
        self.sprite = sprites[sprite_index]
        self.animation_count += 1 
        self.update()

    def update(self):
        self.rect = self.sprite.get_rect(topleft=(self.rect.x, self.rect.y)) # Se ajusta constantemente el rectangulo en la sprite
        self.mask = pygame.mask.from_surface(self.sprite) # Lo que permite el mask es que las colisionen funcionen con los pixeles del personaje y no con las del rectangulo

    def draw(self, window, offset_x, offset_y):
        window.blit(self.sprite, (self.rect.x - offset_x, self.rect.y - offset_y))
