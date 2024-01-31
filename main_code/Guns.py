import pygame
from funciones import insert_image, insert_rect


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, sprite=r"SpriteSheets\Guns\bullet.png"):
        super().__init__()
        # Base
        self.sprite = sprite
        self.image = insert_image(sprite, 10, 5)
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
                    self.rect.y += fire_velocity 
                else:
                    self.rect.x -= fire_velocity
            else:
                if self.looking_up:
                    self.rect.x += fire_velocity 
                    self.rect.y -= fire_velocity 
                elif self.looking_down:
                    self.rect.x += fire_velocity 
                    self.rect.y += fire_velocity 
                else:
                    self.rect.x += fire_velocity

    def update(self, x, y):
        self.image = insert_image(self.sprite, 15, 10)
        
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
        self.next_bullet = -1

        # Bullets
        self.charger_ammo = []
        self.spare_ammo = []

        self.total_charger_ammo = 0
        self.bullet_damage = bullet_dmg
        self.fire_velocity = fire_velocity
        self.reloading_speed = reloading_speed

        # Flags
        self.fire = False


        self.looking_up = False
        self.looking_down = False

    def draw(self, screen, offset_x, offset_y):
        for bullet in self.charger_ammo:
            bullet.fire(screen, offset_x, offset_y, self.fire_velocity)
        screen.blit(self.image, (self.rect.x - offset_x, self.rect.y - offset_y))
            

    def update(self, x, y):
        self.image = insert_image(self.sprite, self.width, self.height)
        self.rect.x = x
        self.rect.y = y

        if self.direction == "left":
            self.image = pygame.transform.flip(self.image, True, False)

        for bullet in self.charger_ammo:
            if not bullet.on_air:
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
        self.charger_ammo = [Bullet(self.rect.x, self.rect.y) for i in range(charger_ammo)]
        self.spare_ammo = [Bullet(self.rect.x, self.rect.y) for i in range(spare_ammo)]
        self.total_charger_ammo = charger_ammo
        self.next_bullet = charger_ammo - 1

    def shoot(self):
        try:
            if self.fire:
                self.next_bullet -= 1
                self.charger_ammo[self.next_bullet].on_air = True
                self.fire = False
        except IndexError:
            self.reload()

    def reload(self):
        if self.spare_ammo:
            if len(self.charger_ammo) < self.total_charger_ammo: 
                bullet = self.spare_ammo.pop()
                self.charger_ammo.append(bullet)
                self.next_bullet = self.total_charger_ammo - 1

            


class M1911(Gun):
    def __init__(self,x, y):
        self.sprite_m1911 = r"SpriteSheets\Guns\M1911.png"
        super().__init__(self.sprite_m1911, x, y, 30, 22, 10, 15, 1)
        self.charger_setup(15, 80)


