import pygame as pg
from random import randint, choice

from config import SCREEN

class Decoration:
    def __init__(self, name, size, position, color):
        self.name = name
        self.size = size
        self.sprite = pg.image.load(f'assets/decoration_sprites/{self.name}.png').convert_alpha()
        self.sprite = pg.transform.scale(self.sprite, (self.size, self.size))
        self.sprite.fill(color, special_flags=pg.BLEND_RGBA_MULT)

        self.rect = self.sprite.get_rect()
        self.rect.x = position[0]
        self.rect.y = position[1]

class Terrain:
    def __init__(self, spawn_pos, config, index, level):
        if randint(1, 777) == 1: config = ['luck_statue', 70, (140, 120, 20)]
        self.index = index
        self.name = config[0]
        self.size = config[1]

        self.sprite = pg.image.load(f'assets/terrain_sprites/{self.name}.png').convert_alpha()
        self.sprite = pg.transform.scale(self.sprite, (self.size, self.size))
        self.sprite.fill(config[2], special_flags=pg.BLEND_RGBA_MULT)

        self.rect = self.sprite.get_rect()
        self.rect.x = spawn_pos[0]
        self.rect.y = spawn_pos[1]

        self.area_rect = pg.Rect(self.rect.x, self.rect.y,
                                 self.size / level.terrain_area_reduction,
                                 self.size / level.terrain_area_reduction)
        self.area_rect.center = self.rect.center
        self.decorations = []

        if self.name == 'table':
            deco_amount = randint(0, 2)

            for deco in range(deco_amount):
                random_deco = choice([
                    ['small_bottle', (110, 110, 100)],
                    ['hat', (150, 150, 150)],
                    ['food', (120, 70, 20)],
                    ['chess', (120, 120, 120)],
                    ['dabloons', (150, 140, 80)]
                ])
                deco = Decoration(random_deco[0], self.size, self.rect, random_deco[1])
                self.decorations.append(deco)

            seats_amount = randint(0, 2)

            for seat in range(seats_amount):
                random_seat = ['chair', (100, 60, 65)]
                if randint(1, 10) == 1: random_seat = ['funny_chair', (100, 60, 65)]

                if seat == 1:
                    seat_pos = [self.rect.x - self.size + 10, self.rect.y]
                else:
                    seat_pos = [self.rect.x + self.size - 10, self.rect.y]

                seat = Decoration(random_seat[0], self.size, seat_pos, random_seat[1])
                self.decorations.append(seat)
        if self.name == 'large_table':
            deco_amount = randint(1, 3)
            already_has = False

            for deco in range(deco_amount):
                random_deco = choice([
                    ['wasted_bandit', (150, 150, 150)],
                    ['small_bottle', (110, 110, 100)],
                    ['hat', (150, 150, 150)],
                    ['food', (120, 70, 20)],
                    ['chess', (120, 120, 120)],
                    ['dabloons', (150, 140, 80)]
                ])

                for existing in self.decorations:
                    if random_deco[0] == 'wasted_bandit' and existing.name == 'wasted_bandit':
                        already_has = True
                if already_has: continue

                if random_deco[0] == 'wasted_bandit':
                    new_size = int(self.size / 1.5)
                    pos_offset = int(new_size / 2.55)
                    deco = Decoration(random_deco[0], new_size,
                    [self.rect.x + randint(0, pos_offset), self.rect.y + pos_offset], random_deco[1])
                else:
                    new_size = int(self.size / 2)
                    deco = Decoration(random_deco[0], new_size,
                    [self.rect.x + randint(0, new_size), self.rect.y + new_size], random_deco[1])
                self.decorations.append(deco)

    def distance_check(self, level):
        # Check if there are any terrain too close to the hitbox, and remove it
        for terrain in level.map:
            if self.area_rect.colliderect(terrain.area_rect) and terrain.index != self.index:
                level.map.remove(terrain)

    def draw(self):
        # Choice to see the area hitbox
        # pg.draw.rect(SCREEN, (255, 128, 0), self.area_rect)
        SCREEN.blit(self.sprite, self.rect)

        for decoration in self.decorations:
            SCREEN.blit(decoration.sprite, decoration.rect)
