from components.instances.player import Player
from config import SCREEN_WIDTH, SCREEN_HEIGHT, PLAYER_COLORS

import pygame as pg
import sys

def handle_events(game):
    keys = pg.key.get_pressed()

    # Player movement check
    if game.player_1:
        if not game.defeat_transition[0]:
            game.player_1.move(keys, game.bullets)
    if game.player_2:
        if not game.defeat_transition[0]:
            game.player_2.move(keys, game.bullets)

    # Detecting player joining the components
    if game.game_state == 'menu' or game.game_state == 'round':
        if keys[pg.K_w] or keys[pg.K_a] or keys[pg.K_s] or keys[pg.K_d]:
            if not game.player_1:
                color = PLAYER_COLORS[game.player_count]
                game.player_count += 1
                game.player_1 = Player('WASD', game.player_count, color)
                game.player_1.rect.center = ((SCREEN_WIDTH / 2) - 120, SCREEN_HEIGHT / 2)
            elif not game.player_2 and game.player_1.controls != 'WASD':
                color = PLAYER_COLORS[game.player_count]
                game.player_count += 1
                game.player_2 = Player('WASD', game.player_count, color)
                game.player_2.rect.center = ((SCREEN_WIDTH / 2) + 120, SCREEN_HEIGHT / 2)
        if keys[pg.K_UP] or keys[pg.K_LEFT] or keys[pg.K_DOWN] or keys[pg.K_RIGHT]:
            if not game.player_1:
                color = PLAYER_COLORS[game.player_count]
                game.player_count += 1
                game.player_1 = Player('ARROWS', game.player_count, color)
                game.player_1.rect.center = ((SCREEN_WIDTH / 2) - 120, SCREEN_HEIGHT / 2)
            elif not game.player_2 and game.player_1.controls != 'ARROWS':
                color = PLAYER_COLORS[game.player_count]
                game.player_count += 1
                game.player_2 = Player('ARROWS', game.player_count, color)
                game.player_2.rect.center = ((SCREEN_WIDTH / 2) + 120, SCREEN_HEIGHT / 2)

    if keys[pg.K_RETURN]:
        if game.game_state == 'menu':
            if game.player_1:
                game.sound.play('sandwreck', -1)
                game.game_state = 'round'
            else:
                game.text.select_error.enabled = True
        if game.game_state == 'victory' or game.game_state == 'defeat':
            game.game_reset()

    if keys[pg.K_BACKSPACE]:
        if game.game_state == 'menu':
            game.player_count = 0
            game.player_1 = None
            game.player_2 = None

    if keys[pg.K_0]:
        game.sound.mute_music()

    if keys[pg.K_EQUALS] or keys[pg.K_PLUS]:
        game.sound.change_volume('increase')
    if keys[pg.K_MINUS]:
        game.sound.change_volume('decrease')

    for event in pg.event.get():
        # Quit the components
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()

        if event.type == pg.KEYUP:
            if event.key == pg.K_0:
                game.sound.button_pressed = False
            if event.key == pg.K_PLUS or event.key == pg.K_EQUALS or event.key == pg.K_MINUS:
                game.sound.button_pressed = False