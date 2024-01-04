import pygame
from funciones import insert_image, insert_rect

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