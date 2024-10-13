import random
from random import randint, choice
from components.instances.bullet import Bullet
from components.sound import Sound
from config import RANDOM_MOVE, SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN, MAX_BULLET_SPEED
import math
import pygame as pg

class Bandit:
    def __init__(self, spawn_pos, config, game):
        self.random_size = choice([50, 60, 70])
        self.item_chance = 60
        self.powerup_chance = 40
        self.base_shoot_cd = 180
        self.points_value = 20
        self.base_move_cooldown = [180, 900]
        self.name = config[0]
        self.health = 1
        self.can_shoot = True

        self.sprite = pg.image.load(f'assets/bandit_sprites/{self.name}.png').convert_alpha()
        self.sprite = pg.transform.scale(self.sprite, (self.random_size, self.random_size))
        self.rect = self.sprite.get_rect()  # Bandit size
        self.rect.x = spawn_pos[0]
        self.rect.y = spawn_pos[1]

        self.item_drop = None
        self.live_bandit = True
        self.spawnpoint = [spawn_pos[2], spawn_pos[3]]

        self.shoot_timer = 0
        self.move_timer = 0
        self.shoot_cd = randint(self.base_shoot_cd, int(self.base_shoot_cd * 2))
        self.move_cd = randint(120, 200)
        self.moving_time = randint(30, 180)
        self.direction = (choice(RANDOM_MOVE), choice(RANDOM_MOVE))
        self.in_screen = False
        self.spawn_grace = True
        self.is_moving = False
        self.last_side = [self.random_size, 0] if self.name != 'drunk_bandit' else [self.random_size - 20, 0]
        self.change_move_cd = [0, 20]

        self.lifetime = 0
        self.max_lifetime = 20

        # Values to handle exponential movement (being pushed)
        self.pushed = False
        self.push_force = []
        self.push_time = 0
        self.push_cd = 25

        ''' SPECIAL VALUES FOR DIFFERENT BANDIT TYPES'''
        # Bomb bandit values
        self.explode = [False, 0, 90, False, False, 0, 60, 20]
        self.explosion = None
        self.explosion_color = (255, 255, 255)
        self.random_near_ufo = randint(70, 180)

        # Table or shielded bandit values
        self.shield = pg.image.load(f'assets/bullet_sprites/center_table.png').convert_alpha()
        self.shield = pg.transform.scale(self.shield, (100, 100))
        self.shield = pg.transform.rotate(self.shield, -90)
        self.shield.fill((200, 150, 160), special_flags=pg.BLEND_RGBA_MULT)
        self.shield_enabled = False if self.name != 'table_bandit' else True
        self.shield_rect = self.shield.get_rect()
        self.shield_hitbox = pg.Rect(self.shield_rect.x, self.shield_rect.y, 60, 100)
        self.shield_health = 3
        self.shield_sfx_cooldown = [0, 25]

        # Drunk bandit values
        self.puddle_color = (230, 150, 90)
        self.bottle = pg.image.load(f'assets/bullet_sprites/bottle.png').convert_alpha()
        self.bottle = pg.transform.scale(self.bottle, (80, 80))
        self.bottle.fill(self.puddle_color, special_flags=pg.BLEND_RGBA_MULT)
        self.bottle_rect = self.bottle.get_rect()
        self.random_drink_time = randint(4, 7)
        self.drink_anim = [False, 0 , 120, False,  0, 60, 0, 40, 1, 120]
        self.drink_puddle = None
        self.puddle_rect = None
        self.puddle_size = [int(self.random_size * 0.3), int(self.random_size * 0.3)]

        self.bottle_enabled = False if self.name != 'drunk_bandit' else True

        # Special buff values
        self.shield_buff = pg.Surface((int(self.random_size * 1.2), int(self.random_size * 1.2)), pg.SRCALPHA)
        self.shield_buff.fill((80, 80, 255, 30))  # 128 is the alpha value (0 is fully
        self.shield_buff_enabled = False
        self.shield_buff_hp = 0

        self.get_drop()


    def get_drop(self):
        # Chance to give the bandit an item to drop at death
        if randint(1, self.item_chance) >= randint(1, 100):
            powerup_chance = randint(1, self.powerup_chance)

            if powerup_chance < randint(1, 100):
                self.item_drop = 'brick'
            else:
                # Getting random collectible item using name in
                # item sprites folder, not including .png
                self.item_drop = random.choice([
                    'shoot_pu', 'bullet_pu',
                    'brick_pu', 'shield_pu'
                ])

    def move_bandit(self, ufo):
        if self.lifetime > self.max_lifetime:
            top_distance = [[0, -3], 0 + self.rect.y]
            bottom_distance = [[0, 3], SCREEN_HEIGHT - self.rect.y]
            left_distance = [[-3, 0], 0 + self.rect.x]
            right_distance = [[3, 0], SCREEN_WIDTH - self.rect.x]
            smallest_x = min(left_distance[1], right_distance[1])
            smallest_y = min(top_distance[1], bottom_distance[1])

            if smallest_x < smallest_y:
                side_goal = left_distance if smallest_x == left_distance[1] else right_distance
            else:
                side_goal = top_distance if smallest_y == top_distance[1] else bottom_distance

            self.rect.x += side_goal[0][0]
            self.rect.y += side_goal[0][1]
        elif self.live_bandit and self.is_moving and not self.pushed:
            if self.name != 'bomb_bandit':
                new_x = self.rect.x + self.direction[0] * 2
                new_y = self.rect.y + self.direction[1] * 2
                self.change_move_cd[0] += 1

                # verify the limits of the screen
                if new_x < 20 or new_x + self.rect.width > SCREEN_WIDTH - 20\
                    and self.change_move_cd[0] >= self.change_move_cd[1]:
                    self.change_move_cd[0] = 0
                    self.direction = (-self.direction[0], self.direction[1])
                if new_y < 20 or new_y + self.rect.height > SCREEN_HEIGHT - 20\
                    and self.change_move_cd[0] >= self.change_move_cd[1]:
                    self.change_move_cd[0] = 0
                    self.direction = (self.direction[0], -self.direction[1])

                self.rect.x += self.direction[0] * 2
                self.rect.y += self.direction[1] * 2
            else:
                direction_x = ufo.rect.centerx - self.rect.centerx
                direction_y = ufo.rect.centery - self.rect.centery
                magnitude = math.sqrt(direction_x ** 2 + direction_y ** 2)

                if magnitude >= self.random_near_ufo:
                    self.rect.x += direction_x / magnitude * 4
                    self.rect.y += direction_y / magnitude * 4

    def update(self, game, target_position):
        self.shoot_timer += 1

        # Detect if offscreen and kill instantly
        if self.live_bandit and self.lifetime > 1:
            offscreen = ((self.rect.x < 0 or self.rect.x > SCREEN_WIDTH)
                         or (self.rect.y < 0 or self.rect.y > SCREEN_HEIGHT))

            if offscreen:
                self.live_bandit = False

        # Initial movement to appear on screen
        if self.lifetime <= 2 and not self.pushed and self.spawn_grace:
            self.rect.x += (self.spawnpoint[0] - self.rect.x) * 0.05
            self.rect.y += (self.spawnpoint[1] - self.rect.y) * 0.05
        else:
            self.spawn_grace = False

        # move each 5 secs
        if self.move_timer >= self.move_cd:
            self.is_moving = True
            self.move_cd = randint(self.base_move_cooldown[0], self.base_move_cooldown[1])
            self.moving_time = randint(30, 180)
            self.direction = (choice(RANDOM_MOVE), choice(RANDOM_MOVE))
            self.move_timer = 0

        if (self.move_timer <= self.moving_time and not self.drink_anim[0]
                and self.is_moving and not self.pushed) or self.lifetime > self.max_lifetime:

            if self.lifetime > self.max_lifetime and self.drink_anim[0]:
                self.live_bandit = False
                return
            self.move_bandit(game.ufo)
        elif self.is_moving:
            self.is_moving = False

        self.shoot_timer += 1
        self.move_timer += 1
        self.push_check()
        self.bomb_bandit_check(game)

        # Handling shield system for bandit
        if self.shield_enabled:
            self.shield_sfx_cooldown[0] += 1

            # Choosing the side position and rotation depending on left or right on screen
            left_distance = [[self.random_size, 0], -180, 0 + self.rect.x]
            right_distance = [[-self.random_size, 0], 180, SCREEN_WIDTH - self.rect.x]
            smallest_x = min(left_distance[2], right_distance[2])

            side_goal = left_distance if smallest_x == left_distance[2] else right_distance

            if self.last_side != side_goal[0]:
                self.shield = pg.transform.rotate(self.shield, side_goal[1])

            # Updating position relative to bandit
            self.shield_rect.center = self.rect.center
            self.shield_rect.x += side_goal[0][0]
            self.shield_rect.y += side_goal[0][1]
            self.shield_hitbox.center = self.shield_rect.center
            self.last_side = side_goal[0]

            if self.shield_health <= 0 and self.shield_enabled:
                self.shield_enabled = False
                if self.name == 'table_bandit' and self.points_value != 50:
                    self.base_shoot_cd = 180
                    self.points_value = 50
                    self.base_move_cooldown = [180, 900]

        # Handling totally legal and PG friendly drink bottle system for bandit
        if self.bottle_enabled:
            # Choosing the side position and flipping bottle depending on position
            left_distance = [[self.random_size - 20, 0], 0 + self.rect.x, -90]
            right_distance = [[-self.random_size + 20, 0], SCREEN_WIDTH - self.rect.x, 90]
            smallest_x = min(left_distance[1], right_distance[1])

            side_goal = left_distance if smallest_x == left_distance[1] else right_distance

            if self.last_side != side_goal[0]:
                self.bottle = pg.transform.flip(self.bottle, True, False)

            self.bottle_rect.center = self.rect.center
            self.bottle_rect.x += side_goal[0][0]
            self.bottle_rect.y += side_goal[0][1]
            self.last_side = side_goal[0]

            # Drink puddle animation and spawning process
            if self.lifetime > self.random_drink_time:
                if not self.drink_anim[0]:
                    self.bottle = pg.transform.rotate(self.bottle, side_goal[-1])
                    self.drink_anim[0] = True
                elif self.drink_anim[1] < self.drink_anim[2]:
                    self.drink_anim[1] += 1
                elif self.drink_anim[4] == 0:
                    self.bottle = pg.transform.rotate(self.bottle, -side_goal[-1])
                    self.drink_anim[4] += 1
                elif self.drink_anim[4] < self.drink_anim[5]:
                    self.drink_anim[4] += 1
                elif not self.drink_anim[3]:
                    self.sprite = pg.transform.rotate(self.sprite, -side_goal[-1])
                    self.drink_anim[3] = True
                elif self.drink_anim[6] < self.drink_anim[7]:
                    self.drink_anim[6] += 1
                elif self.drink_anim[8] < self.drink_anim[9]:
                    self.drink_anim[8] += 1

                if self.drink_anim[8] % 30 == 0 and self.drink_anim[8] < self.drink_anim[9]:
                    # Creating a toxic puddle to trouble player
                    self.drink_puddle = pg.image.load(f'assets/bullet_sprites/puddle.png').convert_alpha()
                    self.drink_puddle.fill(self.puddle_color, special_flags=pg.BLEND_RGBA_MULT)
                    self.drink_puddle.set_alpha(160)
                    self.drink_puddle = pg.transform.scale(self.drink_puddle,
                                        (self.puddle_size[0], self.puddle_size[1]))
                    self.puddle_rect = self.drink_puddle.get_rect()
                    self.puddle_rect.center = self.rect.center

                    # Increasing the size of the puddle every frame until reaches max
                    self.puddle_size[0] += randint(40, 100)
                    self.puddle_size[1] += randint(40, 80)

        # Updating shooting system
        if self.shoot_timer >= self.shoot_cd:
            self.shoot_cd = randint(self.base_shoot_cd, int(self.base_shoot_cd * 2))
            self.shoot(game, target_position)
            self.shoot_timer = 0

    def shoot(self, game, target_position):
        direction_x = target_position[0] - self.rect.centerx
        direction_y = target_position[1] - self.rect.centery
        magnitude = math.sqrt(direction_x ** 2 + direction_y ** 2)

        if magnitude != 0 and self.can_shoot:
            # Applying various different reactions depending on which bandit is shooting
            if self.name != 'bandit_hitman':
                direction = (direction_x / magnitude * 3, direction_y / magnitude * 3)
            else:
                direction = (direction_x / magnitude * 6, direction_y / magnitude * 6)
            bullet_position = (self.rect.centerx, self.rect.centery)

            if self.name == 'cards_bandit':
                # Choosing various different cards and effects for this bandit
                # Their buff functionalities are on "update_bullets"
                card_type = choice([
                    ['shield', (100, 100 ,255)],
                    ['wild', (255, 200, 100)],
                    ['evil', (255, 50, 50)],
                    ['lucky', (50, 255, 50)],
                ])

                if card_type[0] == 'shield':
                    shots = 3

                    for new_bullet in range(shots):
                        shot_offset_x = randint(2, 5)
                        shot_offset_y = randint(2, 5)
                        if randint(1, 2) == 1: shot_offset_x *= -1
                        if randint(1, 2) == 1: shot_offset_y *= -1

                        direction_x = target_position[0] - self.rect.centerx
                        direction_y = target_position[1] - self.rect.centery
                        direction = (direction_x / magnitude * shot_offset_x, direction_y / magnitude * shot_offset_y)

                        bullet = Bullet('card', bullet_position, direction, 14, card_type[1])
                        bullet.random_buff = card_type[0]
                        game.bullets.append(bullet)
                elif card_type[0] == 'wild':
                    bullet = Bullet('card', bullet_position, direction, 14, card_type[1])
                    bullet.wild_mode = True
                    bullet.max_lifetime = 4
                    game.bullets.append(bullet)
                elif card_type[0] == 'evil':
                    bullet = Bullet('card', bullet_position, direction, 20, card_type[1])
                    bullet.random_buff = card_type[0]
                    game.bullets.append(bullet)
                elif card_type[0] == 'lucky':
                    bullet = Bullet('card', bullet_position, direction, 14, card_type[1])
                    bullet.random_buff = card_type[0]
                    game.bullets.append(bullet)
            else:
                bullet = Bullet('bullet', bullet_position, direction, 8)
                game.bullets.append(bullet)

            game.sound.play_sfx('bandit_shoot')

    # Function to handle the entire process of bandit causing explosion
    def bomb_bandit_check(self, game):
        if self.name == 'bomb_bandit':
            self.explode[1] += 1

            if 6 <= self.lifetime < 8:
                if not self.explode[4]:
                    self.explode[4] = True
                    self.sprite.fill((255, 60, 15), special_flags=pg.BLEND_RGBA_MULT)

                if self.explode[1] >= 8 and self.explode[3]:
                    self.explode[1] = 0
                    self.explode[3] = False
                elif self.explode[1] >= 8 and not self.explode[3]:
                    self.explode[1] = 0
                    self.explode[3] = True
            elif self.lifetime >= 8:    # Creating the explosion
                if not self.explode[0]:
                    self.explode[1] = 0
                    self.explode[0] = True
                    game.sound.play_sfx('explode')
                    self.explosion = pg.Rect(self.rect.x, self.rect.y,
                                        self.random_size * 2,
                                        self.random_size * 2)
                    self.explosion.center = self.rect.center

                self.explode[1] += 1
                self.explode[5] += 1

                # Changing colors for explosion effect
                if self.explode[5] >= 8 and self.explosion_color != (255, 130, 0):
                    self.explode[5] = 0
                    self.explosion_color = (255, 130, 0)
                elif self.explode[5] >= 8 and self.explosion_color != (255, 240, 0):
                    self.explode[5] = 0
                    self.explosion_color = (255, 240, 0)

                if self.explode[1] >= self.explode[6]:
                    self.live_bandit = False

    def update_bullets(self, game):
        if self.drink_anim[3]: return

        for bullet in game.bullets:
            # Verify bullet collision with bandit
            if self.live_bandit and bullet.reflect and bullet.rect.colliderect(self.rect)\
                and (self.name == 'cards_bandit' or bullet.name != 'card'):
                game.sound.play_sfx('bandit_damage')

                if self.shield_buff_hp >= 1:
                    self.shield_buff_hp -= 1
                    self.shield_buff.set_alpha(self.shield_buff_hp * 30)
                    game.bullets.remove(bullet)
                    continue
                elif self.health > 1:
                    self.health -= 1
                    game.bullets.remove(bullet)
                    continue

                self.live_bandit = False
                game.bullets.remove(bullet)

                if bullet.player_owned[0]:
                    bullet.player_owned[1].score += self.points_value
                    return self.item_drop

                break

            # Verify bullet collision with bandit shield
            if bullet.rect.colliderect(self.shield_hitbox) and self.shield_enabled and bullet.reflect:
                # Get the relative position of the collision
                self.shield_health -= 1
                self.shield.fill((220, 200, 200), special_flags=pg.BLEND_RGBA_MULT)

                relative_collision_x = (bullet.rect.centerx - self.shield_hitbox.left) / self.shield_hitbox.width
                offset = (relative_collision_x - 0.5) * 2

                # Adjust direction depending on bullet movement
                bullet.speed_x = offset * MAX_BULLET_SPEED

                # Invert bullet direction
                bullet.speed_y *= -1

                # Convert bullet's ownership to the bandit
                if bullet.name == 'bullet': bullet.sprite.fill(bullet.base_color)
                bullet.can_hit = True
                bullet.player_owned[0] = False
                bullet.player_owned[1] = None
                bullet.reflect = False

                if self.shield_sfx_cooldown[0] >= self.shield_sfx_cooldown[1]:
                    game.sound.play_sfx('bounce')
                    self.shield_sfx_cooldown[0] = 0

                if self.shield_health <= 0:
                    game.sound.play_sfx('bandit_damage')

            # Verify buff collision with bandit
            if (self.live_bandit and bullet.rect.colliderect(self.rect) and self.name != 'cards_bandit'
                and bullet.name == 'card' and bullet.random_buff and bullet.tick >= 20):
                    if bullet.random_buff == 'shield':
                        self.shield_buff_hp += 1
                        self.shield_buff_enabled = True
                        self.shield_buff.set_alpha(self.shield_buff_hp * 100)
                    if bullet.random_buff == 'evil':
                        self.base_shoot_cd = int(self.base_shoot_cd * 0.5)
                        self.base_move_cooldown[0] = int(self.base_move_cooldown[0] * 0.5)
                        self.base_move_cooldown[1] = int(self.base_move_cooldown[1] * 0.5)
                        if self.base_shoot_cd < 30: self.base_shoot_cd = 30
                        self.sprite.fill((255, 160, 120), special_flags=pg.BLEND_RGBA_MULT)
                    if bullet.random_buff == 'lucky':
                        self.item_chance *= 3
                        self.powerup_chance *= 2
                        self.get_drop()
                        self.sprite.fill((200, 255, 200), special_flags=pg.BLEND_RGBA_MULT)

                    game.bullets.remove(bullet)
                    game.sound.play_sfx('random_buff')

    # System for pushing exponentially, used to push bandits with the player's shield
    def push_check(self):
        if self.pushed and self.push_time < self.push_cd:
            self.push_time += 1
            self.push_force[0] *= 0.9
            self.push_force[1] *= 0.9

            self.rect.x += self.push_force[0]
            self.rect.y += self.push_force[1]
        elif self.pushed:
            self.push_time = 0
            self.pushed = False

    def shield_collide_check(self, game, player):
        if not player or self.drink_anim[3]:
            return

        # Check if the player's shield is being hit
        shield_rect = player.shield_rect

        if self.rect.colliderect(shield_rect) and player.shield_enabled and not self.pushed\
            and not self.name == 'bandit_hitman':
            # Changed relative position calculation to handle 2 vectors
            relative_collision = self.rect.clip(shield_rect).center
            offset_vector = pg.math.Vector2(self.rect.center) - pg.math.Vector2(relative_collision)
            game.sound.play_sfx('bandit_push')

            # This function just make the vector values in unit (-1 to 1)
            if offset_vector.length() != 0:
                offset_vector.normalize_ip()
            force_x = offset_vector.x * player.push_power
            force_y = offset_vector.y * player.push_power

            # Add pushing values
            self.push_force = [force_x, force_y]
            self.pushed = True

            if self.lifetime < 2: self.lifetime = 2

    def draw(self):
        if self.drink_puddle:
            SCREEN.blit(self.drink_puddle, self.puddle_rect)
        if not self.explode[3]:
            SCREEN.blit(self.sprite, self.rect)

        if self.explosion:
            pg.draw.rect(SCREEN, self.explosion_color, self.explosion)

        if self.shield_enabled:
            SCREEN.blit(self.shield, self.shield_rect)

        if self.bottle_enabled and not self.drink_anim[3]:
            SCREEN.blit(self.bottle, self.bottle_rect)

        if self.shield_buff_enabled:
            SCREEN.blit(self.shield_buff, (self.rect.centerx - int(self.random_size / 1.65),
                                           self.rect.centery - int(self.random_size / 1.65)))


