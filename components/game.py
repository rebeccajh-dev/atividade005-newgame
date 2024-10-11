"""
Class that initializes the main logic of the components and handles events.
"""
import random

from random import randint, choice

from components.instances.ufo import Ufo
from components.screen import display
from components.screen import levels
from components.text import Text
from components.sound import Sound
from components.controls import handle_events
from components.physics import update_physics

from assets import TITLE_SPRITE
from config import SCREEN_WIDTH, SCREEN_HEIGHT, FRAMERATE, PLAYER_COLORS, SCREEN, P2_TITLE_OFFSET

import pygame as pg

class Game:
    def __init__(self):
        # Setting up the display window customization
        pg.display.set_icon(TITLE_SPRITE)
        pg.display.set_caption('WESTERN RAID v1.0')

        self.game_state = 'menu'
        self.clock = pg.time.Clock()
        self.player_1 = None
        self.player_2 = None
        self.level = None
        self.player_count = 0
        self.game_tick = 0
        self.game_timer = 0
        self.full_score = 0
        self.round_time = 240

        # Bandit settings
        self.base_max_bandits = 3 # Limit of bandits on screen
        self.max_bandits = self.base_max_bandits
        self.max_spawned = 2  # Maximum number of bandits that can spawn at once
        self.bandit_count = 0
        self.base_bandit_spawnrate = 240
        self.bandit_spawn_multi = [1, 2] # First for normal mode, second for ambush
        self.can_spawn_bandits = False

        # Base Ambush settings
        self.ambush_mode = False
        self.ambush_time = randint(2, 3)
        self.difficulty_time = 15  # Time in seconds of when difficulty increases

        # Getting classes
        self.sound = Sound()
        self.text = Text()
        self.ufo = Ufo()

        # List for instances to render and update
        self.objects = []
        self.bullets = []
        self.bandits = []
        self.terrain = []

        # These lists are used for "animations" or effects
        self.menu_loop = [35, False]
        self.start_animate = True

        self.base_ambush_start = [False, 0, 5, 0, 60, False, 0, 300, False]
        self.base_begin_start = [True, 0, 600]
        self.begin_start = self.base_begin_start[:]
        self.ambush_start = self.base_ambush_start[:]
        self.start_defeat = False
        self.base_defeat_values = [
            False,  # Transition enabled
            0, 120,  # UFO blinking animation timer
            0, 60,  # Screen transition timer
            False,  # Screen clearing condition
            False  # Final check for defeat
        ]

        self.base_victory_values = [
            False,  # Transition enabled
            False,  # Condition for getting the players inside
            False,  # Condition for song to play
            0, 400,  # Ufo flying back to space animation timer
            0, 60,  # Screen transition timer
            0, 60, # Black screen timer
            False,  # Screen clearing condition
            False  # Final check for victory
        ]
        self.victory_transition = self.base_victory_values[:]
        self.defeat_transition = self.base_defeat_values[:]

        # Loading some starter stuff
        self.level = levels.create_map(self)
        self.sound.play('menu', -1)

    def run(self):
        while True:
            self.update_game_state()
            handle_events(self)

            self.clock.tick(FRAMERATE)
            self.game_tick += 1

    def game_reset(self):
        self.victory_transition = self.base_victory_values[:]
        self.defeat_transition = self.base_defeat_values[:]
        self.ambush_start = self.base_ambush_start[:]
        self.begin_start = self.base_begin_start[:]
        self.base_bandit_spawnrate = 240
        self.sound.play('menu', -1)
        self.game_state = 'menu'
        self.ambush_mode = False
        self.start_defeat = False
        self.text.begin_message.blink = False
        self.game_timer = 0
        self.ufo = Ufo()
        self.bandits = []
        self.bullets = []
        self.objects = []
        self.player_1 = None
        self.player_2 = None
        self.player_count = 0
        self.game_tick = 0
        levels.create_map(self)

    def set_final_score(self):
        new_best = 0
        if self.player_1: new_best += self.player_1.score
        if self.player_2: new_best += self.player_2.score

        if self.full_score < new_best:
            self.full_score = new_best
            self.text.new_best_text.enabled = True
        else:
            self.text.new_best_text.enabled = False

    # Merged "draw" function with components state to make bullets possible
    def update_game_state(self):
        if self.game_state == 'menu':
            display.render_menu(self)
        elif self.game_state == 'round':
            update_physics(self)
            display.render_round(self)
        elif self.game_state == 'victory':
            display.render_victory(self)
        elif self.game_state == 'defeat':
            display.render_defeat(self)

        pg.display.flip()
