"""
Class that initializes the main logic of the components and handles events.
"""
from random import randint, choice
from assets import TITLE_FONT, TEXT_FONT, NORMAL_FONT, TITLE_SPRITE, TITLE_SPRITE_RECT, TITLE_SPRITE_EYES, UFO_SPRITE, \
    TITLE_SPRITE_EYES_RECT, UFO_SPRITE_RECT, TITLE_SPRITE_RECT2, UFO_SPRITE_RECT2, TITLE_SPRITE_EYES_RECT2, \
    TITLE_SPRITE2, TITLE_SPRITE_EYES2, UFO_SPRITE2
from components.bandit import Bandit
from components.player import Player
from components.terrain import Terrain
from components.text import Text
from components.ufo import Ufo
from config import SCREEN_WIDTH, COLOR_WHITE, COLOR_RED, SCREEN_HEIGHT, FRAMERATE, PLAYER_COLORS, MENU_COLOR, SCREEN, \
    BACKGROUND_COLOR, ROUND_TIME

import pygame as pg
import sys


class Game:
        def __init__(self):
            self.on_menu = True
            self.clock = pg.time.Clock()
            self.player_1 = None
            self.player_2 = None
            self.player_count = 0
            self.game_tick = 0
            self.game_timer = 0
            self.difficulty_time = 15   # Time in seconds of when difficulty increases
            self.ambush_time = randint(80, 100)   # Time in seconds of when ambush mode activates

            # Creating text as class objects
            self.title_text = Text('< WESTERN RAID >', (SCREEN_WIDTH / 2, 100), TITLE_FONT)
            self.choose_text = Text('WASD / ARROW keys to select character',
                                   (SCREEN_WIDTH / 2, 580), TEXT_FONT, (120, 200, 255), 30)
            self.start_text = Text('PRESS ENTER TO START',
                                   (SCREEN_WIDTH / 2, 300), TEXT_FONT, COLOR_WHITE, 30)

            self.p1_points_text = Text('00000', (90, 30), NORMAL_FONT)
            self.p2_points_text = Text('00000', (SCREEN_WIDTH - 90, 30), NORMAL_FONT)
            self.timer_text = Text('00:00', (SCREEN_WIDTH / 2, 30),
                                   NORMAL_FONT, COLOR_WHITE, 30, (0, 255, 0))
            self.ambush_text = Text('!! AMBUSH INCOMING !!', (SCREEN_WIDTH / 2, 80), TEXT_FONT,
                                    COLOR_RED, 15)

            self.select_error = Text('SELECT A PLAYER', (SCREEN_WIDTH / 2, SCREEN_HEIGHT - 80),
                                    TEXT_FONT, COLOR_RED, 8, (200, 100, 0))

            self.select_error.enabled = False
            self.start_text.blink = True
            self.select_error.color_blink = True

            self.ufo = Ufo()
            self.bandits = []
            self.terrain = []
            self.max_bandits = 0
            self.bandit_count = 0
            self.bandit_spawnrate = 120
            self.menu_loop = [60, False]
            self.start_animate = True

            self.draw_map()

        def draw_map(self):
            self.ufo = Ufo()
            self.terrain = []

            # Grid used to spawn terrain, 1 allows spawning and 0 makes it empty
            # IMPORTANT: The rotation of the grid is different from the rotation
            # of the screen by 90 degrees clockwise
            terrain_grid = [
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1],
                [1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1],
                [1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1],
                [1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1],
                [1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1],
                [1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1],
                [1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1],
                [1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            ]
            terrain_counter = 1

            for row_index, row in enumerate(terrain_grid):
                for col_index, column in enumerate(row):
                    terrain_counter += 1

                    if column != 0 and terrain_counter % randint(1, 12) == 0:
                        random_index = randint(1, 4)

                        if random_index != 3:  # Condition for larger sprites
                            terrain_size = 70
                        else:
                            terrain_size = 140

                        pos_x = row_index * 80
                        pos_y = col_index * 80
                        new_asset = Terrain([pos_x, pos_y], random_index, terrain_size)
                        self.terrain.append(new_asset)

        def run(self):
            while True:
                self.update_game_state()
                self.handle_events()
                self.clock.tick(FRAMERATE)
                self.game_tick += 1

        def handle_events(self):
            keys = pg.key.get_pressed()

            # Detecting player joining the components
            if keys[pg.K_w] or keys[pg.K_a] or keys[pg.K_s] or keys[pg.K_d]:
                if not self.player_1:
                    color = PLAYER_COLORS[self.player_count]
                    self.player_count += 1
                    self.player_1 = Player('WASD', self.player_count, color)
                elif not self.player_2 and self.player_1.controls != 'WASD':
                    color = PLAYER_COLORS[self.player_count]
                    self.player_count += 1
                    self.player_2 = Player('WASD', self.player_count, color)
            if keys[pg.K_UP] or keys[pg.K_LEFT] or keys[pg.K_DOWN] or keys[pg.K_RIGHT]:
                if not self.player_1:
                    color = PLAYER_COLORS[self.player_count]
                    self.player_count += 1
                    self.player_1 = Player('ARROWS', self.player_count, color)
                elif not self.player_2 and self.player_1.controls != 'ARROWS':
                    color = PLAYER_COLORS[self.player_count]
                    self.player_count += 1
                    self.player_2 = Player('ARROWS', self.player_count, color)

            if keys[pg.K_RETURN] and self.on_menu:
                if self.player_1:
                    self.on_menu = False
                else:
                    self.select_error.enabled = True

            for event in pg.event.get():
                # Quit the components
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()

        # just for now, trying to change for the class Bandita
        def bandit_position(self):
            if (self.game_tick % self.bandit_spawnrate == 0
                and self.bandit_count < self.max_bandits):  # add a bandit each 300 ticks
                spawn_direction = choice(['left', 'right'])
                start_pos = [0, 0, # Position that spawns at first
                             0, 0] # Goal position to move to

                if spawn_direction == 'left':
                    start_pos[0] = -50
                    start_pos[1] = randint(10, SCREEN_HEIGHT - 40)
                    start_pos[2] = randint(30, 100)
                    start_pos[3] = start_pos[1]
                if spawn_direction == 'right':
                    start_pos[0] = SCREEN_WIDTH
                    start_pos[1] = randint(10, SCREEN_HEIGHT - 40)
                    start_pos[2] = SCREEN_WIDTH - randint(70, 140)
                    start_pos[3] = start_pos[1]

                bandit = Bandit(start_pos)
                self.bandits.append(bandit)

        # Merged "draw" function with components state to make bullets possible
        def update_game_state(self):
            keys = pg.key.get_pressed()

            if self.on_menu:
                SCREEN.fill(MENU_COLOR)
                self.title_text.draw()
                self.start_text.draw()
                self.choose_text.draw()

                # Draw characters on screen depending on players joined
                if self.player_1:
                    self.select_error.enabled = False
                    SCREEN.blit(TITLE_SPRITE, TITLE_SPRITE_RECT)
                    SCREEN.blit(TITLE_SPRITE_EYES, TITLE_SPRITE_EYES_RECT)
                    SCREEN.blit(UFO_SPRITE, UFO_SPRITE_RECT)
                if self.player_2:
                    # Apply position offset
                    offset1 = 100
                    offset2 = -100
                    TITLE_SPRITE_RECT.centerx = SCREEN_WIDTH / 2 - offset1
                    UFO_SPRITE_RECT.centerx = SCREEN_WIDTH / 2 - offset1
                    TITLE_SPRITE_EYES_RECT.centerx = (SCREEN_WIDTH / 2) - 4 - offset1

                    TITLE_SPRITE_RECT2.centerx = SCREEN_WIDTH / 2 - offset2
                    UFO_SPRITE_RECT2.centerx = SCREEN_WIDTH / 2 - offset2
                    TITLE_SPRITE_EYES_RECT2.centerx = (SCREEN_WIDTH / 2) - 4 - offset2

                    SCREEN.blit(TITLE_SPRITE2, TITLE_SPRITE_RECT2)
                    SCREEN.blit(TITLE_SPRITE_EYES2, TITLE_SPRITE_EYES_RECT2)
                    SCREEN.blit(UFO_SPRITE2, UFO_SPRITE_RECT2)

                if self.game_tick % self.menu_loop[0] == 0:
                    if self.menu_loop[1]:
                        TITLE_SPRITE_RECT.y -= 15
                        TITLE_SPRITE_EYES_RECT.y -= 15
                        UFO_SPRITE_RECT.y -= 15
                        TITLE_SPRITE_RECT2.y += 15
                        TITLE_SPRITE_EYES_RECT2.y += 15
                        UFO_SPRITE_RECT2.y += 15
                        self.menu_loop[1] = False
                    else:
                        TITLE_SPRITE_RECT.y += 15
                        TITLE_SPRITE_EYES_RECT.y += 15
                        UFO_SPRITE_RECT.y += 15
                        TITLE_SPRITE_RECT2.y -= 15
                        TITLE_SPRITE_EYES_RECT2.y -= 15
                        UFO_SPRITE_RECT2.y -= 15
                        self.menu_loop[1] = True
            else:
                SCREEN.fill(BACKGROUND_COLOR)

                for terrain in self.terrain:
                    terrain.draw()

                self.ufo.draw_ufo(SCREEN)

                if self.ufo.fully_broken:
                    self.on_menu = True
                    self.game_timer = 0
                    self.bandits = []
                    self.player_1 = None
                    self.player_2 = None
                    self.player_count = 0
                    self.game_tick = 0
                    return

                self.bandit_position()
                self.max_bandits = 2 + (2 * self.player_count)
                self.bandit_spawnrate = int(120 - (15 * self.player_count))
                self.bandit_count = len(self.bandits)

                if self.game_tick % FRAMERATE == 0:
                    self.game_timer += 1

                for bandit in self.bandits:
                    if bandit.live_bandit:
                        bandit.update(self.ufo.rect.topleft)  # Pass ufo as target
                        bandit.update_bullets()
                        bandit.shield_collide_check(self.player_1)
                        bandit.shield_collide_check(self.player_2)
                        bandit.draw_bandit()
                    else:
                        self.bandits.remove(bandit)

                    # collision of bullets w ufo
                    for bullet in bandit.bullets:
                        bullet.shield_collide_check(self.player_1)  # collision w shield player 1
                        bullet.player_collide_check(self.player_1)
                        bullet.player_collide_check(self.player_2)
                        bullet.shield_collide_check(self.player_2)
                        if self.game_tick % FRAMERATE == 0:
                            bullet.lifetime += 1

                        self.ufo.ufo_collide_check(bullet)

                    if self.game_tick % FRAMERATE == 0:
                        bandit.lifetime += 1

                # Player movement check and drawing
                if self.player_1:
                    self.player_1.move(keys)
                    self.player_1.draw()
                    self.p1_points_text.text = str("{:05d}".format(self.player_1.score))
                    self.p1_points_text.draw()
                if self.player_2:
                    self.player_2.move(keys)
                    self.player_2.draw()
                    self.p2_points_text.text = str("{:05d}".format(self.player_2.score))
                    self.p2_points_text.draw()

                # Drawing UI
                time_left = ROUND_TIME - self.game_timer
                seconds = time_left % 60
                minutes = int(time_left / 60) % 60
                self.timer_text.text = f'{minutes:02}:{seconds:02}'
                self.timer_text.draw()

            if self.select_error.enabled:
                self.select_error.draw()

            pg.display.flip()
