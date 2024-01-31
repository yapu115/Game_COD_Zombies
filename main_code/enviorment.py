import pygame
from funciones import insert_image, insert_rect
from abc import ABC, abstractmethod

class Resource(pygame.sprite.Sprite):
    def __init__(self, width, height, x, y, image):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.image = insert_image(image, width, height)
        self.rect = insert_rect(self.image, x, y)
    
    def draw(self, screen, offset_x, offset_y):
        screen.blit(self.image, (self.rect.x - offset_x, self.rect.y - offset_y))

class Door(Resource):
    def __init__(self, x, y):
        super().__init__(x, y, 24, 192, r"SpriteSheets\doors\closed.png")
        self.x = x
        self.y = y
        self.width = 24
        self.height = 192

        self.state = "closed"
        self.closed = r"SpriteSheets\doors\closed.png"
        self.opened = r"SpriteSheets\doors\opened.png"
        self.image = insert_image(self.closed, 24, 192)
        self.rect = insert_rect(self.image, x, y)
    
    def update(self): 
        if self.state == "opened":
            self.image = insert_image(self.opened, 96, 150)
            self.rect = insert_rect(self.image, self.x + 34, self.y)
        elif self.state == "closed":
            self.image = insert_image(self.closed, 24, 150)
            self.rect = insert_rect(self.image, self.x - 7, self.y)

    def draw(self, screen, offset_x, offset_y):
        self.update()
        screen.blit(self.image, (self.rect.x - offset_x, self.rect.y - offset_y))

# Combinar ambas puertas en una sola
        
        
class BunkerDoor(Resource):
    def __init__(self, x, y):
        super().__init__(154, 128, x, y, r"SpriteSheets\doors\closed_bunker_door.png")
        self.x = x
        self.y = y
        self.width = 77 * 2.5
        self.height = 64 * 2.5

        self.state = "closed"
        self.closed = r"SpriteSheets\doors\closed_bunker_door.png"
        self.opened = r"SpriteSheets\doors\opened_bunker_door.png"
        self.image = insert_image(self.closed, self.width, self.height)
        self.rect = insert_rect(self.image, x, y)
    
    def update(self): 
        if self.state == "opened":
            self.image = insert_image(self.opened, self.width, self.height)
        elif self.state == "closed":
            self.image = insert_image(self.closed, self.width, self.height)

    def draw(self, screen, offset_x, offset_y):
        self.update()
        screen.blit(self.image, (self.rect.x - offset_x, self.rect.y - offset_y))


class PerkMachine(Resource, ABC):
    def __init__(self, width, height, x, y, perk_image, logo_image):
        super().__init__(width, height, x, y, perk_image)
        self.logo_image = logo_image
        self.logo_width = 33
        self.logo_height = 36

        self.just_bought = True


    @abstractmethod
    def activate(self, screen, player):
        """Activates the perk function on the player"""
        


class Juggernog(PerkMachine):
    def __init__(self, x, y):
        super().__init__(42, 150, x, y, r"SpriteSheets\Perks_machines\Juggernog.png", r"SpriteSheets\Perks_machines\juggernog_logo.png")

    def activate(self, screen, player):

        logo = Resource(self.logo_width, self.logo_width, 400, 620, self.logo_image)
        screen.blit(logo.image, logo.rect)

        player.top_life = 500

        if self.just_bought:
            player.life = 500
            self.just_bought = False
         

class SpeedCola(PerkMachine):
    def __init__(self, x, y):
        super().__init__(37, 78, x, y, r"SpriteSheets\Perks_machines\speed_cola.png", r"SpriteSheets\Perks_machines\speed_cola_logo.png")


    def activate(self, screen, player):
        logo = Resource(33, 36, 400, 620, self.logo_image)
        screen.blit(logo.image, logo.rect)

        if self.just_bought:
            player.gun.loading_speed *= 2
            self.just_bought = False


class DoubleTap(PerkMachine):
    def __init__(self, x, y):
        super().__init__(40, 62, x, y, r"SpriteSheets\Perks_machines\double_tap.png", r"SpriteSheets\Perks_machines\double_tap_logo.png")

    def activate(self, screen, player):

        logo = Resource(self.logo_width, self.logo_height, 400, 620, self.logo_image)
        screen.blit(logo.image, logo.rect)
        
        if self.just_bought:
            player.gun.bullet_damage *= 2
            self.just_bought = False

class QuickRevive(PerkMachine):
    def __init__(self, x, y):
        super().__init__(42, 150, x, y, r"SpriteSheets\Perks_machines\quick_revive.png", r"SpriteSheets\Perks_machines\quick_revive_logo.png")

    def activate(self, screen, player):

        logo = Resource(self.logo_width, self.logo_height, 400, 620, self.logo_image)
        screen.blit(logo.image, logo.rect)
        
        if self.just_bought:
            player.life = 500
            self.just_bought = False
