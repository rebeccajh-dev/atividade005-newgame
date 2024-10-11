from random import randint, choice

from config import SCREEN_WIDTH, COLOR_WHITE, COLOR_RED, SCREEN_HEIGHT, FRAMERATE, PLAYER_COLORS, MENU_COLOR, SCREEN, \
    BACKGROUND_COLOR, AMBUSH_FILTER, VICTORY_COLOR, DEFEAT_COLOR, P2_TITLE_OFFSET

from components.instances.bandit import Bandit
from components.instances.objects import Objects

import pygame as pg

''' Separately updating physics based stuff like position or states, 
    hoping to make the process of drawing faster and less cluttered.
'''

# Function for spawning bandits
def bandit_position(game, number_spawned):
    bandit_spawnrate = int(game.base_bandit_spawnrate - (15 * game.player_count))

    if (game.game_tick % bandit_spawnrate == 0
        and game.bandit_count < game.max_bandits):  # add bandits each 300 ticks
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

            bandit = Bandit(start_pos, game.ambush_mode)
            game.bandits.append(bandit)


def update_physics(game):
    # Creating bandits
    if not game.ambush_mode:
        number_spawned = randint(1, game.max_spawned)
        game.max_bandits = game.base_max_bandits + (game.bandit_spawn_multi[0] * game.player_count)
    else:
        number_spawned = randint(0, game.max_spawned + game.player_count)
        game.max_bandits = game.base_max_bandits + (game.bandit_spawn_multi[1] * game.player_count)

    if game.can_spawn_bandits:
        bandit_position(game, number_spawned)
    game.bandit_count = len(game.bandits)

    if game.game_tick % FRAMERATE == 0:
        game.game_timer += 1

    # increasing difficulty every 15 seconds
    if (game.game_tick % (FRAMERATE * game.difficulty_time) == 0
            and game.base_bandit_spawnrate > 60):
        game.base_bandit_spawnrate -= 15
        if game.base_bandit_spawnrate < 60: game.base_bandit_spawnrate = 60

    for item in game.objects:
        if not item.collected and item.lifetime <= item.despawn_time:
            item.update()
            item.check_collect(game.player_1, game.ufo)
            item.check_collect(game.player_2, game.ufo)

            if game.game_tick % FRAMERATE == 0:
                item.lifetime += 1
        else:
            game.objects.remove(item)


    # Updating bandits
    if not game.victory_transition[0] and not game.defeat_transition[0]:
        for bandit in game.bandits:
            if bandit.live_bandit:
                # Getting a random brick as a target
                # Allowing broken bricks is by design, or else it would be too unfair
                if bandit.name != 'bandit_hitman':
                    target = game.ufo.ufos[randint(0, len(game.ufo.ufos) - 1)][0].topleft
                else:
                    if randint(1, 2) == 1 and game.player_1:
                        target = game.player_1.rect.topleft
                    elif game.player_2:
                        target = game.player_2.rect.topleft
                    else:
                        target = game.player_1.rect.topleft

                # Applhying chance to spawn loot on death
                bandit.update(target, game.bullets, game.ufo)
                possible_loot = bandit.update_bullets(game.bullets)

                if possible_loot:
                    new_item = Objects(possible_loot, bandit.rect)
                    game.objects.append(new_item)

                # Checking various collisions with the bandit explosion
                if bandit.explosion and bandit.explode[1] <= bandit.explode[7]:
                    game.ufo.explosion_collide_check(bandit.explosion)
                    if game.player_1: game.player_1.explosion_collide_check(bandit.explosion)
                    if game.player_2: game.player_1.explosion_collide_check(bandit.explosion)

                bandit.shield_collide_check(game.player_1)
                bandit.shield_collide_check(game.player_2)
            else:
                game.bandits.remove(bandit)

            if game.game_tick % FRAMERATE == 0:
                bandit.lifetime += 1
    else:
        game.bandits = []

    # collision of bullets w ufo
    for bullet in game.bullets:
        if bullet.is_alive:
            bullet.update()
            bullet.shield_collide_check(game.player_1)  # collision w shield player 1
            bullet.player_collide_check(game.player_1)
            bullet.player_collide_check(game.player_2)
            bullet.shield_collide_check(game.player_2)
            if game.game_tick % FRAMERATE == 0:
                bullet.lifetime += 1

            game.ufo.ufo_collide_check(bullet)
        else:
            game.bullets.remove(bullet)