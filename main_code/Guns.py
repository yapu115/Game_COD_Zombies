import pygame
from funciones import insert_image, insert_rect


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, sprite=r"SpriteSheets\Guns\bullet.png"):
        super().__init__()
        self.sprite = sprite
        self.image = insert_image(sprite, 15, 10)
        self.rect = insert_rect(self.image, x, y)
        self.on_air = False
        self.direction = "left"

    def fire(self, screen, offset_x, offset_y):
        if self.on_air:
            screen.blit(self.image, (self.rect.x - offset_x, self.rect.y - offset_y))
            if self.direction == "left":
                self.rect.x -= 5
            else:
                self.rect.x += 5
    
    def update(self, x, y):
        self.image = insert_image(self.sprite, 15, 10)
        self.rect.x = x
        self.rect.y = y
        
        if self.direction == "right":
            self.image = pygame.transform.flip(self.image, True, False)



class Gun(pygame.sprite.Sprite):

    def __init__(self, sprite, x, y, width, height, bullet_dmg, velocity_fire):
        super().__init__()
        self.sprite = sprite
        self.image = insert_image(self.sprite, width, height)
        self.rect = insert_rect(self.image, x, y)
        
        self.direction = "left"
        self.width = width
        self.height = height

        self.charger = []
        self.ammo = []

        self.bullet_damage = bullet_dmg
        self.velocity_fire = velocity_fire

        self.fire = False

        self.contador = 0

    def draw(self, screen, offset_x, offset_y):
        for bullet in self.ammo:
            bullet.fire(screen, offset_x, offset_y)
        screen.blit(self.image, (self.rect.x - offset_x, self.rect.y - offset_y))
            

    def update(self, x, y):
        self.image = insert_image(self.sprite, self.width, self.height)

        self.rect.x = x
        self.rect.y = y
        if self.direction == "left":
            self.image = pygame.transform.flip(self.image, True, False)

        for bullet in self.ammo:
            if not bullet.on_air:
                bullet.direction = self.direction
                bullet.update(x, y)

    def charger_setup(self, charger_ammo, total_chargers):
        self.ammo = [Bullet(self.rect.x, self.rect.y) for i in range(charger_ammo)]

    def shoot(self):
        try:
            if self.fire:
                self.contador += 1
                self.ammo[self.contador].on_air = True
                self.fire = False
        except IndexError:
            print("holaa")
            


class M1911(Gun):
    def __init__(self,x, y):
        self.sprite_m1911 = r"SpriteSheets\Guns\M1911.png"
        super().__init__(self.sprite_m1911, x, y, 30, 22, 5, 1)
        self.charger_setup(7, 80)


