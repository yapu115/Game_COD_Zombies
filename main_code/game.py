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
from enviorment import Door, BunkerDoor, Resource, Juggernog, QuickRevive, SpeedCola, DoubleTap

import threading


class Game:
    def __init__(self) -> None:
        pygame.init()   
        # Screen
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.name = pygame.display.set_caption("Testing")

        # Background
        self.background = funciones.insert_image(r"SpriteSheets\backgrounds\Background.jpg", WIDTH, HEIGHT)
        self.rect_background = self.background.get_rect()

        self.starting_room = funciones.insert_image(r"SpriteSheets\backgrounds\trees3.png", 6500, 1000)
        self.rect_starting_room = funciones.insert_rect(self.starting_room, 1300 , 150)

        self.bunker_one = funciones.insert_image(r"SpriteSheets\backgrounds\bunker_one_bg.png", 1812, 550)
        self.rect_bunker_one = funciones.insert_rect(self.bunker_one, 70 , HEIGHT + 225)

        self.bunker_two = funciones.insert_image(r"SpriteSheets\backgrounds\bunker_two_bg.png", 682, 550)
        self.rect_bunker_two = funciones.insert_rect(self.bunker_two, -1250 , HEIGHT + 260)

        self.bunker_three = funciones.insert_image(r"SpriteSheets\backgrounds\bunker_three_bg.png", 860, 550)
        self.rect_bunker_three = funciones.insert_rect(self.bunker_three, 1360 , HEIGHT + 240)

        self.bunker_four = funciones.insert_image(r"SpriteSheets\backgrounds\bunker_four_bg.png", 1000, 650)
        self.rect_bunker_four = funciones.insert_rect(self.bunker_four, 2400 , HEIGHT + 220)

        self.clock = pygame.time.Clock()

        self.block_size = 32

        # Mechanics
        self.round = 0
        self.round_image = None
        self.round_rect = (10, HEIGHT - 70)
        self.round_changing = True

        self.changing_round_time = 6000
        self.changing_round_start = 6000 #pygame.time.get_ticks()

        self.power_on = False

        # HUD
        self.blood_points = funciones.insert_image(r"SpriteSheets\HUD\Points_blood.png", 34, 10)
        self.blood_points = pygame.transform.scale2x(self.blood_points)
        self.blood_points_rect = funciones.insert_rect(self.blood_points, 50, HEIGHT - 100)
        # Player
        self.player = Player(400, HEIGHT - 20, 27, 58, 2)

        
        self.font = pygame.font.SysFont("inkfree", 25)

        # Zombies
        self.zombies = []
        
        # Enviorment
        self.truck = funciones.insert_image(r"SpriteSheets\Enviorment\Truck.png", 369, 160)
        self.truck = pygame.transform.scale2x(self.truck)
        self.rect_truck = funciones.insert_rect(self.truck, -1400, HEIGHT - 180)
        self.truck.set_colorkey((44, 106, 138))

        self.fire_truck = funciones.insert_image(r"SpriteSheets\Enviorment\Fire_Truck.png", 164 * 1.5 , 64 * 1.5)
        self.fire_truck = pygame.transform.scale2x(self.fire_truck)
        self.rect_fire_truck = funciones.insert_rect(self.fire_truck, 4000, HEIGHT - 125)
        self.fire_truck.set_colorkey((255, 255, 255))

        self.power_switch = funciones.insert_image(r"SpriteSheets\Resources\power_switch.png", 70, 150)
        self.rect_power_switch = funciones.insert_rect(self.power_switch, 2800, -250)


        # Kitchen
        self.enviorment = []
        
        self.kitchen_down_furniture = Resource(350, 65, 1250, HEIGHT - 65, r"SpriteSheets\Enviorment\furniture.png")
        self.kitchen_up_furniture = Resource(350, 60, 1250, HEIGHT - 170, r"SpriteSheets\Enviorment\furniture2.png")
        self.refrigerator = Resource(50, 135, 1490, HEIGHT - 98, r"SpriteSheets\Enviorment\Refrigerator.png")

        self.enviorment.append(self.kitchen_down_furniture)
        self.enviorment.append(self.kitchen_up_furniture)
        self.enviorment.append(self.refrigerator)

        # Living

        coat_rack = Resource(192, 144, 1500, HEIGHT - 460, r"SpriteSheets\Enviorment\coat_rack.png")
        couch = Resource(144, 90, 2000, HEIGHT - 75, r"SpriteSheets\Enviorment\couch.png")
        mirror = Resource(93, 129, 2900, HEIGHT - 450, r"SpriteSheets\Enviorment\mirror.png")
        writing_01 = Resource(200, 150, 2700, HEIGHT - 150, r"SpriteSheets\Enviorment\writing_01.png")


        self.enviorment.append(couch)
        self.enviorment.append(mirror)
        self.enviorment.append(writing_01)

        # Doors

        self.doors = []

        door_kitchen = Door(900, HEIGHT - 105)        
        door_living = Door(1800, HEIGHT - 105)
        door_outside = Door(3000, HEIGHT - 105)
        door_upstairs = Door(1800, HEIGHT - 460)

        door_bunker = BunkerDoor(-self.block_size * 24, HEIGHT - 110)
        
        self.doors.append(door_kitchen)
        self.doors.append(door_living)
        self.doors.append(door_outside)
        self.doors.append(door_upstairs)
        self.doors.append(door_bunker)

        # perks

        quick_revive = QuickRevive(10, HEIGHT - 96)
        juggernog = Juggernog(500, HEIGHT + 432)
        speed_cola = SpeedCola(3700, HEIGHT - 115)
        double_tap = DoubleTap(1000, HEIGHT - 895)

        self.perks = [juggernog, quick_revive, speed_cola, double_tap]
        # Blocks

        #floor
        self.floor = [Block(i * self.block_size, HEIGHT - self.block_size, self.block_size) for i in range(-20, 140)]

        # Pre start
        for i in range(-70, -27):
           self.floor.append(Block(i * self.block_size, HEIGHT - self.block_size, self.block_size))

        # Second floor
        for i in range(40):
           self.floor.append(Block(887 + i * self.block_size, HEIGHT - 384, self.block_size))
        
        # Post kitchen stairs
        for i in range(19):
           self.floor.append(Block(2400 + i * self.block_size, HEIGHT - 384, self.block_size))

        # Third floor 
           #pre stairs
        for i in range(16):
           self.floor.append(Block(887 + i * self.block_size, HEIGHT - 832, self.block_size))
        
            #Post stairs
        for i in range(41):
          self.floor.append(Block(1664 + i * self.block_size, HEIGHT - 832, self.block_size))

        # Roof
        for i in range(66):
           self.floor.append(Block(887 + i * self.block_size, HEIGHT - 1344, self.block_size))
        

        # Bunker
        for i in range(-70, 140):
            self.floor.append(Block(i * self.block_size, HEIGHT + self.block_size * 16, self.block_size))

        self.offset_x = 0
        self.offset_y = 0
        self.scroll_area_width = 400
        self.scroll_area_height = 150


        # Walls
        
        self.walls = []

        # kitchen door
        for j in range(11):
            self.walls.append(Block(888, (HEIGHT - 195) - self.block_size // 2  * j, self.block_size - self.block_size // 2))
        
        # Living door
        for j in range(11):
            self.walls.append(Block(1785, (HEIGHT - 195) - self.block_size // 2  * j, self.block_size - self.block_size // 2))

        # Right house
        for j in range(73):
            self.walls.append(Block(2990, (HEIGHT - 195) - self.block_size // 2  * j, self.block_size - self.block_size // 2))
        
        #left house
        for j in range(43):
            self.walls.append(Block(888, (HEIGHT - 640) - self.block_size // 2  * j, self.block_size - self.block_size // 2))
        
        # Second floor
        for j in range(17):
            self.walls.append(Block(1785, (HEIGHT - 551) - self.block_size // 2  * j, self.block_size - self.block_size // 2))

            
        # Back house walls
        self.back_walls = []
        for j in range(40):
            self.back_walls.append([Wall_Stone(600 + (i * self.block_size), (HEIGHT - 64) - self.block_size * j, self.block_size) for i in range(9, 75)])

        for j in range(10):
            self.back_walls.append([Block(2149 + (i * self.block_size), (HEIGHT - 64) - self.block_size * j, self.block_size) for i in range(1, 10 - j)])
        
        for j in range(13):
            self.back_walls.append([Block(1582 + (i * self.block_size), (HEIGHT - self.block_size * 25) + self.block_size * j, self.block_size) for i in range(1 - j, 1)])
        
        for j in range(21):
            self.back_walls.append([Block(-928 + (i * self.block_size), (HEIGHT + self.block_size * 16) - self.block_size * j, self.block_size) for i in range(1, 18 - j)])

        self.stairs = []


        # Living
        for i in range(12):
            self.stairs.append(Block(2500 + (-i * self.block_size ), HEIGHT - self.block_size - (i * self.block_size), self.block_size))
        
        # Second floor
        for i in range(13):
            self.stairs.append(Block(1200 + (i * self.block_size), HEIGHT - (self.block_size * 13) - (i * self.block_size), self.block_size))
        
        # Bunker
        for i in range(17):
            self.stairs.append(Block(-352 + (-i * self.block_size), HEIGHT + self.block_size * 16 - (i * self.block_size), self.block_size))


        self.stair_floor = []
        # Kitchen
        for i in range(8):
           self.stair_floor.append(Block(2180 + i * self.block_size, HEIGHT - self.block_size * 12, self.block_size))

        # Bunker
        for i in range(8):
            self.stair_floor.append(Block(-self.block_size * 28 + i * self.block_size, HEIGHT - 32, self.block_size))

        # Third floor
        for i in range(5):
            self.stair_floor.append(Block(1500 + i * self.block_size, HEIGHT - self.block_size * 26, self.block_size))


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
                        if not self.player.gun.reloading:
                            self.player.gun.fire = True

                    if event.key == pygame.K_e:
                        for door in self.doors:
                            if (self.player.rect.colliderect((door.rect.x - 30, door.rect.y, door.rect.width, door.rect.height))) or (
                            self.player.rect.colliderect((door.rect.x + 30, door.rect.y, door.rect.width, door.rect.height))):
                                if door.state == "closed" and self.player.score >= 550: #cambiar 750 por una variable propia de las doors
                                    door.state = "opened"
                                    self.player.score -= 550
                        if (self.player.rect.colliderect(self.rect_power_switch.x - 30, self.rect_power_switch.y, self.rect_power_switch.width, self.rect_power_switch.height)):
                            if not self.power_on:
                                self.power_on = True
                                print(self.power_on)

                    for perk in self.perks:
                        if (self.player.rect.colliderect(perk.rect)):
                            if event.key == pygame.K_q and perk not in self.player.perks and perk.available:
                                self.player.perks.append(perk)

            self.player.loop(FPS)
            self.handle_move(self.player, self.floor, self.stairs)

            

            if ((self.player.rect.right - self.offset_x >= WIDTH - self.scroll_area_width) and self.player.x_vel > 0) or (
                (self.player.rect.left - self.offset_x <= self.scroll_area_width) and self.player.x_vel < 0):
                #if self.player.sector == "second_floor" and self.player.rect.x > 2500 :
                #    pass
                #else:
                    self.offset_x += self.player.x_vel

            # drop
            if ((self.player.rect.top - self.offset_y >= HEIGHT - self.scroll_area_height) and self.player.y_vel > 0):
                self.offset_y += self.player.y_vel * 3

            # up
            elif (self.player.rect.bottom - self.offset_y <= self.scroll_area_height * 3):
                if self.player.y_vel < 0:
                    self.offset_y += self.player.y_vel 
                elif self.player.x_vel > 0:
                    self.offset_y -= self.player.x_vel
                else:
                    self.offset_y += self.player.x_vel

            self.draw()
            if len(self.zombies) == 0:
                self.round_changing = True
            
            if self.round_changing:
                self.update_round(self.round, self.changing_round_start)
            else:
                self.changing_round_start = pygame.time.get_ticks()

            print(self.player.life)
                
        pygame.quit()

    def draw(self):
        self.screen.blit(self.background, self.rect_background)
        self.screen.blit(self.bunker_one, (self.rect_bunker_one.x - self.offset_x, self.rect_bunker_one.y - self.offset_y))
        self.screen.blit(self.bunker_two, (self.rect_bunker_two.x - self.offset_x, self.rect_bunker_two.y - self.offset_y))
        self.screen.blit(self.bunker_three, (self.rect_bunker_three.x - self.offset_x, self.rect_bunker_three.y - self.offset_y))
        self.screen.blit(self.bunker_four , (self.rect_bunker_four.x - self.offset_x, self.rect_bunker_four.y - self.offset_y))
        self.screen.blit(self.starting_room, (self.rect_starting_room.x - self.offset_x, self.rect_starting_room.y - self.offset_y))

        for back_wall in self.back_walls:
            for block in back_wall:
                block.draw(self.screen, self.offset_x, self.offset_y)

        for obj in self.floor:
            obj.draw(self.screen, self.offset_x, self.offset_y)        
        
        for wall in self.walls:
            wall.draw(self.screen, self.offset_x, self.offset_y)  

        for stair in self.stairs:
            stair.draw(self.screen, self.offset_x, self.offset_y)
        

        for stair_floor_block in self.stair_floor:
            stair_floor_block.draw(self.screen, self.offset_x, self.offset_y)

        for perk in self.perks:
            perk.draw(self.screen, self.offset_x, self.offset_y)
            if not perk.always_available:
                if self.power_on:
                    perk.available = True
                else:
                    perk.available = False


        self.screen.blit(self.truck, (self.rect_truck.x - self.offset_x, self.rect_truck.y - self.offset_y))
        self.screen.blit(self.fire_truck, (self.rect_fire_truck.x - self.offset_x, self.rect_fire_truck.y - self.offset_y))
        self.screen.blit(self.power_switch, (self.rect_power_switch.x - self.offset_x, self.rect_power_switch.y - self.offset_y))
        
        for furniture in self.enviorment:
            furniture.draw(self.screen, self.offset_x, self.offset_y)
        
        for door in self.doors:
            door.draw(self.screen, self.offset_x, self.offset_y)
        #self.second_door.draw(self.screen, self.offset_x, self.offset_y)
                
        
        self.player.draw(self.screen, self.offset_x, self.offset_y)
        i = 10
        if not self.round_changing:
            for zombie in self.zombies:
                i += 100
                zombie.loop(FPS,i)
                self.handle_zombie_move(zombie, self.floor, self.stairs)
                zombie.die()
                if zombie.show:
                    zombie.draw(self.screen, self.offset_x, self.offset_y)
                else:
                    self.zombies.remove(zombie)

        score_text = self.font.render("{0}".format(self.player.score), True, (255, 255, 255))
        ammo_text = self.font.render("{0} / {1}".format(len(self.player.gun.charger_ammo), len(self.player.gun.spare_ammo)), True, (255, 255, 255))
        self.screen.blit(self.change_round(self.round), self.round_rect)
        self.screen.blit(self.blood_points, self.blood_points_rect)
        self.screen.blit(ammo_text, (1100, 600))
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

                player.on_stairs = False
                collided_objects.append(obj)
        
        player.gun.update_collide(self.walls, self.floor, self.doors, self.zombies, player, self.round_changing)
        for wall in self.walls:
            if pygame.sprite.collide_mask(player, wall): # Si chocan los dos rects
                if dy > 0:
                    player.rect.bottom = wall.rect.top # Si el personaje está cayendo el personaje queda arriba del objeto
                    player.landed()
                elif dy < 0:
                    player.rect.top = wall.rect.bottom # Si el personaje está saltando no lo sobrepasa
                    player.hit_head()
                
                collided_objects.append(wall)
        

        for stair_floor_block in self.stair_floor:
            if not player.looking_down and not player.looking_up:
                if player.rect.colliderect(stair_floor_block.rect) and player.rect.y < stair_floor_block.rect.y - 70:
                    player.rect.bottom = stair_floor_block.rect.top
                    player.landed()
                    player.on_stairs = False

        player.use_stairs(stairs)
            
        return collided_objects
    
    def handle_zombie_vertical_condition(self, zombie, objects, stairs, dy):
        collided_objects = []
        for obj in objects:
            if pygame.sprite.collide_mask(zombie, obj): # Si chocan los dos rects
                if dy > 0:
                    zombie.rect.bottom = obj.rect.top # Si el personaje está cayendo el personaje queda arriba del objeto
                    zombie.landed()
                elif dy < 0:
                    zombie.rect.top = obj.rect.bottom # Si el personaje está saltando no lo sobrepasa
                    zombie.hit_head()
                
                zombie.on_stairs = False
                collided_objects.append(obj)
        
        for wall in self.walls:
            if pygame.sprite.collide_mask(zombie, wall): # Si chocan los dos rects
                if dy > 0:
                    zombie.rect.bottom = wall.rect.top # Si el personaje está cayendo el personaje queda arriba del objeto
                    zombie.landed()
                elif dy < 0:
                    zombie.rect.top = wall.rect.bottom # Si el personaje está saltando no lo sobrepasa
                    zombie.hit_head()
                
                collided_objects.append(wall)

        for stair_floor_block in self.stair_floor:
            if not zombie.looking_down and not zombie.looking_up:
                if zombie.rect.colliderect(stair_floor_block.rect) and zombie.rect.y < stair_floor_block.rect.y - 70:
                    zombie.rect.bottom = stair_floor_block.rect.top
                    zombie.landed()

            
        return collided_objects

    def collide(self, player, objects, dx):
        player.move(dx, 0)
        player.update()
        collided_object = None
        for obj in objects:
            if pygame.sprite.collide_mask(player, obj):
                collided_object = obj
                break
        
        for wall in self.walls:
            if pygame.sprite.collide_mask(player, wall):
                collided_object = wall
                break

        if player.rect.colliderect(self.rect_truck):
            collided_object = self.rect_truck

        if player.rect.colliderect(self.rect_fire_truck):
            collided_object = self.rect_fire_truck
        
        if player.rect.colliderect(self.rect_power_switch):
            collided_object = self.rect_power_switch

        for door in self.doors:
            if (player.rect.colliderect(door.rect) and door.state == "closed"):
                collided_object = door.rect

        player.move(-dx, 0)
        player.update()
        return collided_object

    def handle_move(self, player, objects, stairs):
        
        if player.rect.y < 200 and player.rect.y > -190:
            player.sector = "second_floor"
        elif player.rect.y < 520 and player.rect.y > 200:
            player.sector = "start"
        elif player.rect.y < 1000 and player.rect.y > 520:
            player.sector = "underground"

        keys = pygame.key.get_pressed()

        player.x_vel = 0
        collide_left = self.collide(player, objects, -PLAYER_VEL * 2)
        collide_right = self.collide(player, objects, PLAYER_VEL * 2)

        if player.being_revived:
            if keys[pygame.K_a] and not collide_left: 
                player.move_left(2)

            if keys[pygame.K_d] and not collide_right: 
                player.move_right(2)
        else:    
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
                player.angle = -20
            else:
                player.looking_down = False


        self.handle_vertical_condition(player, objects, stairs, player.y_vel)
    
    def handle_zombie_move(self, zombie, objects, stairs):
        if zombie.rect.y < 165 and zombie.rect.y > -190:
            zombie.sector = "second_floor"
        elif zombie.rect.y < 520 and zombie.rect.y > 140:
            zombie.sector = "start"
        elif zombie.rect.y < 1000 and zombie.rect.y > 520:
            zombie.sector = "underground"
        

        if not zombie.spawning:
            zombie.follow_player(self.player)
            
        if not zombie.spawning:
            self.handle_zombie_vertical_condition(zombie, objects, stairs, zombie.y_vel)


    def change_round(self, round):
        font = pygame.font.SysFont("javanesetext", 60) 
        if round == 0:
            round_image = round_image = funciones.insert_image(r"SpriteSheets\HUD\round_1.png", 85, 50)
        elif round < 11:
            round_image = funciones.insert_image(r"SpriteSheets\HUD\round_{0}.png".format(round), 85, 50)
        else:
            round_image = font.render("{0}".format(round), True, (255, 20, 60))
            self.round_rect = (10, HEIGHT - 100)
        
        return round_image

    def update_round(self, round, changing_round_start):
        passed_changing_round_time = pygame.time.get_ticks() - changing_round_start
        if passed_changing_round_time >= self.changing_round_time:
            self.round += 1
            zombies_num = 0
            zombies_vel = 0
            if self.round < 6:
                match(self.round):
                    case 1: 
                        zombies_num = 7
                        zombies_vel = 1
                    case 2:
                        zombies_num = 10
                        zombies_vel = 1.2
                    case 3:
                        zombies_num = 14
                        zombies_vel = 1.4
                    case 4:
                        zombies_num = 18
                        zombies_vel = 1.6
                    case 5:
                        zombies_num = 22
                        zombies_vel = 1.8
                    case 6:
                        zombies_num = 25
                        zombies_vel = 2
            else:
                zombies_num = self.round + 25 
                zombies_vel = 2.2

            self.zombies = [Zombie(300 + (100 * i), 100, 38, 57, zombies_vel) for i in range(zombies_num)]

        self.round_changing = False

new_game = Game()
new_game.run()