import pygame
import os

TILE_SIZE = 64


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.sprite_dir = os.path.join('assets', 'sprites')
        self.obstacle_tile = pygame.image.load(self.sprite_dir + "/obstacle.png").convert_alpha()
        self.sprite = pygame.transform.scale(self.obstacle_tile, (self.obstacle_tile.get_width() * 2, self.obstacle_tile.get_height() * 2))
        self.rect = self.obstacle_tile.get_rect(center=(x, y))
        self.rect.x = x - self.rect.width // 2
        self.rect.y = y - self.rect.height // 2

    def draw(self, screen):
        self.rect.x = round(self.rect.x / TILE_SIZE) * TILE_SIZE
        self.rect.y = round(self.rect.y / TILE_SIZE) * TILE_SIZE
        screen.blit(self.sprite, self.rect)
