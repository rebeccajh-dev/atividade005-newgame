import random
from random import randint, choice
from components.bullet import Bullet
from config import RANDOM_MOVE, SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN
import math
import pygame as pg



class Bandit:
    def __init__(self, spawn_pos):
        random_size = choice([50, 60, 70])

        self.name = 'BANDIT'
        self.sprite = pg.image.load(f'assets/bandit_sprites/bandit1.png')
        self.sprite = pg.transform.scale(self.sprite, (random_size, random_size))
        self.rect = self.sprite.get_rect()  # Bandit size
        self.rect.x = spawn_pos[0]
        self.rect.y = spawn_pos[1]

        self.item_drop = None
        self.live_bandit = True
        self.spawnpoint = [spawn_pos[2], spawn_pos[3]]
        self.item_chance = 50
        self.powerup_chance = 50

        self.shoot_timer = 0
        self.move_timer = 0
        self.base_shoot_cd = 180
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


    def move_bandit(self):
        if self.lifetime > self.max_lifetime:
            top_distance = [[0, 2], 0 + self.rect.y]
            bottom_distance = [[0, -2], SCREEN_HEIGHT - self.rect.y]
            left_distance = [[-2, 0], 0 + self.rect.x]
            right_distance = [[2, 0], SCREEN_WIDTH - self.rect.x]
            largest = max(top_distance[1], bottom_distance[1], left_distance[1], right_distance[1])
            side_goal = []

            if largest == top_distance[1]: side_goal = top_distance
            if largest == bottom_distance[1]: side_goal = bottom_distance
            if largest == left_distance[1]: side_goal = left_distance
            if largest == right_distance[1]: side_goal = right_distance

            self.rect.x += side_goal[0][0]
            self.rect.y += side_goal[0][1]
            return

        if self.live_bandit and self.is_moving and not self.pushed:
            new_x = self.rect.x + self.direction[0] * 2
            new_y = self.rect.y + self.direction[1] * 2

            # verify the limits of the screen
            if new_x < 20 or new_x + self.rect.width > SCREEN_WIDTH - 20:
                self.direction = (-self.direction[0], self.direction[1])
            if new_y < 20 or new_y + self.rect.height > SCREEN_HEIGHT - 20:
                self.direction = (self.direction[0], -self.direction[1])

            self.rect.x += self.direction[0] * 2
            self.rect.y += self.direction[1] * 2

    def update(self, target_position, bullets_list):
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
            self.move_cd = randint(180, 900)
            self.moving_time = randint(30, 180)
            self.direction = (choice(RANDOM_MOVE), choice(RANDOM_MOVE))
            self.move_timer = 0

        if (self.move_timer <= self.moving_time
                and self.is_moving and not self.pushed):
            self.move_bandit()
        elif self.is_moving:
            self.is_moving = False

        self.shoot_timer += 1
        self.move_timer += 1
        self.push_check()

        if self.shoot_timer >= self.shoot_cd:
            self.shoot_cd = randint(self.base_shoot_cd, int(self.base_shoot_cd * 2))
            self.shoot(target_position, bullets_list)
            self.shoot_timer = 0

    def shoot(self, target_position, bullets_list):
        direction_x = target_position[0] - self.rect.centerx
        direction_y = target_position[1] - self.rect.centery
        magnitude = math.sqrt(direction_x ** 2 + direction_y ** 2)

        if magnitude != 0:
            direction = (direction_x / magnitude * 3, direction_y / magnitude * 3)
            bullet_position = (self.rect.centerx, self.rect.centery)
            bullet = Bullet(bullet_position, direction)
            bullets_list.append(bullet)

    def update_bullets(self, bullets_list):
        for bullet in bullets_list:

            # Verify the collision w bandit
            if self.live_bandit and bullet.reflect and bullet.rect.colliderect(self.rect):
                self.live_bandit = False
                bullet.is_alive = False
                if bullet.player_owned[0]:
                    bullet.player_owned[1].score += 20
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

        if self.rect.colliderect(shield_rect) and player.shield_enabled and not self.pushed:
            # Changed relative position calculation to handle 2 vectors
            relative_collision = self.rect.clip(shield_rect).center
            offset_vector = pg.math.Vector2(self.rect.center) - pg.math.Vector2(relative_collision)

            # This function just make the vector values in unit (-1 to 1)
            if offset_vector.length() != 0:
                offset_vector.normalize_ip()
            force_x = offset_vector.x * player.push_power
            force_y = offset_vector.y * player.push_power

            # Add pushing values
            self.push_force = [force_x, force_y]
            self.pushed = True
            self.lifetime = 2

    def draw_bandit(self):
        SCREEN.blit(self.sprite, self.rect)
