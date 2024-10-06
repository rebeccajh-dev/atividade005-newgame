"""
Class responsible for drawing the UFO's
"""
from config import SQUARE_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT, BACKGROUND_COLOR, UFO_COLORS, COLOR_DAMAGED
import pygame as pg

class Ufo:
    def __init__(self):
        self.live_ball = True
        self.fully_broken = False
        self.width = SQUARE_SIZE
        self.height = SQUARE_SIZE
        self.size = SQUARE_SIZE
        self.ufos = []
        self.center_position()
        self.rect = pg.Rect(SCREEN_WIDTH // 2 - self.size // 2, SCREEN_HEIGHT // 2 - self.size // 2, self.size,
                            self.size)

    def ufo_collide_check(self, bullet):
        if not self.ufos:
            return

        brick_amount = len(self.ufos)
        broken_amount = 0

        # check the collides by the lists
        for i in range(brick_amount):
            rect, strength, brick_row = self.ufos[i]

            if self.ufos[i][1] <= 0:
                broken_amount += 1

            # Checks if the bullets collides w ufo
            if (bullet.rect.colliderect(rect) and bullet.can_hit
                and self.ufos[i][1] >= 1):
                bullet.can_hit = False
                bullet.is_alive = False
                self.take_damage(i)
                break

        if broken_amount >= brick_amount:
            self.fully_broken = True

    def take_damage(self, index):
        if index < len(self.ufos):
            self.ufos[index][1] -= 1
            if self.ufos[index][1] < 0:
                self.ufos[index][1] = 0  # Manter a força em zero

    def center_position(self):
        # Define the UFO grid as a list of lists
        ufo_grid = [
            [1, 1, 1],
            [1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1]
        ]

        # Calculate the total height of the UFOs
        total_height = sum(len(row) * self.height for row in ufo_grid)

        # Calculate the starting y position to center the rows
        y = (SCREEN_HEIGHT - 400)

        for row_index, strengths in enumerate(ufo_grid):
            strength = strengths[0]  # Assuming uniform strength for each column in this row
            row_width = len(strengths) * self.width

            # Calculate the starting x position for the current row
            x = (SCREEN_WIDTH - row_width) // 2

            # Add UFOs for the current row
            for col_index, strength in enumerate(strengths):
                rect = pg.Rect(x + col_index * self.width, y + row_index * self.height, self.width, self.height)
                self.ufos.append([rect, strength, row_index])

    def draw_ufo(self, surface):
        if self.live_ball:
            for brick in self.ufos:
                rect, strength, brick_row = brick
                # change the color based in the strength
                color = UFO_COLORS[brick_row] if strength > 0 else COLOR_DAMAGED
                pg.draw.rect(surface, color, rect)
                pg.draw.rect(surface, BACKGROUND_COLOR, rect, 2)
