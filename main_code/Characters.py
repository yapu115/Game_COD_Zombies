from typing import Any

from pygame.sprite import Group
from funciones import *
from os.path import isfile, join
from Guns import *
import pygame
import time

class Character(pygame.sprite.Sprite):
    """
    Represents all characters in the game, for now the player and the zombies
    """
    GRAVITY = 1
    ANIMATION_DELAY = 5
    def __init__(self, x, y, width, height):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.x_vel = 0
        self.y_vel = 0

        self.mask = None
        self.animation_count = 0
        self.fall_count = 0
        self.jump_count = 0
        self.sprite = None
        self.score = 11500
        self.life = 1

        self.direction = "right"
        self.sector = "start"

        self.looking_up = False
        self.looking_down = False

        self.starting_time = time.time()

    def move(self, dx, dy): # Displaysment in x and displaysment in y
        """
        Represents the movement
        """
        self.rect.x += dx
        self.rect.y += dy
    
    def move_left(self, vel):
        """
        Moves the character to the left
        """
        self.x_vel = -vel
        if self.direction != "left":
            self.direction = "left"
            self.animation_count = 0

    def move_right(self, vel):
        """
        Moves the character to the right
        """
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

    def update(self):
        self.rect = self.sprite.get_rect(topleft=(self.rect.x, self.rect.y)) # Se ajusta constantemente el rectangulo en la sprite
        self.mask = pygame.mask.from_surface(self.sprite) # Lo que permite el mask es que las colisionen funcionen con los pixeles del personaje y no con las del rectangulo




class Player(Character):
    """
    Represents the player, who in the future will be 4 skins
    """
    SPRITES = load_sprite_sheets("MainCharacters", "Nikolai", 27, 58, True)

    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        # HUD
        self.life = 100
        self.top_life = 100
        self.lives = 1
        self.score = 11500
        self.perks = []

        # Animation
        self.front_arm = insert_image(r"SpriteSheets\MainCharacters\Nikolai\front_arm.png", 48, 12)
        self.back_arm = insert_image(r"SpriteSheets\MainCharacters\Nikolai\back_arm.png", 46, 14)

        self.back_arm_rect = insert_rect(self.back_arm, self.rect.x + 45, self.rect.y + 50)
        self.front_arm_rect = insert_rect(self.front_arm, self.rect.x + 45, self.rect.y + 50)

        self.angle = 0

        # Weapon
        self.gun = M1911(self.front_arm_rect.x + 5, self.front_arm_rect.y + 5)

        # Flags
        self.on_stairs = False
        self.being_attacked = False


    def jump(self):
        self.y_vel = -self.GRAVITY * 8
        self.animation_count = 0
        self.jump_count += 1
        if self.jump_count == 1:
            self.fall_count = 0


    def use_stairs(self, stairs):
        for stair in stairs:    
            if self.rect.colliderect(stair.rect):
                if self.looking_down or self.looking_up or self.on_stairs:
                    self.on_stairs = True
                    self.rect.bottom = stair.rect.top
                    self.landed()


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
        self.update_life()

    def update_life(self):
        passed_time = time.time() - self.starting_time
        if self.life < self.top_life and not self.being_attacked:
            if passed_time >= 5:
                self.life += 10
                self.starting_time = time.time()

    def update_perks(self, screen):
        for perk in self.perks:
            perk.activate(screen, self)
    
    def update_arm(self):
        self.front_arm = insert_image(r"SpriteSheets\MainCharacters\Nikolai\front_arm.png", 48, 12)
        self.back_arm = insert_image(r"SpriteSheets\MainCharacters\Nikolai\back_arm.png", 46, 14)


        if self.direction == "right":
            self.front_arm_rect = insert_rect(self.front_arm, self.rect.x + 45, self.rect.y + 50)
            self.back_arm_rect = insert_rect(self.back_arm, self.rect.x + 48, self.rect.y + 54)

            self.gun.direction = "right"
            self.gun.update(self.front_arm_rect.x + 33, self.front_arm_rect.y - 10)

        else: 
            self.front_arm = pygame.transform.flip(self.front_arm, True, False)
            self.back_arm = pygame.transform.flip(self.back_arm, True, False)

            self.front_arm_rect = insert_rect(self.back_arm, self.rect.x + 10, self.rect.y + 50)
            self.back_arm_rect = insert_rect(self.back_arm, self.rect.x + 8, self.rect.y + 53)

            self.gun.direction = "left"
            self.gun.update(self.front_arm_rect.x - 17, self.front_arm_rect.y - 10)
        

        if self.looking_up:
            if self.direction == "right":
                self.back_arm = pygame.transform.rotate(self.back_arm, self.angle)
                self.front_arm = pygame.transform.rotate(self.front_arm, self.angle)
                
                self.gun.image = pygame.transform.rotate(self.gun.image, self.angle)
                self.gun.rect.y = self.front_arm_rect.y - 50
                self.gun.rect.x = self.front_arm_rect.x + 25

                self.gun.looking_up = True

            else:
                self.back_arm = pygame.transform.rotate(self.back_arm, -self.angle)
                self.front_arm = pygame.transform.rotate(self.front_arm, -self.angle)
                
                self.gun.image = pygame.transform.rotate(self.gun.image, -self.angle)
                self.gun.rect.y = self.front_arm_rect.y - 50
                self.gun.rect.x = self.front_arm_rect.x - 15

                self.gun.looking_up = True
            self.front_arm_rect.y = self.rect.y  + 10
            self.back_arm_rect.y = self.rect.y  + 10

        else:
            self.gun.looking_up = False
            if self.looking_down:
                if self.direction == "right":
                    self.back_arm = pygame.transform.rotate(self.back_arm, self.angle)
                    self.front_arm = pygame.transform.rotate(self.front_arm, self.angle)

                    self.gun.image = pygame.transform.rotate(self.gun.image, self.angle)
                    self.gun.rect.y = self.front_arm_rect.y + 8
                    self.gun.rect.x = self.front_arm_rect.x + 32
                else:
                    self.back_arm = pygame.transform.rotate(self.back_arm, -self.angle)
                    self.front_arm = pygame.transform.rotate(self.front_arm, -self.angle) 
                    
                    self.gun.image = pygame.transform.rotate(self.gun.image, -self.angle)
                    self.gun.rect.y = self.front_arm_rect.y + 8
                    self.gun.rect.x = self.front_arm_rect.x - 20
                
                self.gun.looking_down = True
            else:
                self.gun.looking_down = False


    def draw(self, screen, offset_x, offset_y):
        screen.blit(self.sprite, (self.rect.x - offset_x, self.rect.y - offset_y))
        screen.blit(self.back_arm, (self.back_arm_rect.x - offset_x, self.back_arm_rect.y - offset_y))
        self.gun.draw(screen, offset_x, offset_y)
        screen.blit(self.front_arm, (self.front_arm_rect.x - offset_x, self.front_arm_rect.y - offset_y))

        self.update_perks(screen)
        self.gun.shoot()


class Zombie(Character):
    SPRITES = load_sprite_sheets("MainCharacters", "zombies", 38, 57, True)

    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.attack = False
        self.life = 70
        self.show = True

        self.using_stairs = False


    def move(self, dx, dy): # Displaysment in x and displaysment in y
        if self.attack is False:
            self.rect.x += dx
        self.rect.y += dy
    

    def go_upstairs(self, stairs_x, left_stairs, player):
        if player.rect.y > self.rect.y + 20:
            pass
        else:
            if left_stairs:
                if self.rect.x > stairs_x or self.using_stairs:
                    self.move_left(5)
                    self.looking_up = True
                    self.using_stairs = True
                else:
                    self.looking_up = False 
                    if not self.using_stairs:
                        self.move_right(5)
            else:
                pass

    def follow_player(self, player):
        if self.rect.colliderect(player.rect):
            self.attack = True
            self.attack_player(player)
        else:
            self.attack = False
            player.being_attacked = False
            if (self.sector != player.sector):
                match(self.sector):
                    case "start":
                        match(player.sector):
                            case "second_floor":
                                self.go_upstairs(2520, True, player)
            else:
                self.using_stairs = False
                self.looking_down = False
                self.looking_up = False
                if self.rect.x > player.rect.x:
                    self.move_left(5)
                else:
                    self.move_right(5)

    def update_sprite(self):
        sprite_sheet = "walk_2"
        if self.attack:
            sprite_sheet = "attack"

        sprite_sheet_name = sprite_sheet + "_" + self.direction
        sprites = self.SPRITES[sprite_sheet_name]

        sprite_index = (self.animation_count // self.ANIMATION_DELAY) % len(sprites) # Para regular la cantidad de tiempo que pasa entre frame y frame
        self.sprite = sprites[sprite_index]

        self.animation_count += 1 
        self.update()
        self.die()

    def draw(self, window, offset_x, offset_y):
        window.blit(self.sprite, (self.rect.x - offset_x, self.rect.y - offset_y))

    def attack_player(self, player):
        passed_time = time.time() - self.starting_time
        if passed_time >= 1.5:
            player.life -= 10
            player.being_attacked = True
            self.starting_time = time.time()

    def die(self):
        if self.life < 0:
            self.show = False
