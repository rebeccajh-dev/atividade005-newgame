"""
Module for loading and configuring components assets.

This module handles the initialization of fonts and the loading and transformation
of image resources. It centralizes asset management to keep the main code clean.
"""

import pygame as pg
from config import SCREEN_WIDTH, SCREEN_HEIGHT, BASE_PLAYER_SIZE, P2_TITLE_OFFSET

pg.init()

# Font configuration
SMALL_FONT = pg.font.Font("assets/retro_font.ttf", 16)
TEXT_FONT = pg.font.Font("assets/retro_font.ttf", 24)
NORMAL_FONT = pg.font.Font("assets/retro_font.ttf", 40)
TITLE_FONT = pg.font.Font("assets/retro_font.ttf", 72)

# Image configuration
TITLE_SPRITE = pg.image.load('assets/player_sprites/1/body.png')
TITLE_SPRITE = pg.transform.scale(TITLE_SPRITE, BASE_PLAYER_SIZE)
TITLE_SPRITE_RECT = TITLE_SPRITE.get_rect()
TITLE_SPRITE_RECT.center = (SCREEN_WIDTH // 2, 440)

TITLE_SPRITE2 = pg.image.load('assets/player_sprites/2/body.png')
TITLE_SPRITE2 = pg.transform.scale(TITLE_SPRITE2, BASE_PLAYER_SIZE)
TITLE_SPRITE_RECT2 = TITLE_SPRITE2.get_rect()
TITLE_SPRITE_RECT2.center = (SCREEN_WIDTH // 2, 440 + P2_TITLE_OFFSET)

TITLE_SPRITE_EYES = pg.image.load('assets/player_sprites/1/eyes.png')
TITLE_SPRITE_EYES = pg.transform.scale(TITLE_SPRITE_EYES, BASE_PLAYER_SIZE)
TITLE_SPRITE_EYES_RECT = TITLE_SPRITE_EYES.get_rect()
TITLE_SPRITE_EYES_RECT.center = ((SCREEN_WIDTH // 2) - 4, 440)

TITLE_SPRITE_EYES2 = pg.image.load('assets/player_sprites/1/eyes.png')
TITLE_SPRITE_EYES2 = pg.transform.scale(TITLE_SPRITE_EYES2, BASE_PLAYER_SIZE)
TITLE_SPRITE_EYES_RECT2 = TITLE_SPRITE_EYES2.get_rect()
TITLE_SPRITE_EYES_RECT2.center = ((SCREEN_WIDTH // 2) - 4, 440 + P2_TITLE_OFFSET)

WIN_SPRITE_EYES = pg.image.load('assets/player_sprites/1/happy_eyes.png')
WIN_SPRITE_EYES = pg.transform.scale(WIN_SPRITE_EYES, BASE_PLAYER_SIZE)
WIN_SPRITE_EYES_RECT = WIN_SPRITE_EYES.get_rect()
WIN_SPRITE_EYES_RECT.center = ((SCREEN_WIDTH // 2) - 4, 440)

WIN_SPRITE_EYES2 = pg.image.load('assets/player_sprites/1/happy_eyes.png')
WIN_SPRITE_EYES2 = pg.transform.scale(WIN_SPRITE_EYES2, BASE_PLAYER_SIZE)
WIN_SPRITE_EYES_RECT2 = WIN_SPRITE_EYES2.get_rect()
WIN_SPRITE_EYES_RECT2.center = ((SCREEN_WIDTH // 2) - 4, 440 + P2_TITLE_OFFSET)

UFO_SPRITE = pg.image.load('assets/UFO.png')
UFO_SPRITE = pg.transform.scale(UFO_SPRITE, (150, 150))
UFO_SPRITE_RECT = UFO_SPRITE.get_rect()
UFO_SPRITE_RECT.center = (SCREEN_WIDTH / 2, 420)

UFO_SPRITE2 = pg.image.load('assets/UFO2.png')
UFO_SPRITE2 = pg.transform.scale(UFO_SPRITE2, (150, 150))
UFO_SPRITE_RECT2 = UFO_SPRITE2.get_rect()
UFO_SPRITE_RECT2.center = (SCREEN_WIDTH / 2, 420 + P2_TITLE_OFFSET)

DEFEAT_CAGE = pg.image.load('assets/defeat_cage.png')
DEFEAT_CAGE = pg.transform.scale(DEFEAT_CAGE, (int(110 * 5), int(30 * 5)))
DEFEAT_CAGE_RECT = DEFEAT_CAGE.get_rect()
DEFEAT_CAGE_RECT.center = ((SCREEN_WIDTH // 2), SCREEN_HEIGHT - 200)