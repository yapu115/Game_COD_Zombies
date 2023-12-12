import pygame
import os
import random
import math
from os import listdir
from os.path import isfile, join
from Character import Player
import funciones
from constants import *
from Objects import *


class Game:
    def __init__(self) -> None:
        pygame.init()   
        # Screen
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.name = pygame.display.set_caption("Testing")

        # Background
        self.background = funciones.insertar_imagen("SpriteSheets\Background.jpg", WIDTH, HEIGHT)
        self.rect_background = self.background.get_rect()

        self.player = Player(100, 100, 50, 50)
        self.clock = pygame.time.Clock()
        
        # Blocks
        self.block_size = 32
        #floor
        self.floor = [Block(i * self.block_size, HEIGHT - self.block_size, self.block_size) for i in range(-WIDTH // self.block_size , WIDTH * 2 // self.block_size)]

        self.offset_x = 0
        self.offset_y = 0
        self.scroll_area_width = 200
        self.scroll_area_height = 150

        # Walls
        self.walls = []
        #self.walls = [Wall_Stone(i * self.block_size, HEIGHT - self.block_size * 2, self.block_size) for i in range(-WIDTH // self.block_size , WIDTH * 2 // self.block_size)]
        for j in range(30):
            self.walls.append([Wall_Stone(i * self.block_size, (HEIGHT - 64) - self.block_size * j, self.block_size) for i in range(-WIDTH // self.block_size, WIDTH * 2 // self.block_size)])

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

            self.player.loop(FPS)
            self.handle_move(self.player, self.floor)

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
        for obj in self.floor:
            obj.draw(self.screen, self.offset_x, self.offset_y)        
        for wall in self.walls:
            for block in wall:
                block.draw(self.screen, self.offset_x, self.offset_y)
        
        self.player.draw(self.screen, self.offset_x, self.offset_y)

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
            player.angulo = 45
        else:
            player.looking_up = False

        if keys[pygame.K_RSHIFT]:
            player.looking_down = True
            player.angulo = -45
        else:
            player.looking_down = False

        self.handle_vertical_condition(self.player, objects, player.y_vel)



    
new_game = Game()
new_game.run()