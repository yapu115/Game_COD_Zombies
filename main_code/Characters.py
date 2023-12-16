from typing import Any
from funciones import *
from os.path import isfile, join
from Guns import *
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

        self.front_arm = insert_image(r"SpriteSheets\MainCharacters\Nikolai\front_arm.png", 48, 12)
        self.back_arm = insert_image(r"SpriteSheets\MainCharacters\Nikolai\back_arm.png", 46, 14)

        self.back_arm_rect = insert_rect(self.back_arm, self.rect.x + 45, self.rect.y + 50)
        self.front_arm_rect = insert_rect(self.front_arm, self.rect.x + 45, self.rect.y + 50)

        self.looking_up = False
        self.looking_down = False

        self.angle = 0

        self.gun = M1911(self.front_arm_rect.x + 5, self.front_arm_rect.y + 5)

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
        self.front_arm = insert_image(r"SpriteSheets\MainCharacters\Nikolai\front_arm.png", 48, 12)
        self.back_arm = insert_image(r"SpriteSheets\MainCharacters\Nikolai\back_arm.png", 46, 14)

        if self.direction == "right":
            self.front_arm_rect = insert_rect(self.front_arm, self.rect.x + 45, self.rect.y + 50)
            self.back_arm_rect = insert_rect(self.back_arm, self.rect.x + 48, self.rect.y + 54)

            self.gun.direction = "right"
            self.gun.update(self.front_arm_rect.x + 35, self.front_arm_rect.y - 10)
        else: 
            self.front_arm = pygame.transform.flip(self.front_arm, True, False)
            self.back_arm = pygame.transform.flip(self.back_arm, True, False)

            self.front_arm_rect = insert_rect(self.back_arm, self.rect.x + 10, self.rect.y + 50)
            self.back_arm_rect = insert_rect(self.back_arm, self.rect.x + 8, self.rect.y + 53)

            self.gun.direction = "left"
            self.gun.update(self.front_arm_rect.x - 20, self.front_arm_rect.y - 10)

        
        if self.looking_up:                         # Esto se puede automatizar con parametros de entrada como el self.angulo para que on hayan tantos ifs
            if self.direction == "right":
                self.back_arm = pygame.transform.rotate(self.back_arm, self.angle)
                self.front_arm = pygame.transform.rotate(self.front_arm, self.angle)
            else:
                self.back_arm = pygame.transform.rotate(self.back_arm, -self.angle)
                self.front_arm = pygame.transform.rotate(self.front_arm, -self.angle)
            self.front_arm_rect.y = self.rect.y  + 10
            self.back_arm_rect.y = self.rect.y  + 10

        elif self.looking_down:
            if self.direction == "right":
                self.back_arm = pygame.transform.rotate(self.back_arm, self.angle)
                self.front_arm = pygame.transform.rotate(self.front_arm, self.angle)
            else:
                self.back_arm = pygame.transform.rotate(self.back_arm, -self.angle)
                self.front_arm = pygame.transform.rotate(self.front_arm, -self.angle)
               


    def update(self):
        self.rect = self.sprite.get_rect(topleft=(self.rect.x, self.rect.y)) # Se ajusta constantemente el rectangulo en la sprite
        self.mask = pygame.mask.from_surface(self.sprite) # Lo que permite el mask es que las colisionen funcionen con los pixeles del personaje y no con las del rectangulo

    def draw(self, screen, offset_x, offset_y):
        screen.blit(self.sprite, (self.rect.x - offset_x, self.rect.y - offset_y))
        screen.blit(self.back_arm, (self.back_arm_rect.x - offset_x, self.back_arm_rect.y - offset_y))
        self.gun.draw(screen, offset_x, offset_y)
        screen.blit(self.front_arm, (self.front_arm_rect.x - offset_x, self.front_arm_rect.y - offset_y))

        self.gun.shoot(screen, offset_x, offset_y)


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
