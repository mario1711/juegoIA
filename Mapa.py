import os
import random
import pygame

TILE_SIZE = 64


class Mapa(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.sprite_dir = os.path.join('assets', 'sprites')
        self.border = pygame.image.load(os.path.join(self.sprite_dir + "/border.png")).convert_alpha()
        self.ground = pygame.image.load(os.path.join(self.sprite_dir + "/ground.png")).convert_alpha()
        self.ground1 = pygame.image.load(os.path.join(self.sprite_dir + "/ground2.png")).convert_alpha()

        self.tile_mappings = {
            0: self.border,
            1: self.ground,
            2: self.ground1
        }

        self.obstacles = pygame.sprite.Group()
        self.mapa = [
            [0] * 13,
            [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
            [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
            [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
            [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
            [0, 1, 1, 1, 1, 2, 2, 2, 1, 1, 1, 1, 0],
            [0, 1, 1, 1, 1, 2, 2, 2, 1, 1, 1, 1, 0],
            [0, 1, 1, 1, 1, 2, 2, 2, 1, 1, 1, 1, 0],
            [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
            [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
            [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
            [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
            [0] * 13]

    def draw(self, screen):
        for row_index, row in enumerate(self.mapa):
            for col_index, tile_type in enumerate(row):
                tile = self.tile_mappings.get(tile_type)
                if tile:
                    image = pygame.transform.scale(tile, (tile.get_width() * 2, tile.get_height() * 2))
                    screen.blit(image, (col_index * TILE_SIZE, row_index * TILE_SIZE))
