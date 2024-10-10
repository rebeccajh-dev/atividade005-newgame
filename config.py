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
COLOR_DAMAGED = (160, 0, 0)
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

TERRAIN_COLORS = [
    (0, 0, 0),
    (40, 110, 60),
    (40, 110, 60),
    (80, 60, 40),
    (80, 60, 40),
    (80, 70, 50),
    (65, 45, 40),
    (70, 50, 35),
    (130, 130, 130),
    (130, 130, 130),
    (130, 130, 130),
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
BACKGROUND_COLOR = (40, 20, 0)
DEFEAT_COLOR = (50, 15, 0)
AMBUSH_COLOR = (50, 35, 10)
SQUARE_SIZE = 25

AMBUSH_FILTER = pg.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pg.SRCALPHA)
AMBUSH_FILTER.fill((180, 80, 0, 50))  # 128 is the alpha value (0 is fully


