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

        self.live_bandit = True
        self.bullets = []
        self.spawnpoint = [spawn_pos[2], spawn_pos[3]]

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
        self.max_lifetime = 10

        # Values to handle exponential movement (being pushed)
        self.pushed = False
        self.push_force = []
        self.push_time = 0
        self.push_cd = 25

    def move_bandit(self):
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

    def update(self, target_position):
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
            self.shoot(target_position)
            self.shoot_timer = 0

    def shoot(self, target_position):
        direction_x = target_position[0] - self.rect.centerx
        direction_y = target_position[1] - self.rect.centery
        magnitude = math.sqrt(direction_x ** 2 + direction_y ** 2)

        if magnitude != 0:
            direction = (direction_x / magnitude * 3, direction_y / magnitude * 3)
            bullet_position = (self.rect.centerx, self.rect.centery)
            bullet = Bullet(bullet_position, direction)
            self.bullets.append(bullet)

    def update_bullets(self):
        bullets_to_remove = []
        for bullet in self.bullets:
            bullet.update()

            # Verify the collision w bandit
            if self.live_bandit and bullet.reflect and bullet.rect.colliderect(self.rect):
                self.live_bandit = False
                bullet.is_alive = False
                if bullet.player_owned[0]:
                    bullet.player_owned[1].score += 20

                bullets_to_remove.append(bullet)
                break

            if not bullet.is_alive:
                bullets_to_remove.append(bullet)

        for bullet in bullets_to_remove:
            if bullet in self.bullets:
                self.bullets.remove(bullet)

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
