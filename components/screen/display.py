from assets import TITLE_FONT, TEXT_FONT, NORMAL_FONT, TITLE_SPRITE, TITLE_SPRITE_RECT, TITLE_SPRITE_EYES, UFO_SPRITE, \
    TITLE_SPRITE_EYES_RECT, UFO_SPRITE_RECT, TITLE_SPRITE_RECT2, UFO_SPRITE_RECT2, TITLE_SPRITE_EYES_RECT2, \
    TITLE_SPRITE2, TITLE_SPRITE_EYES2, UFO_SPRITE2, SMALL_FONT, WIN_SPRITE_EYES, WIN_SPRITE_EYES2, WIN_SPRITE_EYES_RECT, \
    WIN_SPRITE_EYES_RECT2, DEFEAT_CAGE, DEFEAT_CAGE_RECT

from config import SCREEN_WIDTH, COLOR_WHITE, COLOR_RED, SCREEN_HEIGHT, FRAMERATE, PLAYER_COLORS, MENU_COLOR, SCREEN, \
    AMBUSH_FILTER, VICTORY_COLOR, DEFEAT_COLOR, P2_TITLE_OFFSET

import pygame as pg

def hud_message_update(game, new_text):
    game.text.HUD_text_list[0] = new_text
    game.text.HUD_text_list[1] = 0
    game.text.HUD_text_list[3] = True

def always_render(game):
    if game.text.HUD_text_list[0] and game.text.HUD_text_list[3]:
        game.text.HUD_text_list[1] += 1
        game.text.HUD_text_list[0].draw()

        if game.text.HUD_text_list[1] >= game.text.HUD_text_list[2]:
            game.text.HUD_text_list[3] = False
            game.text.HUD_text_list[1] = 0

''' ============================================================= '''
''' ========== HANDLING EVERYTHING THAT SHOWS IN MENU  ========== '''
''' ============================================================= '''
def render_menu(game):
    SCREEN.fill(MENU_COLOR)
    game.stars.update(game)

    game.text.title_text.draw()
    game.text.choose_text.draw()
    game.text.volume_text.draw()
    game.text.full_score_text.rect = (SCREEN_WIDTH / 2, 180)
    game.text.full_score_text.string = str("SCORE: {:07d}".format(game.full_score))
    game.text.full_score_text.draw()
    game.text.new_best_text.draw()
    game.text.player1_text.draw()
    game.text.player2_text.draw()

    # Draw characters on screen depending on players joined
    if game.player_1:
        game.text.start_text.draw()
        game.text.select_error.enabled = False
        offset1 = 100

        TITLE_SPRITE_RECT.centerx = SCREEN_WIDTH / 2 - offset1
        UFO_SPRITE_RECT.centerx = TITLE_SPRITE_RECT.centerx
        TITLE_SPRITE_EYES_RECT.centery = TITLE_SPRITE_RECT.centery
        TITLE_SPRITE_EYES_RECT.centerx = TITLE_SPRITE_RECT.centerx - 4

        SCREEN.blit(TITLE_SPRITE, TITLE_SPRITE_RECT)
        SCREEN.blit(TITLE_SPRITE_EYES, TITLE_SPRITE_EYES_RECT)
        SCREEN.blit(UFO_SPRITE, UFO_SPRITE_RECT)
    else:
        game.text.select_text.draw()
    if game.player_2:
        # Apply position offset

        offset2 = -100

        TITLE_SPRITE_RECT2.centerx = SCREEN_WIDTH / 2 - offset2
        UFO_SPRITE_RECT2.centerx = TITLE_SPRITE_RECT2.centerx
        TITLE_SPRITE_EYES_RECT2.centery = TITLE_SPRITE_RECT2.centery
        TITLE_SPRITE_EYES_RECT2.centerx = TITLE_SPRITE_RECT2.centerx - 4

        SCREEN.blit(TITLE_SPRITE2, TITLE_SPRITE_RECT2)
        SCREEN.blit(TITLE_SPRITE_EYES2, TITLE_SPRITE_EYES_RECT2)
        SCREEN.blit(UFO_SPRITE2, UFO_SPRITE_RECT2)
    if game.game_tick % game.menu_loop[0] == 0:
        if game.menu_loop[1]:
            TITLE_SPRITE_RECT.y -= 15
            TITLE_SPRITE_EYES_RECT.y -= 15
            UFO_SPRITE_RECT.y -= 15
            TITLE_SPRITE_RECT2.y += 15
            TITLE_SPRITE_EYES_RECT2.y += 15
            UFO_SPRITE_RECT2.y += 15
            game.menu_loop[1] = False
        else:
            TITLE_SPRITE_RECT.y += 15
            TITLE_SPRITE_EYES_RECT.y += 15
            UFO_SPRITE_RECT.y += 15
            TITLE_SPRITE_RECT2.y -= 15
            TITLE_SPRITE_EYES_RECT2.y -= 15
            UFO_SPRITE_RECT2.y -= 15
            game.menu_loop[1] = True

    if game.text.select_error.enabled:
        game.text.select_error.draw()


''' ============================================================= '''
''' ========== HANDLING EVERYTHING THAT SHOWS IN ROUND ========== '''
''' ============================================================= '''
def render_round(game):
    SCREEN.fill(game.level.background_color)
    if game.stars.enabled: game.stars.enabled = False

    for terrain in game.level.map:
        terrain.draw()

    if game.player_1:
        if not game.defeat_transition[0]: game.player_1.draw()
        game.text.p1_points_text.string = str("{:05d}".format(game.player_1.score))
        game.text.p1_points_text.rect = (90, 30)
        game.text.p1_points_text.draw()
        game.text.move_tip.string = f'! {game.player_1.controls} keys to move !'
    if game.player_2:
        if not game.defeat_transition[0]: game.player_2.draw()
        game.text.p2_points_text.string = str("{:05d}".format(game.player_2.score))
        game.text.p2_points_text.rect = (SCREEN_WIDTH - 90, 30)
        game.text.p2_points_text.draw()
        game.text.move_tip.string = f'! {game.player_1.controls}/{game.player_2.controls} keys to move !'

    for terrain in game.level.map:
        if terrain.size < 90:
            terrain_Zindex = terrain.rect.y + int(terrain.size / 2)
        else:
            terrain_Zindex = terrain.rect.y + int(terrain.size / 1.4)

        if game.player_1 and game.player_1.rect.centery <= terrain_Zindex:
            terrain.draw()
        elif game.player_2 and game.player_2.rect.centery <= terrain_Zindex:
            terrain.draw()

    game.ufo.draw_ufo(game)

    for item in game.objects:
        item.draw()

    for bandit in game.bandits:
        bandit.draw()

    for bullet in game.bullets:
        bullet.draw()

    time_left = game.round_time - game.game_timer
    seconds = time_left % 60
    minutes = int(time_left / 60) % 60
    game.text.timer_text.string = f'{minutes:02}:{seconds:02}'

    if game.begin_start[0]:
        game.text.begin_message.draw()
        game.text.move_tip.draw()
        game.begin_start[1] += 1

        if game.begin_start[1] >= (game.begin_start[2] / 1.5):
            game.text.begin_message.blink = True
            game.text.move_tip.blink = True
            game.can_spawn_bandits = True
        if game.begin_start[1] >= game.begin_start[2]:
            game.begin_start[0] = False

    if not game.victory_transition[0]:
        # Drawing UI
        game.text.timer_text.draw()

    ''' AMBUSH MODE PROCESS '''
    if (game.game_timer > game.ambush_time and not game.ambush_mode
            and not game.victory and not game.defeat):
        game.ambush_mode = True
        game.ambush_start[5] = True
        game.ambush_start[8] = True
        game.sound.play_sfx('ambush')
        game.sound.play('BANDIT-RAID', -1)
        game.ambush_fog.enabled = True

    game.ambush_fog.update(game)
    if game.ambush_mode:
        if not game.ambush_start[0]:
            SCREEN.blit(AMBUSH_FILTER, (0, 0))

    # Apply effects on ambush start
    if game.ambush_start[5]:
        game.ambush_start[1] += 1
        game.ambush_start[3] += 1

        if game.ambush_start[1] >= game.ambush_start[2] and game.ambush_start[0]:
            game.ambush_start[1] = 0
            game.ambush_start[0] = False
        elif game.ambush_start[1] >= game.ambush_start[2] and not game.ambush_start[0]:
            game.ambush_start[1] = 0
            game.ambush_start[0] = True
        if game.ambush_start[3] >= game.ambush_start[4]:
            game.ambush_start[5] = False
            game.ambush_start[0] = False
    if game.ambush_start[8] and game.ambush_start[6] <= game.ambush_start[7]:
        game.ambush_start[6] += 1
        game.text.ambush_text.draw()

    # Defeat if ufo is broken, should show a defeat screen with final score
    if game.ufo.fully_broken and not game.defeat_transition[0]:
        game.defeat_transition[0] = True
        game.ambush_fog.enabled = False
        game.sound.play_sfx('ufo_destroy')
        pg.mixer.stop()
    elif time_left < 0 and not game.victory_transition[0]:
        game.victory_transition[0] = True
        game.can_spawn_bandits = False
        game.ambush_fog.enabled = False
        game.sound.play('none')

        # Add points for every brick not destroyed at the end
        for brick in game.ufo.ufos:
            rect, strength, brick_row, surface = brick
            game.sound.play_sfx('brick_build')
            if strength > 0:
                if game.player_1: game.player_1.score += 50
                if game.player_2: game.player_2.score += 50

                brick[1] = 100
                game.sound.play_sfx('points')
            else:
                brick[1] = 1

            pg.time.delay(100)

            # Drawing temporary screen for UFO points effect
            SCREEN.fill(game.level.background_color)
            game.ufo.draw_ufo(game)
            for terrain in game.level.map:
                terrain.draw()

            pg.display.flip()

        pg.time.delay(1000)

        game.sound.play('you_should_probably_get_in_the_ufo_now', -1)
        game.sound.play_sfx('ufo_rebuild')


    ''' VICTORY CUTSCENE PROCESS '''
    if game.victory_transition[0]:
        game.victory = True
        if game.victory_transition[-1]:
            SCREEN.fill((0, 0, 0))
            game.victory_transition[0] = False
            game.sound.play('victory', -1)
            game.game_state = 'victory'
            game.set_final_score()
        elif not game.victory_transition[1]:
            game.text.get_in.draw()
            game.ufo.image_mode = True
            game.ufo.can_get_in = True
            game.victory_transition[1] = game.ufo.victory_ufo(game.player_1, game.player_2)
        elif game.victory_transition[3] <= game.victory_transition[4]:
            if not game.victory_transition[2]:
                game.sound.play('escape')
                game.victory_transition[2] = True
                game.ufo.can_get_in = False

                if game.player_1: game.player_1.victory = True
                if game.player_2: game.player_2.victory = True
            game.victory_transition[3] += 1
            game.ufo.victory_ufo(game.player_1, game.player_2)
        elif game.victory_transition[5] <= game.victory_transition[6]:
            game.victory_transition[5] += 1
            game.ufo.image_mode = False

            if game.victory_transition[5] % 8 == 0 and not game.victory_transition[7]:
                SCREEN.fill(VICTORY_COLOR)
                game.victory_transition[7] = True
            elif game.victory_transition[5] % 8 == 0 and game.victory_transition[7]:
                SCREEN.fill(game.level.background_color)
                game.victory_transition[7] = False
        elif game.victory_transition[7] <= game.victory_transition[8]:
            game.victory_transition[7] += 1
            SCREEN.fill((0, 0, 0))
        else:
            SCREEN.fill((0, 0, 0))
            game.victory_transition[9] = False
            game.victory_transition[-1] = True
            UFO_SPRITE_RECT.center = (SCREEN_WIDTH / 2, 420)
            UFO_SPRITE_RECT2.center = (SCREEN_WIDTH / 2, 420 + P2_TITLE_OFFSET)

            TITLE_SPRITE_RECT.center = (SCREEN_WIDTH / 2, 440)
            WIN_SPRITE_EYES_RECT.center = TITLE_SPRITE_RECT.center
            TITLE_SPRITE_RECT2.center = (SCREEN_WIDTH / 2, 440 + P2_TITLE_OFFSET)
            WIN_SPRITE_EYES_RECT2.center = TITLE_SPRITE_RECT2.center


    ''' DEFEAT CUTSCENE PROCESS '''
    if game.defeat_transition[0]:
        if game.defeat_transition[-1]:
            game.defeat_transition[0] = False
            game.sound.play('defeat')
            game.game_state = 'defeat'
            game.set_final_score()
        elif game.defeat_transition[1] <= game.defeat_transition[2]:
            game.defeat_transition[1] += 1
            game.ufo.blink[0] = True
            if not game.defeat:
                game.defeat = True
                game.sound.play('none')
                game.sound.play_sfx('ufo_destroy')
        elif game.defeat_transition[3] <= game.defeat_transition[4]:
            game.defeat_transition[3] += 1
            game.ufo.blink[0] = False

            if game.defeat_transition[3] % 8 == 0 and not game.defeat_transition[5]:
                SCREEN.fill(DEFEAT_COLOR)
                game.defeat_transition[5] = True
            elif game.defeat_transition[3] % 8 == 0 and game.defeat_transition[5]:
                SCREEN.fill(game.level.background_color)
                game.defeat_transition[5] = False
        else:
            game.defeat_transition[5] = False
            game.defeat_transition[-1] = True


''' ============================================================= '''
''' ========= HANDLING EVERYTHING IN THE VICTORY SCREEN ========= '''
''' ============================================================= '''
def render_victory(game):
    SCREEN.fill(VICTORY_COLOR)
    game.win_stars.update(game)

    game.text.survived_text.draw()
    game.text.final_message.draw()
    game.text.final_message2.draw()

    game.text.full_score_text.rect = (265, 250)
    game.text.full_score_text.string = str("FINAL SCORE: {:07d}".format(game.full_score))
    game.text.full_score_text.draw()
    game.text.return_text.draw()

    # Draw victory stats and players
    if game.player_1:
        game.text.select_error.enabled = False
        offset1 = -100
        TITLE_SPRITE_RECT.centerx = SCREEN_WIDTH / 2 - offset1
        UFO_SPRITE_RECT.centerx = SCREEN_WIDTH / 2 - offset1
        WIN_SPRITE_EYES_RECT.centerx = (SCREEN_WIDTH / 2) - 4 - offset1

        SCREEN.blit(TITLE_SPRITE, TITLE_SPRITE_RECT)
        SCREEN.blit(WIN_SPRITE_EYES, WIN_SPRITE_EYES_RECT)
        SCREEN.blit(UFO_SPRITE, UFO_SPRITE_RECT)

        game.text.p1_points_text.string = str("PLAYER 1: {:05d}".format(game.player_1.score))
        game.text.p1_points_text.rect = (195, 300)
        game.text.p1_points_text.draw()
    if game.player_2:
        # Apply position offset
        offset2 = -300

        TITLE_SPRITE_RECT2.centerx = SCREEN_WIDTH / 2 - offset2
        UFO_SPRITE_RECT2.centerx = TITLE_SPRITE_RECT2.centerx
        WIN_SPRITE_EYES_RECT2.centerx = TITLE_SPRITE_RECT2.centerx - 4

        SCREEN.blit(TITLE_SPRITE2, TITLE_SPRITE_RECT2)
        SCREEN.blit(WIN_SPRITE_EYES2, WIN_SPRITE_EYES_RECT2)
        SCREEN.blit(UFO_SPRITE2, UFO_SPRITE_RECT2)

        game.text.p2_points_text.string = str("PLAYER 2: {:05d}".format(game.player_2.score))
        game.text.p2_points_text.rect = (200, 350)
        game.text.p2_points_text.draw()
    if game.game_tick % int(game.menu_loop[0] / 1.5) == 0:
        if game.menu_loop[1]:
            TITLE_SPRITE_RECT.y -= 15
            WIN_SPRITE_EYES_RECT.y -= 15
            UFO_SPRITE_RECT.y -= 15
            TITLE_SPRITE_RECT2.y += 15
            WIN_SPRITE_EYES_RECT2.y += 15
            UFO_SPRITE_RECT2.y += 15
            game.menu_loop[1] = False
        else:
            TITLE_SPRITE_RECT.y += 15
            WIN_SPRITE_EYES_RECT.y += 15
            UFO_SPRITE_RECT.y += 15
            TITLE_SPRITE_RECT2.y -= 15
            WIN_SPRITE_EYES_RECT2.y -= 15
            UFO_SPRITE_RECT2.y -= 15
            game.menu_loop[1] = True


''' ============================================================= '''
''' ========= HANDLING EVERYTHING IN THE DEFEAT SCREEN  ========= '''
''' ============================================================= '''
def render_defeat(game):
    SCREEN.fill(DEFEAT_COLOR)
    game.text.lost_text.draw()
    game.text.full_score_text.rect = (265, 250)
    game.text.full_score_text.string = str("FINAL SCORE: {:07d}".format(game.full_score))
    game.text.full_score_text.draw()
    game.text.return_text.draw()

    # Draw defeat stats and players
    if game.player_1:
        rect_offset = 0
        if game.player_2: rect_offset = -60

        game.player_1.defeated = True
        game.player_1.rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT - 200)
        game.player_1.draw([-4, 2], rect_offset)
    if game.player_2:
        rect_offset = 60
        game.player_2.defeated = True
        game.player_2.rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT - 200)
        game.player_2.draw([4, 2], rect_offset)

    SCREEN.blit(DEFEAT_CAGE, DEFEAT_CAGE_RECT)
