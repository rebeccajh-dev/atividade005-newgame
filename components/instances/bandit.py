import random
from random import randint, choice
from components.instances.bullet import Bullet
from components.sound import Sound
from config import RANDOM_MOVE, SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN
import math
import pygame as pg



class Bandit:
    def __init__(self, spawn_pos, ambush):
        self.random_size = choice([50, 60, 70])
        self.item_chance = 60
        self.powerup_chance = 50
        self.base_shoot_cd = 180
        self.points_value = 20
        self.base_move_cooldown = [180, 900]

        if ambush:
            self.bandit_chance = randint(1, 120)
        else:
            self.bandit_chance = randint(1, 90)

        if self.bandit_chance >= 110:
            self.name = 'bomb_bandit'
            self.item_chance = 150
            self.powerup_chance = 40
            self.points_value = 100
            self.base_move_cooldown = [10, 60]
        elif self.bandit_chance >= 100:
            self.name = 'bandit_hitman'
            self.base_shoot_cd = 240
            self.item_chance = 80
            self.powerup_chance = 70
            self.points_value = 40
            self.base_move_cooldown = [90, 300]
        elif self.bandit_chance >= 80:
            self.name = 'skilled_bandit'
            self.base_shoot_cd = 120
            self.item_chance = 70
            self.powerup_chance = 60
            self.points_value = 40
            self.base_move_cooldown = [120, 700]
        else:
            self.name = 'basic_bandit'
            self.powerup_chance = 40

        self.sprite = pg.image.load(f'assets/bandit_sprites/{self.name}.png').convert_alpha()
        self.sprite = pg.transform.scale(self.sprite, (self.random_size, self.random_size))
        self.rect = self.sprite.get_rect()  # Bandit size
        self.rect.x = spawn_pos[0]
        self.rect.y = spawn_pos[1]
        self.sound = Sound()

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

        self.lifetime = 0
        self.max_lifetime = 20

        # Values to handle exponential movement (being pushed)
        self.pushed = False
        self.push_force = []
        self.push_time = 0
        self.push_cd = 25

        # Values for other bandit types
        self.explode = [False, 0, 90, False, False, 0, 60, 5]
        self.explosion = None
        self.explosion_color = (255, 255, 255)
        self.random_near_ufo = randint(70, 180)

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
            side_goal = []

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

                # verify the limits of the screen
                if new_x < 20 or new_x + self.rect.width > SCREEN_WIDTH - 20:
                    self.direction = (-self.direction[0], self.direction[1])
                if new_y < 20 or new_y + self.rect.height > SCREEN_HEIGHT - 20:
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

    def update(self, target_position, bullets_list, ufo):
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

        if (self.move_timer <= self.moving_time
                and self.is_moving and not self.pushed) or self.lifetime > self.max_lifetime:
            self.move_bandit(ufo)
        elif self.is_moving:
            self.is_moving = False

        self.shoot_timer += 1
        self.move_timer += 1
        self.push_check()
        self.bomb_bandit_check(ufo)

        if self.shoot_timer >= self.shoot_cd:
            self.shoot_cd = randint(self.base_shoot_cd, int(self.base_shoot_cd * 2))
            self.shoot(target_position, bullets_list)
            self.shoot_timer = 0

    def shoot(self, target_position, bullets_list):
        direction_x = target_position[0] - self.rect.centerx
        direction_y = target_position[1] - self.rect.centery
        magnitude = math.sqrt(direction_x ** 2 + direction_y ** 2)

        if magnitude != 0 and self.name != 'bomb_bandit':
            if self.name != 'bandit_hitman':
                direction = (direction_x / magnitude * 3, direction_y / magnitude * 3)
            else:
                direction = (direction_x / magnitude * 6, direction_y / magnitude * 6)
            bullet_position = (self.rect.centerx, self.rect.centery)
            bullet = Bullet(bullet_position, direction)
            bullets_list.append(bullet)
            self.sound.play_sfx('bandit_shoot')

    def bomb_bandit_check(self, ufo):
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
            elif self.lifetime >= 8:
                if not self.explode[0]:
                    self.explode[1] = 0
                    self.explode[0] = True
                    self.sound.play_sfx('explode')
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


    def update_bullets(self, bullets_list):
        for bullet in bullets_list:

            # Verify the collision w bandit
            if self.live_bandit and bullet.reflect and bullet.rect.colliderect(self.rect):
                self.live_bandit = False
                bullet.is_alive = False
                self.sound.play_sfx('bandit_damage')

                if bullet.player_owned[0]:
                    bullet.player_owned[1].score += self.points_value
                    return self.item_drop

                bullets_list.remove(bullet)
                break

            if not bullet.is_alive:
                bullets_list.remove(bullet)


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

    def shield_collide_check(self, player):
        if not player:
            return

        # Check if the player's shield is being hit
        shield_rect = player.shield_rect

        if self.rect.colliderect(shield_rect) and player.shield_enabled and not self.pushed\
            and not self.name == 'bandit_hitman':
            # Changed relative position calculation to handle 2 vectors
            relative_collision = self.rect.clip(shield_rect).center
            offset_vector = pg.math.Vector2(self.rect.center) - pg.math.Vector2(relative_collision)
            self.sound.play_sfx('bandit_push')

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
        if not self.explode[3]:
            SCREEN.blit(self.sprite, self.rect)

        if self.explosion:
            pg.draw.rect(SCREEN, self.explosion_color, self.explosion)
