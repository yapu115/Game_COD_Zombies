import pygame
from funciones import insert_image, insert_rect

class Door(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.x = x
        self.y = y
        self.width = width
        self.height = height

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