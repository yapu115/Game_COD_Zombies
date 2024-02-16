import pygame
from pygame.sprite import Group
from funciones import insert_image, insert_rect
import time


class Bullet(pygame.sprite.Sprite):
    def __init__(self, width, height, x, y, sprite):
        super().__init__()
        # Base
        self.sprite = sprite
        self.image = insert_image(sprite, width, height)
        self.height = height
        self.width = width
        self.rect = insert_rect(self.image, 1000, 1000)
        self.direction = "left"
        self.x = x
        self.y = y
        self.angle = 40
        
        # Flags
        self.on_air = False
        self.looking_up = False
        self.looking_down = False
        self.first_second = True
        self.hit = False


    def fire(self, screen, offset_x, offset_y, fire_velocity):
        if self.on_air :
            if self.first_second:
                self.rect = insert_rect(self.image, self.x, self.y)
                self.first_second = False
            screen.blit(self.image, (self.rect.x - offset_x, self.rect.y - offset_y))
            if self.direction == "left":
                if self.looking_up:
                    self.rect.x -= fire_velocity 
                    self.rect.y -= fire_velocity 
                elif self.looking_down:
                    self.rect.x -= fire_velocity 
                    self.rect.y += fire_velocity // 2
                else:
                    self.rect.x -= fire_velocity
            else:
                if self.looking_up:
                    self.rect.x += fire_velocity 
                    self.rect.y -= fire_velocity 
                elif self.looking_down:
                    self.rect.x += fire_velocity 
                    self.rect.y += fire_velocity // 2
                else:
                    self.rect.x += fire_velocity

    def update(self, x, y):
        self.image = insert_image(self.sprite, self.width, self.height)
        
        x_sum = 0
        y_sum = 0
        
        if self.direction == "right":
            self.image = pygame.transform.flip(self.image, True, False)
            x_sum = 10
            y_sum = 6
            if self.looking_up:
                self.image = pygame.transform.rotate(self.image, self.angle)
                y_sum = -30
            elif self.looking_down:
                self.image = pygame.transform.rotate(self.image, -self.angle)
                y_sum = 38
                x_sum = 30
        else:
            x_sum = 15
            y_sum = 6
            if self.looking_up:
                self.image = pygame.transform.rotate(self.image, -self.angle)
                y_sum = -40
            elif self.looking_down:
                self.image = pygame.transform.rotate(self.image, self.angle)
                y_sum = 40
                x_sum = -10
        
                 

        self.x = x + x_sum
        self.y = y + y_sum

class Gun(pygame.sprite.Sprite):

    def __init__(self, sprite, x, y, width, height, bullet_dmg, fire_velocity, reloading_speed):
        super().__init__()
        # Base
        self.sprite = sprite
        self.image = insert_image(self.sprite, width, height)
        self.rect = insert_rect(self.image, x, y)
        
        self.direction = "left"
        self.width = width
        self.height = height
        self.next_charger_bullet_index = -1
        self.next_shooted_bullet_index = -1

        # Bullets
        self.bullet_sprite = r"SpriteSheets\Guns\bullet.png"
        self.bullets_width = 8
        self.bullets_height = 4

        self.charger_ammo = []
        self.spare_ammo = []
        self.shooted_ammo = []

        self.total_charger_ammo = 0
        self.bullet_damage = bullet_dmg
        self.fire_velocity = fire_velocity
        self.reloading_speed = reloading_speed

        # times
        self.reloading_starting_time =  pygame.time.get_ticks()
        # Flags
        self.fire = False
        self.reloading = False
        self.looking_up = False
        self.looking_down = False

        # Arms alignment
        self.right_dir_x = 33
        self.left_dir_x = -17
        self.center_y = -10

        self.look_up_right_x = 25
        self.look_up_left_x = -15
        self.look_up_y = -50

        self.look_down_right_x = 32
        self.look_down_left_x = -20
        self.look_down_y = 8




    def draw(self, screen, offset_x, offset_y):
        for bullet in self.shooted_ammo:
            bullet.fire(screen, offset_x, offset_y, self.fire_velocity)
        screen.blit(self.image, (self.rect.x - offset_x, self.rect.y - offset_y))
            

    def update(self, x, y):
        self.image = insert_image(self.sprite, self.width, self.height)
        self.rect.x = x
        self.rect.y = y

        if self.direction == "left":
            self.image = pygame.transform.flip(self.image, True, False)

        for bullet in self.charger_ammo:
            bullet.direction = self.direction
            bullet.update(x, y)

            if self.looking_up:
                bullet.looking_up = True
            else:
                bullet.looking_up = False

            if self.looking_down:
                bullet.looking_down = True
            else:
                bullet.looking_down = False


    def charger_setup(self, charger_ammo, spare_ammo):
        self.charger_ammo = [Bullet(self.bullets_width, self.bullets_height, self.rect.x, self.rect.y, self.bullet_sprite) for i in range(charger_ammo)]
        self.spare_ammo = [Bullet(self.bullets_width, self.bullets_height,self.rect.x, self.rect.y, self.bullet_sprite) for i in range(spare_ammo)]
        self.total_charger_ammo = charger_ammo 
        self.next_charger_bullet_index = charger_ammo - 1

    def shoot(self):
        if self.charger_ammo:
            if self.fire:
                self.next_charger_bullet_index -= 1
                self.next_shooted_bullet_index += 1
                self.shooted_ammo.append(self.charger_ammo.pop(self.next_charger_bullet_index))
                self.shooted_ammo[self.next_shooted_bullet_index].on_air = True
                self.fire = False
                self.reloading_starting_time = pygame.time.get_ticks()
        else:
            self.reloading = True
            self.reload(self.reloading_starting_time)

    def reload(self, reloading_starting_time):
        passed_reloading_time =  pygame.time.get_ticks() - reloading_starting_time
        if self.spare_ammo:
            if (passed_reloading_time >= self.reloading_speed): 
                if len(self.spare_ammo) > self.total_charger_ammo:
                    for i in range(self.total_charger_ammo - len(self.charger_ammo)):
                        self.charger_ammo.append(self.spare_ammo.pop())
                    self.next_charger_bullet_index = self.total_charger_ammo - 1
                else:
                    spare_ammo_len = len(self.spare_ammo)
                    for i in range(spare_ammo_len):
                        self.charger_ammo.append(self.spare_ammo.pop())
                    self.next_charger_bullet_index = spare_ammo_len - 1 # para este punto el len ya es 0 asi que no funciona
                self.shooted_ammo.clear()
                self.next_shooted_bullet_index = -1
                self.reloading = False

    def update_collide(self, walls, floor, doors, zombies, player, round_change):
        for bullet in self.shooted_ammo:
            for floor_block in floor:
                if floor_block.rect.colliderect(bullet.rect):
                    bullet.hit = True

            for wall in walls:
                if wall.rect.colliderect(bullet.rect):
                    bullet.hit = True

            for door in doors:
                if door.rect.colliderect(bullet.rect) and door.state == "closed":
                    bullet.hit = True

            if not round_change:
                for zombie in zombies:
                    if zombie.rect.colliderect(bullet.rect):
                        zombie.life -= self.bullet_damage
                        player.score += 10
                        bullet.hit = True

            if bullet.hit:
                self.shooted_ammo.remove(bullet)
                if not self.reloading:
                    self.next_shooted_bullet_index -= 1



            


class M1911(Gun):
    def __init__(self,x, y):
        self.sprite_m1911 = r"SpriteSheets\Guns\M1911.png"
        super().__init__(self.sprite_m1911, x, y, 30, 22, 10, 15, 1)
        self.charger_setup(15, 80)

class RayGun(Gun):
    def __init__(self, x, y):
        self.sprite_ray_gun = r"SpriteSheets\Guns\ray_gun.png"
        super().__init__(self.sprite_ray_gun, x, y, 40, 26, 200, 10, 2000)
        self.bullet_sprite = r"SpriteSheets\Guns\ray_gun_bullet.png"
        self.bullets_width = 10
        self.bullets_height = 6
        
        self.charger_setup(15, 80)

        

        # Arms alignment
        self.right_dir_x = 33
        self.left_dir_x = -25
        self.center_y = -15

        self.look_up_right_x = 15
        self.look_up_left_x = -18
        self.look_up_y = -60

        self.look_down_right_x = 30
        self.look_down_left_x = -27
        self.look_down_y = -4


class RPK(Gun):
    def __init__(self, x, y):
        self.sprite_ray_gun = r"SpriteSheets\Guns\ray_gun.png"
        super().__init__(self.sprite_ray_gun, x, y, 40, 26, 200, 10, 2)
        self.charger_setup(15, 80)






class Knife(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()







