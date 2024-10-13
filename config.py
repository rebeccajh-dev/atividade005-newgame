"""
Module for storing configuration constants and settings for the components.

This module contains variables related to screen configuration, color settings,
components constants, and interface-related configurations.
"""

import pygame as pg

# Screen configuration
SCREEN_WIDTH = 960
SCREEN_HEIGHT = 620
FRAMERATE = 60
SCREEN = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Basic color configuration
PLAYER_COLORS = [(120, 255, 120), (200, 120, 200)]
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_RED = (255, 0, 0)
COLOR_DAMAGED = (160, 0, 0, 128)
UFO_COLORS = [
    [   # Brick power 1
        (240, 240, 240),
        (240, 240, 240),
        (240, 240, 240),
        (100, 200, 100),
        (100, 200, 100)
    ],
    [   # Brick power 2
        (240, 240, 180),
        (240, 240, 180),
        (240, 240, 180),
        (150, 200, 60),
        (150, 200, 60)
    ],
    [   # Brick power 3+
        (240, 240, 100),
        (240, 240, 100),
        (240, 240, 100),
        (200, 230, 20),
        (200, 230, 20)
    ],
]

# Constant variables
BASE_PLAYER_SIZE = (50, 50)
BASE_SHIELD_X = 130
BASE_SHIELD_Y = 20
SHIELD_DISTANCE = 70

BASE_PLAYER_SPEED = 4
BASE_ENEMY_SPEED = 2
MAX_BULLET_SPEED = 5
RANDOM_MOVE = [-1, -0.5, 0.25, 0, 0.25, 0.5, 1]

# Interface configuration
P2_TITLE_OFFSET = 15

# Global variables
MENU_COLOR = (10, 10, 30)
VICTORY_COLOR = (30, 20, 50)
DEFEAT_COLOR = (50, 15, 0)
AMBUSH_COLOR = (50, 35, 10)
SQUARE_SIZE = 25

AMBUSH_FILTER = pg.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pg.SRCALPHA)
AMBUSH_FILTER.fill((180, 80, 0, 50))  # 128 is the alpha value (0 is fully

# Level configuration
LEVEL1_CONFIG = {
    "background": (50, 30, 0),
    "spawn_types":
        [
            # 0 = Name, 1 = Chance, 2 = Only on Ambush, 3 = Ambush chance increment
            ["basic_bandit", 80, False, -15],
            ["skilled_bandit", 20, False, 10],
            ["bomb_bandit", 15, True, 0],
            ["bandit_hitman", 10, True, 0],
        ],
    "enviroment":
        [
            # 0 = Name, 1 = Size, 2 = Color, 3 = Chance
            ['cactus1', 70, (40, 110, 60), 10],
            ['cactus2', 70, (40, 110, 60), 10],
            ['rock', 70, (80, 60, 40), 5],
            ['tumbleweed', 70, (80, 70, 50), 7],
            ['large_rock', 140, (80, 60, 40), 3],
        ],
    "terrain_spacing": 8,
    "terrain_area_reduction": 1.7,

}

LEVEL2_CONFIG = {
    "background": (60, 40, 35),
    "spawn_types":
        [
            # 0 = Name, 1 = Chance, 2 = Only on Ambush, 3 = Ambush chance increment
            ["basic_bandit", 80, False, -15],
            ["cards_bandit", 15, False, 5],
            ["table_bandit", 15, False, 5],
            ["bandit_hitman", 10, True, 0],
            ["drunk_bandit", 25, True, 0],
        ],
    "enviroment":
        [
            # 0 = Name, 1 = Size, 2 = Color, 3 = Chance
            ['table', 100, (100, 60, 65), 50],
            ['large_table', 200, (100, 60, 65), 20],
            ['broken_table', 100, (100, 60, 65), 10],
            ['small_bottle', 100, (155, 130, 80), 5],
            ['funny_chair', 100, (100, 60, 65), 5],
            ['jukebox', 140, (110, 80, 40), 3],
            ['arcade_machine', 140, (100, 90, 50), 3],
        ],
    "terrain_spacing": 10,
    "terrain_area_reduction": 1.5,

}

LEVEL3_CONFIG = {
    "background": (30, 25, 20),
    "spawn_types":
        [
            # 0 = Name, 1 = Chance, 2 = Only on Ambush, 3 = Ambush chance increment
            ["skilled_bandit", 80, False, -10],
            ["bomb_bandit", 20, False, 20],
            ["bandit_hitman", 10, True, 0],
        ],
    "enviroment":
        [
            # 0 = Name, 1 = Size, 2 = Color, 3 = Chance
            ['rock', 70, (50, 40, 30), 10],
            ['dead_bush', 70, (60, 55, 15), 10],
            ['fossil1', 70, (130, 130, 130), 15],
            ['fossil2', 50, (130, 130, 130), 15],
            ['dead_tree', 140, (70, 60, 35), 8],
            ['large_fossil', 140, (130, 130, 130), 5],
        ],
    "terrain_spacing": 10,
    "terrain_area_reduction": 2,

}