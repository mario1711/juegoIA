import pygame
import os

TILE_SIZE = 64


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.sprite_dir = os.path.join('assets', 'sprites')
        self.image = pygame.image.load(os.path.join(self.sprite_dir, "monster.png")).convert_alpha()
        self.sprite = pygame.transform.scale(self.image, (self.image.get_width() * 2, self.image.get_height() * 2))
        self.rect = self.sprite.get_rect(center=(x, y))

    def draw(self, screen):
        self.rect.x = self.rect.x // TILE_SIZE * TILE_SIZE
        self.rect.y = self.rect.y // TILE_SIZE * TILE_SIZE
        screen.blit(self.sprite, self.rect)
