import pygame
from funciones import get_block

class Object(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, name=None):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.width = width
        self.height = height
        self.name = name
    
    def draw(self, screen, offset_x, offset_y):
        screen.blit(self.image, (self.rect.x - offset_x, self.rect.y - offset_y))



class Block(Object):
    def __init__(self, x, y, size):
        super().__init__(x, y, size, size)
    
        block = get_block(size, 64, 128)
        self.image.blit(block, (0, 0))
        self.mask = pygame.mask.from_surface(self.image)


class Wall_Stone(Object):
    def __init__(self, x, y, size):
        super().__init__(x, y, size, size)
    
        block = get_block(size, 64, 160)
        self.image.blit(block, (0, 0))
        self.mask = pygame.mask.from_surface(self.image)
