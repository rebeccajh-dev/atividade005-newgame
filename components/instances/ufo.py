"""
Class responsible for drawing the UFO's
"""
from config import SQUARE_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT, UFO_COLORS, COLOR_DAMAGED, SCREEN
from assets import UFO_SPRITE, UFO_SPRITE_RECT, NORMAL_FONT
from components import text
import pygame as pg

class Ufo:
    def __init__(self):
        self.fully_broken = False
        self.width = SQUARE_SIZE
        self.height = SQUARE_SIZE
        self.size = SQUARE_SIZE
        self.ufos = []
        self.center_position()
        self.rect = pg.Rect(SCREEN_WIDTH // 2 - self.size // 2, SCREEN_HEIGHT // 2 - self.size // 2, self.size,
                            self.size)

        self.pointer = text.Create('v v v', (self.rect.centerx, self.rect.centery - 110),
                                   NORMAL_FONT, (255, 255, 80))
        self.pointer_tick = 0
        self.pointer_cd = 20
        self.pointer_down = False

        self.blink = [False, 0, 10, False]
        self.image_mode = False
        self.got_inside = False
        self.can_get_in = False
        self.rect_offset = 0

    def ufo_collide_check(self, game, bullet):
        if not self.ufos:
            return

        brick_amount = len(self.ufos)
        broken_amount = 0

        # check the collides by the lists
        for i in range(brick_amount):
            rect, strength, brick_row, surface = self.ufos[i]

            if self.ufos[i][1] <= 0:
                broken_amount += 1

            # Checks if the bullet_sprites collides w ufo
            if (bullet.rect.colliderect(rect) and bullet.can_hit
                and self.ufos[i][1] >= 1):
                bullet.can_hit = False
                bullet.is_alive = False
                self.take_damage(game, i)
                break

        if broken_amount >= brick_amount:
            self.fully_broken = True

    def explosion_collide_check(self, game, explosion):
        if not self.ufos:
            return

        brick_amount = len(self.ufos)
        broken_amount = 0

        # check the collides by the lists
        for i in range(brick_amount):
            rect, strength, brick_row, surface = self.ufos[i]

            if self.ufos[i][1] <= 0:
                broken_amount += 1

            # Checks if the bullet_sprites collides w ufo
            if (explosion.colliderect(rect)
                and self.ufos[i][1] >= 1):
                self.take_damage(game, i)
                break

        if broken_amount >= brick_amount:
            self.fully_broken = True

    def take_damage(self, game, index):
        if index < len(self.ufos):
            self.ufos[index][1] -= 1
            game.sound.play_sfx('brick_break')

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
                rect = pg.Rect(x + col_index * self.width, y + row_index * self.height,
                               self.width - 3, self.height - 3)
                surface = pg.Surface(rect.size, pg.SRCALPHA)
                self.ufos.append([rect, strength, row_index, surface])

    def victory_ufo(self, player1, player2):
        check_1 = False
        check_2 = False
        if player1:
            player1.victory_tick += 1
            if player1.victory_tick > player1.victory_cooldown:
                check_1 = UFO_SPRITE_RECT.colliderect(player1.rect)
        else: check_1 = True
        if player2:
            player2.victory_tick += 1
            if player2.victory_tick > player2.victory_cooldown:
                check_2 = UFO_SPRITE_RECT.colliderect(player2.rect)
        else: check_2 = True

        UFO_SPRITE_RECT.center = self.rect.center
        UFO_SPRITE_RECT.y -= 40

        if not self.got_inside:
            if check_1 and check_2:
                self.got_inside = True
                return True
            else:
                return False
        else:
            self.rect_offset += 2

            UFO_SPRITE_RECT.y -= self.rect_offset


    def draw_ufo(self, game):
        self.blink[1] += 1

        if not self.blink[3] and not self.got_inside and not self.image_mode:
            for brick in self.ufos:
                rect, strength, brick_row, surface = brick
                # change the color based in the strength
                if strength <= 0:
                    color = COLOR_DAMAGED
                elif strength == 1:
                    color = UFO_COLORS[0][brick_row]
                elif strength == 2:
                    color = UFO_COLORS[1][brick_row]
                elif 3 <= strength < 100:
                    color = UFO_COLORS[2][brick_row]
                else:
                    color = UFO_COLORS[3][brick_row]

                surface.fill(color)
                SCREEN.blit(surface, rect)

        elif self.blink[0]:
            if self.blink[1] >= self.blink[2] and self.blink[3]:
                self.blink[1] = 0
                self.blink[3] = False
            elif self.blink[1] >= self.blink[2] and not self.blink[3]:
                self.blink[1] = 0
                self.blink[3] = True

        self.pointer_tick += 1
        if self.pointer_tick >= self.pointer_cd and self.pointer_down:
            self.pointer.rect = (self.rect.centerx, self.rect.centery - 120)
            self.pointer_tick = 0
            self.pointer_down = False
        elif self.pointer_tick >= self.pointer_cd and not self.pointer_down:
            self.pointer.rect = (self.rect.centerx, self.rect.centery - 110)
            self.pointer_tick = 0
            self.pointer_down = True

        if self.image_mode:
            SCREEN.blit(UFO_SPRITE, UFO_SPRITE_RECT)
            if self.can_get_in: self.pointer.draw()
