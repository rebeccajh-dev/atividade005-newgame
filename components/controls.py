from components.instances.player import Player
from components.screen.display import hud_message_update
from config import SCREEN_WIDTH, SCREEN_HEIGHT, PLAYER_COLORS

import pygame as pg
import sys

sound_key_table = [pg.K_PLUS, pg.K_EQUALS, pg.K_MINUS, pg.K_LEFTBRACKET, pg.K_RIGHTBRACKET, pg.K_LEFTPAREN, pg.K_RIGHTPAREN]

def handle_events(game):
    keys = pg.key.get_pressed()

    # Player movement check
    if not game.defeat:
        if game.player_1:
            game.player_1.move(game, keys)
        if game.player_2:
            game.player_2.move(game, keys)

    # Detecting player joining the components
    if game.game_state == 'menu' or game.game_state == 'round':
        if keys[pg.K_w] or keys[pg.K_a] or keys[pg.K_s] or keys[pg.K_d]:
            if not game.player_1:
                color = PLAYER_COLORS[game.player_count]
                game.player_count += 1
                game.player_1 = Player('WASD', game.player_count, color)
                game.player_1.rect.center = ((SCREEN_WIDTH / 2) - 120, SCREEN_HEIGHT / 2)
                game.sound.play_sfx('join')
            elif not game.player_2 and game.player_1.controls != 'WASD':
                color = PLAYER_COLORS[game.player_count]
                game.player_count += 1
                game.player_2 = Player('WASD', game.player_count, color)
                game.player_2.rect.center = ((SCREEN_WIDTH / 2) + 120, SCREEN_HEIGHT / 2)
                game.sound.play_sfx('join')
        if keys[pg.K_UP] or keys[pg.K_LEFT] or keys[pg.K_DOWN] or keys[pg.K_RIGHT]:
            if not game.player_1:
                color = PLAYER_COLORS[game.player_count]
                game.player_count += 1
                game.player_1 = Player('ARROWS', game.player_count, color)
                game.player_1.rect.center = ((SCREEN_WIDTH / 2) - 120, SCREEN_HEIGHT / 2)
                game.sound.play_sfx('join')
            elif not game.player_2 and game.player_1.controls != 'ARROWS':
                color = PLAYER_COLORS[game.player_count]
                game.player_count += 1
                game.player_2 = Player('ARROWS', game.player_count, color)
                game.player_2.rect.center = ((SCREEN_WIDTH / 2) + 120, SCREEN_HEIGHT / 2)
                game.sound.play_sfx('join')


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
        if game.game_state == 'menu' and (game.player_1 or game.player_2):
            game.player_count = 0
            game.sound.play_sfx('remove')
            game.player_1 = None
            game.player_2 = None

    if keys[pg.K_0] and not game.sound.button_pressed:
        if game.sound.mute: game.text.muted.string = f'MUTE DISABLED'
        else: game.text.muted.string = f'MUTE ENABLED'
        hud_message_update(game, game.text.muted)
        game.sound.mute_music()

    if ((keys[pg.K_EQUALS] or keys[pg.K_PLUS] )
        and not game.sound.button_pressed):
        game.sound.change_volume('increase')
        game.text.music_change_vol.string = f'+ Music: {int(10 * game.sound.volume_offset)}'
        hud_message_update(game, game.text.music_change_vol)
    if (keys[pg.K_MINUS]
        and not game.sound.button_pressed):
        game.sound.change_volume('decrease')
        game.text.music_change_vol.string = f'- Music: {int(10 * game.sound.volume_offset)}'
        hud_message_update(game, game.text.music_change_vol)
    if ((keys[pg.K_RIGHTBRACKET] or keys[pg.K_RIGHTPAREN])
        and not game.sound.button_pressed):
        game.sound.change_volume_sfx('increase')
        game.text.sfx_change_vol.string = f'+ SFX: {int(10 * game.sound.sfx_offset)}'
        hud_message_update(game, game.text.sfx_change_vol)
    if ((keys[pg.K_LEFTBRACKET] or keys[pg.K_LEFTPAREN])
        and not game.sound.button_pressed):
        game.sound.change_volume_sfx('decrease')
        game.text.sfx_change_vol.string = f'- SFX: {int(10 * game.sound.sfx_offset)}'
        hud_message_update(game, game.text.sfx_change_vol)

    for event in pg.event.get():
        # Quit the components
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()

        if event.type == pg.KEYUP:
            if event.key == pg.K_0:
                game.sound.button_pressed = False
            if event.key in sound_key_table:
                game.sound.button_pressed = False