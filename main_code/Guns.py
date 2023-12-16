import pygame
from funciones import insert_image, insert_rect


class Bullet(pygame.sprite.Sprite):
    def __init__(self, sprite=r"SpriteSheets\Guns\bullet.png"):
        super().__init__()
        self.image = insert_image(sprite, 100, 100)
        self.rect = insert_rect(self.image, 10, 10)


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

    def draw(self, screen, offset_x, offset_y):
        screen.blit(self.image, (self.rect.x - offset_x, self.rect.y - offset_y))

    def update(self, x, y):
        self.image = insert_image(self.sprite, self.width, self.height)

        self.rect.x = x
        self.rect.y = y
        if self.direction == "left":
            self.image = pygame.transform.flip(self.image, True, False)

    def charger_setup(self, charger_ammo, total_chargers):
        for i in range(total_chargers):
            self.ammo.append(Bullet())

    def shoot(self, screen, offset_x, offset_y):
        screen.blit(self.ammo[0].image, (self.ammo[0].rect.x - offset_x, self.ammo[0].rect.y - offset_y))
        if self.fire:
            if self.direction == "left":
                self.ammo[0].rect.x -= 0.5


class M1911(Gun):
    def __init__(self,x, y):
        self.sprite_m1911 = r"SpriteSheets\Guns\M1911.png"
        super().__init__(self.sprite_m1911, x, y, 30, 22, 5, 1)
        self.charger_setup(7, 80)


