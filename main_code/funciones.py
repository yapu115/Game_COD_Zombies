import pygame
from os import listdir
from os.path import isfile, join
import os
import random
import math

def insert_image(direction , width, height):
    image = pygame.image.load(direction)
    image = pygame.transform.scale(image, (width, height))
    return image

def insert_rect(image, x, y):
    rect = image.get_rect()
    rect.centerx = x
    rect.centery = y
    return rect

def flip(sprites):
    return [pygame.transform.flip(sprite, True, False) for sprite in sprites]


def load_sprite_sheets(dir1, dir2, width, height, direction=False):
    path = join("SpriteSheets", dir1, dir2)
    images = [f for f in listdir(path) if isfile(join(path, f))] # Obtiene una lista de todos los archivos segun el path que se paso
    
    all_sprites = {}
    for image in images:
        sprite_sheet = pygame.image.load(join(path, image)) # De todas las imagenes tomo una sola sprite
        #sprite_sheet.set_colorkey((0, 0, 0))
        sprites = []

        print(path, image,  sprite_sheet)
        for i in range(sprite_sheet.get_width() // width): # Tomo cada frame de la sprite sheet dividiendo el largo total con el largo pasado
            surface = pygame.Surface((width, height), pygame.SRCALPHA, 32) # Creo una superficie para ese frame
            rect = pygame.Rect(i * width, 0, width, height) # creo un rectangulo
            surface.blit(sprite_sheet, (0, 0), rect) # Lo dibujo
            #sprites.append(surface)
            sprites.append(pygame.transform.scale2x(surface)) # Lo hago mas grande mientras lo agrego a la lista

        if direction: # En caso de que tenga distintos lados
            all_sprites[image.replace(".png", "") + "_right"] = sprites # Cuando esté a la derecha el sprite queda igual
            all_sprites[image.replace(".png", "") + "_left"] = flip(sprites) # Cuando esté a la izquierda hacer el flip
        else:
            all_sprites[image.replace(".png", "") + ""] = sprites # En caso de no tener dos lados lo dejo igual

    return all_sprites


def get_block(size, pos_x, pos_y):
    path = join("SpriteSheets", "Terrain", "Terrain.png") # start from here
    image = pygame.image.load(path).convert_alpha()
    surface = pygame.Surface((size, size), pygame.SRCALPHA, 32)
    rect = pygame.Rect(pos_x, pos_y, size, size)
    surface.blit(image, (0, 0), rect)
    return surface
    #return pygame.transform.scale2x(surface)
