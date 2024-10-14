from random import randint, choice, choices

from config import SCREEN_WIDTH, COLOR_WHITE, COLOR_RED, SCREEN_HEIGHT, FRAMERATE, PLAYER_COLORS, MENU_COLOR, SCREEN, \
    AMBUSH_FILTER, VICTORY_COLOR, DEFEAT_COLOR, P2_TITLE_OFFSET

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

            # Get a random bandit to spawn depending on chance
            spawns = []
            chances = []

            for bandit_type in game.level.spawn_types:
                if not bandit_type[2]:
                    spawns.append(bandit_type)
                    if not game.ambush_mode:
                        chances.append(bandit_type[1])
                    else:
                        chances.append(bandit_type[1] + bandit_type[3])
                elif bandit_type[2] and game.ambush_mode:
                    spawns.append(bandit_type)
                    chances.append(bandit_type[1])

            choosen_bandit = choices(population=spawns, weights=chances)[0]

            bandit = Bandit(start_pos, choosen_bandit, game)

            # Preset of certain bandit values to change
            if bandit.name == 'bomb_bandit':
                bandit.can_shoot = False
                bandit.item_chance = 150
                bandit.powerup_chance = 40
                bandit.points_value = 80
                bandit.base_move_cooldown = [10, 60]
            elif bandit.name == 'bandit_hitman':
                bandit.base_shoot_cd = 240
                bandit.item_chance = 80
                bandit.powerup_chance = 70
                bandit.points_value = 50
                bandit.base_move_cooldown = [90, 300]
            elif bandit.name == 'skilled_bandit':
                bandit.base_shoot_cd = 120
                bandit.item_chance = 70
                bandit.powerup_chance = 60
                bandit.points_value = 40
                bandit.base_move_cooldown = [120, 700]
            elif bandit.name == 'table_bandit':
                bandit.base_shoot_cd = 400
                bandit.points_value = 200
                bandit.base_move_cooldown = [500, 1200]
            elif bandit.name == 'cards_bandit':
                bandit.base_shoot_cd = 200
                bandit.item_chance = 40
                bandit.powerup_chance = 90
                bandit.points_value = 80
                bandit.base_move_cooldown = [100, 500]
            elif bandit.name == 'drunk_bandit':
                bandit.can_shoot = False
                bandit.points_value = 50
                bandit.base_move_cooldown = [60, 180]

            game.bandits.append(bandit)


def update_physics(game):
    if game.defeat or game.victory_transition[0]:
        game.bandits = []
        game.bullets = []
        game.objects = []
        game.can_spawn_bandits = False

    # Creating bandits
    if not game.ambush_mode:
        number_spawned = randint(1, game.max_spawned)
        game.max_bandits = game.base_max_bandits + (game.bandit_spawn_multi[0] * game.player_count) + game.max_increase
    else:
        number_spawned = randint(0, game.max_spawned + game.player_count)
        game.max_bandits = game.base_max_bandits + (game.bandit_spawn_multi[1] * game.player_count) + game.max_increase

    if game.can_spawn_bandits:
        bandit_position(game, number_spawned)
    game.bandit_count = len(game.bandits)

    if game.game_tick % FRAMERATE == 0 and not game.defeat:
        game.game_timer += 1

    # increasing difficulty every 15 seconds
    if (game.game_tick % (FRAMERATE * game.difficulty_time) == 0
            and game.base_bandit_spawnrate > 60):
        game.base_bandit_spawnrate -= 15
        if game.base_bandit_spawnrate < 60: game.base_bandit_spawnrate = 60
    '''if game.game_tick % (FRAMERATE * game.difficulty_time * 4) == 0:
        game.max_increase += 1
    '''

    for item in game.objects:
        if not item.collected and item.lifetime <= item.despawn_time:
            item.update()
            item.check_collect(game, game.player_1)
            item.check_collect(game, game.player_2)

            if game.game_tick % FRAMERATE == 0:
                item.lifetime += 1
        else:
            game.objects.remove(item)

    # Updating bandits
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
                    target = game.ufo.ufos[randint(0, len(game.ufo.ufos) - 1)][0].topleft

            # Applhying chance to spawn loot on death
            bandit.update(game, target)
            possible_loot = bandit.update_bullets(game)

            if possible_loot:
                new_item = Objects(possible_loot, bandit.rect)
                game.objects.append(new_item)

            # Checking various collisions with the bandit explosion
            if bandit.explosion and bandit.explode[1] <= bandit.explode[7]:
                game.ufo.explosion_collide_check(game, bandit.explosion)
                if game.player_1: game.player_1.damage_collide_check(game, bandit.explosion)
                if game.player_2: game.player_1.damage_collide_check(game, bandit.explosion)

            if bandit.puddle_rect:
                if game.player_1: game.player_1.damage_collide_check(game, bandit.puddle_rect)
                if game.player_2: game.player_1.damage_collide_check(game, bandit.puddle_rect)

            bandit.shield_collide_check(game, game.player_1)
            bandit.shield_collide_check(game, game.player_2)
        else:
            game.bandits.remove(bandit)

        if game.game_tick % FRAMERATE == 0:
            bandit.lifetime += 1

    # collision of bullet_sprites w ufo
    for bullet in game.bullets:
        if bullet.is_alive and bullet.lifetime <= bullet.max_lifetime:
            bullet.update(game)
            bullet.shield_collide_check(game, game.player_1)  # collision w shield player 1
            bullet.player_collide_check(game, game.player_1)
            bullet.player_collide_check(game, game.player_2)
            bullet.shield_collide_check(game, game.player_2)
            if game.game_tick % FRAMERATE == 0:
                bullet.lifetime += 1

            game.ufo.ufo_collide_check(game, bullet)
        else:
            game.bullets.remove(bullet)