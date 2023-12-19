import pygame
import os
import random
import math
from os import listdir
from os.path import isfile, join
from Characters import Player, Zombie 
import funciones
from constants import *
from Objects import *
from enviorment import Door


class Game:
    def __init__(self) -> None:
        pygame.init()   
        # Screen
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.name = pygame.display.set_caption("Testing")

        # Background
        self.background = funciones.insert_image(r"SpriteSheets\backgrounds\Background.jpg", WIDTH, HEIGHT)
        self.rect_background = self.background.get_rect()

        self.starting_room = funciones.insert_image(r"SpriteSheets\backgrounds\trees2.png", 3000, HEIGHT)
        self.rect_starting_room = funciones.insert_rect(self.starting_room, 400 , 310)

        self.clock = pygame.time.Clock()

        # Player
        self.player = Player(100, HEIGHT - 96, 50, 50)

        # Zombies
        self.zombie = Zombie(300, 100, 50, 50)
        
        # Enviorment
        self.truck = funciones.insert_image(r"SpriteSheets\Enviorment\Truck.png", 369, 160)
        self.truck = pygame.transform.scale2x(self.truck)
        self.rect_truck = funciones.insert_rect(self.truck, -800, HEIGHT - 180)
        self.truck.set_colorkey((44, 106, 138))

        # Doors

        self.door = Door(300, HEIGHT - 105, 3, 3)

        # perks

        self.quick_revive = funciones.insert_image(r"SpriteSheets\Perks_machines\quick_revive.png", 70, 124)
        self.quick_revive.set_colorkey((255, 255, 255))
        self.rect_quick_revive = funciones.insert_rect(self.quick_revive, 0, HEIGHT - 96)
        
        # Blocks
        self.block_size = 32
        #floor
        #self.floor = [Block(i * self.block_size, HEIGHT - self.block_size, self.block_size) for i in range(-WIDTH // self.block_size , WIDTH * 2 // self.block_size)]
        self.floor = [Block(i * self.block_size, HEIGHT - self.block_size, self.block_size) for i in range(-100, 100)]

        self.offset_x = 0
        self.offset_y = 0
        self.scroll_area_width = 200
        self.scroll_area_height = 150

        # Walls
        self.walls = []
        for j in range(10):
            self.walls.append([Wall_Stone(i * self.block_size, (HEIGHT - 64) - self.block_size * j, self.block_size) for i in range(9, 60)])

        self.outside_walls = []

        self.upstairs_walls = []

        self.bunker_walls = []


    def run(self):
        running = True
        while running:
            self.clock.tick(FPS)
            events_list = pygame.event.get()
            for event in events_list:
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.player.jump()
                    
                    # Shooting
                    if event.key == pygame.K_f:
                        self.player.gun.fire = True

                    if event.key == pygame.K_e:
                        if self.player.rect.colliderect((self.door.rect.x - 30, self.door.rect.y, self.door.rect.width, self.door.rect.height)):
                            print("aaa")
                            if self.door.state == "opened":
                                self.door.state = "closed"
                            else:
                                self.door.state =  "opened"

            self.player.loop(FPS)
            self.zombie.loop(FPS)
            self.handle_move(self.player, self.floor)
            self.handle_zombie_move(self.zombie, self.floor)

            if ((self.player.rect.right - self.offset_x >= WIDTH - self.scroll_area_width) and self.player.x_vel > 0) or (
                (self.player.rect.left - self.offset_x <= self.scroll_area_width) and self.player.x_vel < 0):
                self.offset_x += self.player.x_vel

            # drop
            if ((self.player.rect.top - self.offset_y >= HEIGHT - self.scroll_area_height) and self.player.y_vel > 0):
                self.offset_y += self.player.y_vel * 3

            #jump
            elif (self.player.rect.bottom - self.offset_y <= self.scroll_area_height  and self.player.y_vel < 0):
                self.offset_y += self.player.y_vel 
            
            self.draw()

        pygame.quit()

    def draw(self):
        self.screen.blit(self.background, self.rect_background)
        self.screen.blit(self.starting_room, (self.rect_starting_room.x - self.offset_x, self.rect_starting_room.y - self.offset_y))
        for obj in self.floor:
            obj.draw(self.screen, self.offset_x, self.offset_y)        
        for wall in self.walls:
            for block in wall:
                block.draw(self.screen, self.offset_x, self.offset_y)
        
        self.screen.blit(self.truck, (self.rect_truck.x - self.offset_x, self.rect_truck.y - self.offset_y))
        self.screen.blit(self.quick_revive, (self.rect_quick_revive.x - self.offset_x, self.rect_quick_revive.y - self.offset_y))
        self.door.draw(self.screen, self.offset_x, self.offset_y)
        self.player.draw(self.screen, self.offset_x, self.offset_y)
        self.zombie.draw(self.screen, self.offset_x, self.offset_y)

        pygame.display.flip()


    def handle_vertical_condition(self, player, objects, dy):
        collided_objects = []
        for obj in objects:
            if pygame.sprite.collide_mask(player, obj): # Si chocan los dos rects
                if dy > 0:
                    player.rect.bottom = obj.rect.top # Si el personaje está cayendo el personaje queda arriba del objeto
                    player.landed()
                elif dy < 0:
                    player.rect.top = obj.rect.bottom # Si el personaje está saltando no lo sobrepasa
                    player.hit_head()

            collided_objects.append(obj)
            
        return collided_objects

    def collide(self, player, objects, dx):
        player.move(dx, 0)
        player.update()
        collided_object = None
        for obj in objects:
            if pygame.sprite.collide_mask(player, obj):
                collided_object = obj
                break
        
        if player.rect.colliderect(self.rect_truck):
            collided_object = self.rect_truck

        if player.rect.colliderect(self.door.rect) and self.door.state == "closed":
            collided_object = self.door.rect

        player.move(-dx, 0)
        player.update()
        return collided_object

    def handle_move(self, player, objects):
        keys = pygame.key.get_pressed()

        player.x_vel = 0
        collide_left = self.collide(player, objects, -PLAYER_VEL * 2)
        collide_right = self.collide(player, objects, PLAYER_VEL * 2)

        if keys[pygame.K_a] and not collide_left: 
            player.move_left(PLAYER_VEL)

        if keys[pygame.K_d] and not collide_right: 
            player.move_right(PLAYER_VEL)

        if keys[pygame.K_LSHIFT]:
            player.looking_up = True
            player.angle = 45
        else:
            player.looking_up = False

        if keys[pygame.K_RSHIFT]:
            player.looking_down = True
            player.angle = -45
        else:
            player.looking_down = False


        self.handle_vertical_condition(self.player, objects, player.y_vel)
    
    def handle_zombie_move(self, zombie, objects):
        #for zombie in zombies:
            if zombie.rect.colliderect(self.player.rect):
                pass
            else:
                if zombie.rect.x > self.player.rect.x:
                    zombie.move_left(1)
                else:
                    zombie.move_right(1)
                pass

            self.handle_vertical_condition(zombie, objects, zombie.y_vel)


    
new_game = Game()
new_game.run()