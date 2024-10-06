import pygame as pg

from config import TERRAIN_COLORS, SCREEN


class Terrain:
    def __init__(self, spawn_pos, index, size):
        self.name = 'TERRAIN'
        self.sprite = pg.image.load(f'assets/terrain_sprites/{index}.png').convert_alpha()
        self.sprite = pg.transform.scale(self.sprite, (size, size))
        self.sprite.fill(TERRAIN_COLORS[index], special_flags=pg.BLEND_RGBA_MULT)

        self.rect = self.sprite.get_rect() # Bandit size
        self.rect.x = spawn_pos[0]
        self.rect.y = spawn_pos[1]

    def draw(self):
        SCREEN.blit(self.sprite, self.rect)
