"""
Class that initializes the main logic of the components and handles events.
"""
import random
from random import randint, choice
from assets import TITLE_FONT, TEXT_FONT, NORMAL_FONT, TITLE_SPRITE, TITLE_SPRITE_RECT, TITLE_SPRITE_EYES, UFO_SPRITE, \
    TITLE_SPRITE_EYES_RECT, UFO_SPRITE_RECT, TITLE_SPRITE_RECT2, UFO_SPRITE_RECT2, TITLE_SPRITE_EYES_RECT2, \
    TITLE_SPRITE2, TITLE_SPRITE_EYES2, UFO_SPRITE2, SMALL_FONT, WIN_SPRITE_EYES, WIN_SPRITE_EYES2, WIN_SPRITE_EYES_RECT, \
    WIN_SPRITE_EYES_RECT2, DEFEAT_CAGE, DEFEAT_CAGE_RECT
from components.bandit import Bandit
from components.player import Player
from components.terrain import Terrain
from components.text import Text
from components.ufo import Ufo
from components.objects import Objects
from components.music import Music
from config import SCREEN_WIDTH, COLOR_WHITE, COLOR_RED, SCREEN_HEIGHT, FRAMERATE, PLAYER_COLORS, MENU_COLOR, SCREEN, \
    BACKGROUND_COLOR, AMBUSH_FILTER, VICTORY_COLOR, DEFEAT_COLOR, P2_TITLE_OFFSET

import pygame as pg
import sys


class Game:
        def __init__(self):
            self.game_state = 'menu'
            self.ambush_mode = False
            self.can_spawn_bandits = False
            self.clock = pg.time.Clock()
            self.player_1 = None
            self.player_2 = None
            self.player_count = 0
            self.game_tick = 0
            self.game_timer = 0
            self.full_score = 0
            self.round_time = 240
            self.music = Music()

            self.difficulty_time = 15   # Time in seconds of when difficulty increases

            # Time in seconds of when ambush mode activates
            self.ambush_time = randint(140, 160)

            # Creating text as class objects
            # Menu messages
            self.survived_text = Text('-=[ YOU SURVIVED ]=-', (SCREEN_WIDTH / 2, 100), TITLE_FONT,
                                      COLOR_WHITE, 30, (120, 255, 160))
            self.lost_text = Text('~X CAPTURED X~', (SCREEN_WIDTH / 2, 100), TITLE_FONT,
                                      (255, 160, 50))
            self.final_message = Text('CONGRATULATIONS AND', (190, SCREEN_HEIGHT - 150),
                                      TEXT_FONT, (255, 255, 255))
            self.final_message2 = Text('THANKS FOR PLAYING! :]', (185, SCREEN_HEIGHT - 115),
                                      TEXT_FONT, (255, 255, 255))

            self.title_text = Text('< WESTERN RAID >', (SCREEN_WIDTH / 2, 100), TITLE_FONT)
            self.player1_text = Text('PLAYER 1', (SCREEN_WIDTH / 2 - 100, 350), TEXT_FONT, COLOR_WHITE)
            self.player2_text = Text('PLAYER 2', (SCREEN_WIDTH / 2 + 100, 350), TEXT_FONT, COLOR_WHITE)
            self.select_text = Text('SELECT THE PLAYER(S)',
                                   (SCREEN_WIDTH / 2, 270), TEXT_FONT, COLOR_WHITE, 30)
            self.choose_text = Text('use WASD or ARROW keys to select your player',
                                   (SCREEN_WIDTH / 2, 300), TEXT_FONT, (120, 200, 255), 30)
            self.move_tip = Text(' WASD/ARROW keys to move !',
                                    (SCREEN_WIDTH / 2, 430), TEXT_FONT, (255, 255, 255), 10)
            self.volume_text = Text('0 = Mute & -/+ keys to change volume',
                                    (SCREEN_WIDTH / 2, 600), SMALL_FONT, (200, 200, 200), 30)
            self.start_text = Text('PRESS ENTER TO START',
                                   (SCREEN_WIDTH / 2, 270), TEXT_FONT, COLOR_WHITE, 30)
            self.return_text = Text('PRESS ENTER TO GO BACK TO MENU',
                               (SCREEN_WIDTH / 2, SCREEN_HEIGHT - 40), TEXT_FONT, COLOR_WHITE, 30)

            self.full_score_text = Text('SCORE: 0000000', (SCREEN_WIDTH / 2, 180), NORMAL_FONT)
            self.new_best_text = Text('NEW BEST!', (SCREEN_WIDTH / 2, 220),
                                    TEXT_FONT, (250, 230, 100), 10, (150, 255, 100))

            # Round stats messages
            self.p1_points_text = Text('00000', (90, 30), NORMAL_FONT)
            self.p2_points_text = Text('00000', (SCREEN_WIDTH - 90, 30), NORMAL_FONT)
            self.timer_text = Text('00:00', (SCREEN_WIDTH / 2, 30),
                                   NORMAL_FONT, COLOR_WHITE, 30, (0, 255, 0))

            # In-round messages
            self.begin_message = Text("Bandits approaching, protect your ship until timer runs out!",
                                    (SCREEN_WIDTH / 2, 170), TEXT_FONT, (255, 255, 0), 10)
            self.ambush_text = Text('!! AMBUSH INCOMING !!', (SCREEN_WIDTH / 2, 80), TEXT_FONT,
                                    COLOR_RED, 15)
            self.get_in = Text('- THE SPACESHIP HAS BEEN FIXED! GET IN!! -', (SCREEN_WIDTH / 2, 80),
                                    TEXT_FONT, COLOR_WHITE, 15, 8)

            # Error messages
            self.select_error = Text('SELECT A PLAYER', (SCREEN_WIDTH / 2, SCREEN_HEIGHT - 100),
                                    TEXT_FONT, COLOR_RED, 8, (200, 100, 0))

            self.new_best_text.enabled = False
            self.select_error.enabled = False
            self.survived_text.color_blink = True
            self.new_best_text.color_blink = True
            self.select_error.color_blink = True
            self.ambush_text.blink = True
            self.start_text.blink = True
            self.select_text.blink = True
            self.return_text.blink = True
            self.get_in.blink = True

            self.ufo = Ufo()
            self.objects = []
            self.bullets = []
            self.bandits = []
            self.terrain = []
            self.base_max_bandits = 3
            self.max_bandits = 0
            self.bandit_count = 0
            self.base_bandit_spawnrate = 240
            self.menu_loop = [35, False]
            self.start_animate = True
            # These lists are used for "animations" or effects
            self.base_ambush_start = [False, 0, 5, 0, 60, False, 0, 300, False]
            self.base_begin_start = [True, 0, 600]
            self.begin_start = self.base_begin_start[:]
            self.ambush_start = self.base_ambush_start[:]
            self.start_defeat = False
            self.base_defeat_values = [
                False, # Transition enabled
                0, 120, # UFO blinking animation timer
                0, 60, # Screen transition timer
                False, # Screen clearing condition
                False  # Final check for defeat
            ]

            self.base_victory_values = [
                False,  # Transition enabled
                False,  # Condition for getting the players inside
                False,  # Condition for song to play
                0, 400,  # Ufo flying back to space animation timer
                0, 60,  # Screen transition timer
                False,  # Screen clearing condition
                False  # Final check for victory
            ]
            self.victory_transition = self.base_victory_values[:]
            self.defeat_transition = self.base_defeat_values[:]

            self.draw_map()
            self.music.play('menu', -1)

        def draw_map(self):
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
            terrain_type = randint(1, 2)
            ter1_sprites = [1, 2, 3, 4, 5]
            ter2_sprites = [3, 4, 5, 6, 7, 8, 9, 10]

            for row_index, row in enumerate(terrain_grid):
                for col_index, column in enumerate(row):
                    terrain_counter += 1

                    if column != 0 and terrain_counter % randint(1, 12) == 0:
                        large_sprites = [3, 7, 8]   # Index for large sprites in the terrain sprites folder
                        random_index = 1

                        if terrain_type == 1:
                            random_index = random.choice(ter1_sprites)
                        elif terrain_type == 2:
                            random_index = random.choice(ter2_sprites)

                        if randint(1, 777) == 1: random_index = 99  # Rare snake sprite for flavor

                        if not large_sprites.count(random_index) != 0:  # Condition for larger sprites
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
            if self.game_state == 'menu' or self.game_state == 'round':
                if keys[pg.K_w] or keys[pg.K_a] or keys[pg.K_s] or keys[pg.K_d]:
                    if not self.player_1:
                        color = PLAYER_COLORS[self.player_count]
                        self.player_count += 1
                        self.player_1 = Player('WASD', self.player_count, color)
                        self.player_1.rect.center = ((SCREEN_WIDTH / 2) - 120, SCREEN_HEIGHT / 2)
                    elif not self.player_2 and self.player_1.controls != 'WASD':
                        color = PLAYER_COLORS[self.player_count]
                        self.player_count += 1
                        self.player_2 = Player('WASD', self.player_count, color)
                        self.player_2.rect.center = ((SCREEN_WIDTH / 2) + 120, SCREEN_HEIGHT / 2)
                if keys[pg.K_UP] or keys[pg.K_LEFT] or keys[pg.K_DOWN] or keys[pg.K_RIGHT]:
                    if not self.player_1:
                        color = PLAYER_COLORS[self.player_count]
                        self.player_count += 1
                        self.player_1 = Player('ARROWS', self.player_count, color)
                        self.player_1.rect.center = ((SCREEN_WIDTH / 2) - 120, SCREEN_HEIGHT / 2)
                    elif not self.player_2 and self.player_1.controls != 'ARROWS':
                        color = PLAYER_COLORS[self.player_count]
                        self.player_count += 1
                        self.player_2 = Player('ARROWS', self.player_count, color)
                        self.player_2.rect.center = ((SCREEN_WIDTH / 2) + 120, SCREEN_HEIGHT / 2)

            if keys[pg.K_RETURN]:
                if self.game_state == 'menu':
                    if self.player_1:
                        self.music.play('sandwreck', -1)
                        self.game_state = 'round'
                    else:
                        self.select_error.enabled = True
                if self.game_state == 'victory' or self.game_state == 'defeat':
                    self.game_reset()

            if keys[pg.K_BACKSPACE]:
                if self.game_state == 'menu':
                    self.player_count = 0
                    self.player_1 = None
                    self.player_2 = None

            if keys[pg.K_0]:
                self.music.mute_music()

            if keys[pg.K_EQUALS] or keys[pg.K_PLUS]:
                self.music.change_volume('increase')
                print(self.music.volume_offset)
            if keys[pg.K_MINUS]:
                self.music.change_volume('decrease')
                print(self.music.volume_offset)

            for event in pg.event.get():
                # Quit the components
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()

                if event.type == pg.KEYUP:
                    if event.key == pg.K_0:
                        self.music.button_pressed = False
                    if event.key == pg.K_PLUS or event.key == pg.K_EQUALS or event.key == pg.K_MINUS:
                        self.music.button_pressed = False

        # Spawning bandits randomly
        def bandit_position(self, number_spawned):
            bandit_spawnrate = int(self.base_bandit_spawnrate - (15 * self.player_count))

            if (self.game_tick % bandit_spawnrate == 0
                and self.bandit_count < self.max_bandits):  # add bandits each 300 ticks
                for new_bandit in range(number_spawned):
                    spawn_direction = choice(['left', 'right'])
                    start_pos = [0, 0,  # Position that spawns at first
                                 0, 0]  # Goal position to move to

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

                    bandit = Bandit(start_pos, self.ambush_mode)
                    self.bandits.append(bandit)

        def game_reset(self):
            self.victory_transition = self.base_victory_values[:]
            self.defeat_transition = self.base_defeat_values[:]
            self.ambush_start = self.base_ambush_start[:]
            self.begin_start = self.base_begin_start[:]
            self.base_bandit_spawnrate = 240
            self.music.play('menu', -1)
            self.game_state = 'menu'
            self.ambush_mode = False
            self.start_defeat = False
            self.begin_message.blink = False
            self.game_timer = 0
            self.ufo = Ufo()
            self.bandits = []
            self.bullets = []
            self.objects = []
            self.player_1 = None
            self.player_2 = None
            self.player_count = 0
            self.game_tick = 0
            self.draw_map()
        def set_final_score(self):
            new_best = 0
            if self.player_1: new_best += self.player_1.score
            if self.player_2: new_best += self.player_2.score

            if self.full_score < new_best:
                self.full_score = new_best
                self.new_best_text.enabled = True
            else:
                self.new_best_text.enabled = False

        # Merged "draw" function with components state to make bullets possible
        def update_game_state(self):
            keys = pg.key.get_pressed()

            if self.game_state == 'menu':
                SCREEN.fill(MENU_COLOR)
                self.title_text.draw()
                self.choose_text.draw()
                self.volume_text.draw()
                self.full_score_text.rect = (SCREEN_WIDTH / 2, 180)
                self.full_score_text.text = str("SCORE: {:07d}".format(self.full_score))
                self.full_score_text.draw()
                self.new_best_text.draw()
                self.player1_text.draw()
                self.player2_text.draw()

                # Draw characters on screen depending on players joined
                if self.player_1:
                    self.start_text.draw()
                    self.select_error.enabled = False
                    offset1 = 100

                    TITLE_SPRITE_RECT.centerx = SCREEN_WIDTH / 2 - offset1
                    UFO_SPRITE_RECT.centerx = TITLE_SPRITE_RECT.centerx
                    TITLE_SPRITE_EYES_RECT.centery = TITLE_SPRITE_RECT.centery
                    TITLE_SPRITE_EYES_RECT.centerx = TITLE_SPRITE_RECT.centerx - 4

                    SCREEN.blit(TITLE_SPRITE, TITLE_SPRITE_RECT)
                    SCREEN.blit(TITLE_SPRITE_EYES, TITLE_SPRITE_EYES_RECT)
                    SCREEN.blit(UFO_SPRITE, UFO_SPRITE_RECT)
                else:
                    self.select_text.draw()
                if self.player_2:
                    # Apply position offset

                    offset2 = -100

                    TITLE_SPRITE_RECT2.centerx = SCREEN_WIDTH / 2 - offset2
                    UFO_SPRITE_RECT2.centerx = TITLE_SPRITE_RECT2.centerx
                    TITLE_SPRITE_EYES_RECT2.centery = TITLE_SPRITE_RECT2.centery
                    TITLE_SPRITE_EYES_RECT2.centerx = TITLE_SPRITE_RECT2.centerx - 4

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
            elif self.game_state == 'round':
                SCREEN.fill(BACKGROUND_COLOR)

                for terrain in self.terrain:
                    terrain.draw()

                self.ufo.draw_ufo(SCREEN)

                # Creating a random bandit
                number_spawned = 0

                if not self.ambush_mode:
                    number_spawned = randint(1, 2)
                    self.max_bandits = self.base_max_bandits + (2 * self.player_count)
                else:
                    number_spawned = randint(0, 2 + (2 * self.player_count))
                    self.max_bandits = self.base_max_bandits + (4 * self.player_count)

                if self.can_spawn_bandits:
                    self.bandit_position(number_spawned)
                self.bandit_count = len(self.bandits)

                if self.game_tick % FRAMERATE == 0:
                    self.game_timer += 1

                # increasing difficulty every 15 seconds
                if (self.game_tick % (FRAMERATE * self.difficulty_time) == 0
                    and self.base_bandit_spawnrate > 60):
                    self.base_bandit_spawnrate -= 15
                    if self.base_bandit_spawnrate < 60: self.base_bandit_spawnrate = 60

                for item in self.objects:
                    if not item.collected and item.lifetime <= item.despawn_time:
                        item.update()
                        item.check_collect(self.player_1, self.ufo)
                        item.check_collect(self.player_2, self.ufo)
                        item.draw()

                        if self.game_tick % FRAMERATE == 0:
                            item.lifetime += 1
                    else:
                        self.objects.remove(item)

                if not self.victory_transition[0] and not self.defeat_transition[0]:
                    for bandit in self.bandits:
                        if bandit.live_bandit:
                            # Getting a random brick as a target
                            # Allowing broken bricks is by design, or else it would be too unfair
                            if bandit.name != 'bandit_hitman':
                                target = self.ufo.ufos[randint(0, len(self.ufo.ufos) - 1)][0].topleft
                            else:
                                if randint(1, 2) == 1 and self.player_1:
                                    target = self.player_1.rect.topleft
                                elif self.player_2:
                                    target = self.player_2.rect.topleft
                                else:
                                    target = self.player_1.rect.topleft


                            bandit.update(target, self.bullets, self.ufo)
                            possible_loot = bandit.update_bullets(self.bullets)

                            if possible_loot:
                                new_item = Objects(possible_loot, bandit.rect)
                                self.objects.append(new_item)

                            # Checking various collisions with the bandit explosion
                            if bandit.explosion and bandit.explode[1] <= bandit.explode[7]:
                                self.ufo.explosion_collide_check(bandit.explosion)
                                if self.player_1: self.player_1.explosion_collide_check(bandit.explosion)
                                if self.player_2: self.player_1.explosion_collide_check(bandit.explosion)

                            bandit.shield_collide_check(self.player_1)
                            bandit.shield_collide_check(self.player_2)
                            bandit.draw_bandit()
                        else:
                            self.bandits.remove(bandit)

                        if self.game_tick % FRAMERATE == 0:
                            bandit.lifetime += 1

                    # collision of bullets w ufo
                    for bullet in self.bullets:
                        if bullet.is_alive:
                            bullet.update()
                            bullet.shield_collide_check(self.player_1)  # collision w shield player 1
                            bullet.player_collide_check(self.player_1)
                            bullet.player_collide_check(self.player_2)
                            bullet.shield_collide_check(self.player_2)
                            if self.game_tick % FRAMERATE == 0:
                                bullet.lifetime += 1

                            self.ufo.ufo_collide_check(bullet)
                        else:
                            self.bullets.remove(bullet)

                # Player movement check and drawing
                if self.player_1:
                    if not self.defeat_transition[0]:
                        self.player_1.move(keys, self.bullets)
                        self.player_1.draw()
                    self.p1_points_text.text = str("{:05d}".format(self.player_1.score))
                    self.p1_points_text.rect = (90, 30)
                    self.p1_points_text.draw()
                    self.move_tip.text = f'! {self.player_1.controls} keys to move !'
                if self.player_2:
                    if not self.defeat_transition[0]:
                        self.player_2.move(keys, self.bullets)
                        self.player_2.draw()
                    self.p2_points_text.text = str("{:05d}".format(self.player_2.score))
                    self.p2_points_text.rect = (SCREEN_WIDTH - 90, 30)
                    self.p2_points_text.draw()
                    self.move_tip.text = f'! {self.player_1.controls}/{self.player_2.controls} keys to move !'

                time_left = self.round_time - self.game_timer
                seconds = time_left % 60
                minutes = int(time_left / 60) % 60
                self.timer_text.text = f'{minutes:02}:{seconds:02}'

                if self.begin_start[0]:
                    self.begin_message.draw()
                    self.move_tip.draw()
                    self.begin_start[1] += 1

                    if self.begin_start[1] >= (self.begin_start[2] / 1.5):
                        self.begin_message.blink = True
                        self.move_tip.blink = True
                        self.can_spawn_bandits = True
                    if self.begin_start[1] >= self.begin_start[2]:
                        self.begin_start[0] = False

                if not self.victory_transition[0]:
                    # Drawing UI
                    self.timer_text.draw()

                # Toggles ambush mode at a certain point, true challenge begins
                if self.game_timer > self.ambush_time and not self.ambush_mode:
                    self.ambush_mode = True
                    self.ambush_start[5] = True
                    self.ambush_start[8] = True
                    self.music.play_sfx('ambush')
                    self.music.play('BANDIT-RAID', -1)

                if self.ambush_mode:
                    if not self.ambush_start[0]:
                        SCREEN.blit(AMBUSH_FILTER, (0, 0))

                # Apply effects on ambush start
                if self.ambush_start[5]:
                    self.ambush_start[1] += 1
                    self.ambush_start[3] += 1

                    if self.ambush_start[1] >= self.ambush_start[2] and self.ambush_start[0]:
                        self.ambush_start[1] = 0
                        self.ambush_start[0] = False
                    elif self.ambush_start[1] >= self.ambush_start[2] and not self.ambush_start[0]:
                        self.ambush_start[1] = 0
                        self.ambush_start[0] = True
                    if self.ambush_start[3] >= self.ambush_start[4]:
                        self.ambush_start[5] = False
                        self.ambush_start[0] = False
                if self.ambush_start[8] and self.ambush_start[6] <= self.ambush_start[7]:
                    self.ambush_start[6] += 1
                    self.ambush_text.draw()

                # Defeat if ufo is broken, should show a defeat screen with final score
                if self.ufo.fully_broken and not self.defeat_transition[0]:
                    self.defeat_transition[0] = True
                    self.music.play_sfx('ufo_destroy')
                    pg.mixer.stop()
                elif time_left == 0 and not self.victory_transition[0]:
                    self.victory_transition[0] = True
                    self.music.play_sfx('ufo_rebuild')
                    self.music.play('you_should_probably_get_in_the_ufo_now', -1)

                    # Add points for every brick not destroyed at the end
                    for brick in self.ufo.ufos:
                        rect, strength, brick_row = brick
                        if strength > 0:
                            if self.player_1: self.player_1.score += 50
                            if self.player_2: self.player_2.score += 50

                # Entire transition handling for victory cutscene
                if self.victory_transition[0]:
                    if self.victory_transition[-1]:
                        self.victory_transition[0] = False
                        self.music.play('victory', -1)
                        self.game_state = 'victory'
                        self.set_final_score()
                    elif not self.victory_transition[1]:
                        self.get_in.draw()
                        self.ufo.image_mode = True
                        self.victory_transition[1] = self.ufo.victory_ufo(self.player_1, self.player_2)
                    elif self.victory_transition[3] <= self.victory_transition[4]:
                        if not self.victory_transition[2]:
                            self.music.play('escape')
                            self.victory_transition[2] = True

                            if self.player_1: self.player_1.victory = True
                            if self.player_2: self.player_2.victory = True
                        self.victory_transition[3] += 1
                        self.ufo.victory_ufo(self.player_1, self.player_2)
                    elif self.victory_transition[5] <= self.victory_transition[6]:
                        self.victory_transition[5] += 1
                        self.ufo.image_mode = False

                        if self.victory_transition[5] % 8 == 0 and not self.victory_transition[7]:
                            SCREEN.fill(VICTORY_COLOR)
                            self.victory_transition[7] = True
                        elif self.victory_transition[5] % 8 == 0 and self.victory_transition[7]:
                            SCREEN.fill(BACKGROUND_COLOR)
                            self.victory_transition[7] = False
                    else:
                        self.victory_transition[7] = False
                        self.victory_transition[-1] = True
                        UFO_SPRITE_RECT.center = (SCREEN_WIDTH / 2, 420)
                        TITLE_SPRITE_RECT.center = (SCREEN_WIDTH / 2, 440)
                        WIN_SPRITE_EYES_RECT.center = TITLE_SPRITE_RECT.center
                        TITLE_SPRITE_RECT2.center = (SCREEN_WIDTH / 2, 440 + P2_TITLE_OFFSET)
                        WIN_SPRITE_EYES_RECT2.center = TITLE_SPRITE_RECT2.center

                # Entire transition handling for defeat cutscene
                if self.defeat_transition[0]:
                    if self.defeat_transition[-1]:
                        self.defeat_transition[0] = False
                        self.music.play('defeat')
                        self.game_state = 'defeat'
                        self.set_final_score()
                    elif self.defeat_transition[1] <= self.defeat_transition[2]:
                        self.defeat_transition[1] += 1
                        self.ufo.blink[0] = True
                        if not self.start_defeat:
                            self.start_defeat = True
                            self.music.play('remove')
                            self.music.play_sfx('ufo_destroy')
                    elif self.defeat_transition[3] <= self.defeat_transition[4]:
                        self.defeat_transition[3] += 1
                        self.ufo.blink[0] = False

                        if self.defeat_transition[3] % 8 == 0 and not self.defeat_transition[5]:
                            SCREEN.fill(DEFEAT_COLOR)
                            self.defeat_transition[5] = True
                        elif self.defeat_transition[3] % 8 == 0 and self.defeat_transition[5]:
                            SCREEN.fill(BACKGROUND_COLOR)
                            self.defeat_transition[5] = False
                    else:
                        self.defeat_transition[5] = False
                        self.defeat_transition[-1] = True


            elif self.game_state == 'victory':
                SCREEN.fill(VICTORY_COLOR)
                self.survived_text.draw()
                self.final_message.draw()
                self.final_message2.draw()

                self.full_score_text.rect = (265, 250)
                self.full_score_text.text = str("FINAL SCORE: {:07d}".format(self.full_score))
                self.full_score_text.draw()
                self.return_text.draw()

                # Draw victory stats and players
                if self.player_1:
                    self.select_error.enabled = False
                    offset1 = -100
                    TITLE_SPRITE_RECT.centerx = SCREEN_WIDTH / 2 - offset1
                    UFO_SPRITE_RECT.centerx = SCREEN_WIDTH / 2 - offset1
                    WIN_SPRITE_EYES_RECT.centerx = (SCREEN_WIDTH / 2) - 4 - offset1

                    SCREEN.blit(TITLE_SPRITE, TITLE_SPRITE_RECT)
                    SCREEN.blit(WIN_SPRITE_EYES, WIN_SPRITE_EYES_RECT)
                    SCREEN.blit(UFO_SPRITE, UFO_SPRITE_RECT)

                    self.p1_points_text.text = str("PLAYER 1: {:05d}".format(self.player_1.score))
                    self.p1_points_text.rect = (195, 300)
                    self.p1_points_text.draw()
                if self.player_2:
                    # Apply position offset
                    offset2 = -300

                    TITLE_SPRITE_RECT2.centerx = SCREEN_WIDTH / 2 - offset2
                    UFO_SPRITE_RECT2.centerx = TITLE_SPRITE_RECT2.centerx
                    WIN_SPRITE_EYES_RECT2.centerx = TITLE_SPRITE_RECT2.centerx - 4

                    SCREEN.blit(TITLE_SPRITE2, TITLE_SPRITE_RECT2)
                    SCREEN.blit(WIN_SPRITE_EYES2, WIN_SPRITE_EYES_RECT2)
                    SCREEN.blit(UFO_SPRITE2, UFO_SPRITE_RECT2)

                    self.p2_points_text.text = str("PLAYER 2: {:05d}".format(self.player_2.score))
                    self.p2_points_text.rect = (200, 350)
                    self.p2_points_text.draw()
                if self.game_tick % int(self.menu_loop[0] / 1.5) == 0:
                    if self.menu_loop[1]:
                        TITLE_SPRITE_RECT.y -= 15
                        WIN_SPRITE_EYES_RECT.y -= 15
                        UFO_SPRITE_RECT.y -= 15
                        TITLE_SPRITE_RECT2.y += 15
                        WIN_SPRITE_EYES_RECT2.y += 15
                        UFO_SPRITE_RECT2.y += 15
                        self.menu_loop[1] = False
                    else:
                        TITLE_SPRITE_RECT.y += 15
                        WIN_SPRITE_EYES_RECT.y += 15
                        UFO_SPRITE_RECT.y += 15
                        TITLE_SPRITE_RECT2.y -= 15
                        WIN_SPRITE_EYES_RECT2.y -= 15
                        UFO_SPRITE_RECT2.y -= 15
                        self.menu_loop[1] = True
            elif self.game_state == 'defeat':
                SCREEN.fill(DEFEAT_COLOR)
                self.lost_text.draw()
                self.full_score_text.rect = (265, 250)
                self.full_score_text.text = str("FINAL SCORE: {:07d}".format(self.full_score))
                self.full_score_text.draw()
                self.return_text.draw()

                # Draw defeat stats and players
                if self.player_1:
                    rect_offset = 0
                    if self.player_2: rect_offset = -60

                    self.player_1.defeated = True
                    self.player_1.rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT - 200)
                    self.player_1.draw([-4, 2], rect_offset)
                if self.player_2:
                    rect_offset = 60
                    self.player_2.defeated = True
                    self.player_2.rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT - 200)
                    self.player_2.draw([4, 2], rect_offset)

                SCREEN.blit(DEFEAT_CAGE, DEFEAT_CAGE_RECT)

            if self.select_error.enabled:
                self.select_error.draw()

            pg.display.flip()
