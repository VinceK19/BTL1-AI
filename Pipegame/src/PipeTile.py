import pygame
from pygame.sprite import Sprite
from src.constant import *
from src.Spritesheet import Spritesheet


class PipeTile(Sprite):
    def __init__(self, tile_x, tile_y, piece, spritesheet: Spritesheet):
        Sprite.__init__(self)
        self.spritesheet = spritesheet
        self.image = pygame.Surface((64, 64))
        self.image.fill((0, 0, 0))
        self.tile_x, self.tile_y = tile_x, tile_y
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = tile_x * TILE_SIZE, tile_y * TILE_SIZE

    def update(self, pieces, states):
        if len(self.groups()) == 0:
            self.kill()
            return
        x, y = self.tile_x, self.tile_y
        state = "pipe" if states[x][y] & 1 == 0 else "light"
        self.image = self.spritesheet.parse_sprite(f"{state}_{pieces[x][y] + 1}.png")

    def draw(self, surface: pygame.Surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))
