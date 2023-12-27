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

        self.starting_room = funciones.insert_image(r"SpriteSheets\backgrounds\trees3.png", 6000, HEIGHT)
        self.rect_starting_room = funciones.insert_rect(self.starting_room, 1300 , 310)

        self.clock = pygame.time.Clock()

        # HUD
        self.blood_points = funciones.insert_image(r"SpriteSheets\HUD\Points_blood.png", 34, 10)
        self.blood_points = pygame.transform.scale2x(self.blood_points)
        self.blood_points_rect = funciones.insert_rect(self.blood_points, 50, HEIGHT - 100)
        # Player
        self.player = Player(100, HEIGHT - 10, 50, 50)

        
        #font_input = pygame.font.SysFont("Arial", TAMAÑO_LETRA)

        self.font = pygame.font.SysFont("calibri", 25)

        # Zombies
        self.zombies = [Zombie(300 * i, 100, 50, 50) for i in range(30)]
        
        # Enviorment
        self.truck = funciones.insert_image(r"SpriteSheets\Enviorment\Truck.png", 369, 160)
        self.truck = pygame.transform.scale2x(self.truck)
        self.rect_truck = funciones.insert_rect(self.truck, -500, HEIGHT - 180)
        self.truck.set_colorkey((44, 106, 138))

        self.fire_truck = funciones.insert_image(r"SpriteSheets\Enviorment\Fire_Truck.png", 164 * 1.5 , 64 * 1.5)
        self.fire_truck = pygame.transform.scale2x(self.fire_truck)
        self.rect_fire_truck = funciones.insert_rect(self.fire_truck, 4000, HEIGHT - 125)
        self.fire_truck.set_colorkey((255, 255, 255))

        # Doors

        self.door = Door(900, HEIGHT - 105, 3, 3)
        self.second_door = Door(1300, HEIGHT - 105, 3, 3)

        # perks

        self.quick_revive = funciones.insert_image(r"SpriteSheets\Perks_machines\quick_revive.png", 70, 124)
        self.quick_revive.set_colorkey((255, 255, 255))
        self.rect_quick_revive = funciones.insert_rect(self.quick_revive, 100, HEIGHT - 96)
        
        # Blocks
        self.block_size = 32
        #floor
        #self.floor = [Block(i * self.block_size, HEIGHT - self.block_size, self.block_size) for i in range(-WIDTH // self.block_size , WIDTH * 2 // self.block_size)]
        self.floor = [Block(i * self.block_size, HEIGHT - self.block_size, self.block_size) for i in range(-100, 140)]
        for i in range(20):
           self.floor.append(Block(887 + i * self.block_size, HEIGHT - 384, self.block_size))

        self.offset_x = 0
        self.offset_y = 0
        self.scroll_area_width = 200
        self.scroll_area_height = 150

        # Walls
        self.walls = []
        for j in range(10):
            self.walls.append([Wall_Stone(600 + (i * self.block_size), (HEIGHT - 64) - self.block_size * j, self.block_size) for i in range(9, 60)])

        for j in range(11):
            self.floor.append(Block(888, (HEIGHT - 195) - self.block_size // 2  * j, self.block_size - self.block_size // 2))
        
        self.stairs = []
        for i in range(23):
            self.stairs.append(Block(1870 + (-i * self.block_size * 0.5), HEIGHT - self.block_size - (i * self.block_size * 0.5), self.block_size))

        #for i in range(10):
        #    self.stairs.append([Block(1500 + (i * self.block_size), HEIGHT - self.block_size - (i * self.block_size * 0.5), self.block_size) for i in range(10)])

        # Hacer las paredes por separado y despues un append para unirlas todas en self.walls
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
                            if self.door.state == "closed" and self.player.score >= 750:
                                self.door.state = "opened"
                                self.player.score -= 750

            self.player.loop(FPS)
            self.handle_move(self.player, self.floor, self.stairs)
            for zombie in self.zombies:
                zombie.loop(FPS)
                self.handle_zombie_move(zombie, self.floor, self.stairs)
            

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

            x, y = pygame.mouse.get_pos()
            #print(x, y)
        pygame.quit()

    def draw(self):
        self.screen.blit(self.background, self.rect_background)
        self.screen.blit(self.starting_room, (self.rect_starting_room.x - self.offset_x, self.rect_starting_room.y - self.offset_y))
        for wall in self.walls:
            for block in wall:
                block.draw(self.screen, self.offset_x, self.offset_y)
        for obj in self.floor:
            obj.draw(self.screen, self.offset_x, self.offset_y)        
        for stair in self.stairs:
            stair.draw(self.screen, self.offset_x, self.offset_y)
        
        self.screen.blit(self.truck, (self.rect_truck.x - self.offset_x, self.rect_truck.y - self.offset_y))
        self.screen.blit(self.fire_truck, (self.rect_fire_truck.x - self.offset_x, self.rect_fire_truck.y - self.offset_y))
        self.screen.blit(self.quick_revive, (self.rect_quick_revive.x - self.offset_x, self.rect_quick_revive.y - self.offset_y))
        self.door.draw(self.screen, self.offset_x, self.offset_y)
        #self.second_door.draw(self.screen, self.offset_x, self.offset_y)
                
        
        self.player.draw(self.screen, self.offset_x, self.offset_y)
        for zombie in self.zombies:
            zombie.die()
            if zombie.show:
                zombie.draw(self.screen, self.offset_x, self.offset_y)
            else:
                self.zombies.remove(zombie)

        score_text = self.font.render("{0}".format(self.player.score), True, (255, 255, 255))
        self.screen.blit(self.blood_points, self.blood_points_rect)
        self.screen.blit(score_text, self.blood_points_rect)

        pygame.display.flip()


    def handle_vertical_condition(self, player, objects, stairs, dy):
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

        for stair in stairs:
            if player.rect.colliderect(stair):
                player.rect.bottom = stair.rect.top
                player.landed()            
            
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

        if player.rect.colliderect(self.rect_fire_truck):
            collided_object = self.rect_fire_truck

        if player.rect.colliderect(self.door.rect) and self.door.state == "closed":
            collided_object = self.door.rect

        player.move(-dx, 0)
        player.update()
        return collided_object

    def handle_move(self, player, objects, stairs):
        keys = pygame.key.get_pressed()

        player.x_vel = 0
        collide_left = self.collide(player, objects, -PLAYER_VEL * 2)
        collide_right = self.collide(player, objects, PLAYER_VEL * 2)

        if keys[pygame.K_a] and not collide_left: 
            player.move_left(PLAYER_VEL)

        if keys[pygame.K_d] and not collide_right: 
            player.move_right(PLAYER_VEL)

        if keys[pygame.K_LSHIFT] :
            player.looking_up = True
            player.angle = 40
        else:
            player.looking_up = False

        if keys[pygame.K_RSHIFT]:
            player.looking_down = True
            player.angle = -40
        else:
            player.looking_down = False


        self.handle_vertical_condition(player, objects, stairs, player.y_vel)
    
    def handle_zombie_move(self, zombie, objects, stairs):
        #for zombie in zombies:
            if zombie.rect.colliderect(self.player.rect):
                pass
            else:
                if zombie.rect.x > self.player.rect.x:
                    zombie.move_left(1)
                else:
                    zombie.move_right(1)
                pass

            self.handle_vertical_condition(zombie, objects, stairs, zombie.y_vel)
            self.zombies_damage(zombie, self.player)

    def zombies_damage(self, zombie, player):
        #try:
            for bullet in player.gun.ammo:
                if zombie.rect.colliderect(bullet.rect):
                    player.gun.ammo.remove(bullet)
                    zombie.life -= 30
                    print("disparo acertado")
                    print(zombie.life)
                    player.score += 20
                    print(player.score)
                    #except:
         #   print("a????????")

    
new_game = Game()
new_game.run()