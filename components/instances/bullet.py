"""
Class for spawning bullet_sprites and handling their behaviour,
they have a position to be spawned at and a direction to constantly go.
"""
from config import SCREEN, MAX_BULLET_SPEED
import pygame as pg
from random import randint


class Bullet:
    def __init__(self, name, position, direction, size=8, base_color=(255, 255, 255)):
        self.name = name
        self.size = size
        self.base_color = base_color
        self.color = self.base_color
        self.sprite = pg.image.load(f'assets/bullet_sprites/{self.name}.png').convert_alpha()
        self.sprite = pg.transform.scale(self.sprite, (self.size, self.size))
        self.sprite.fill(self.color, special_flags=pg.BLEND_RGBA_MULT)
        self.rect = self.sprite.get_rect()
        self.rect.x = position[0]
        self.rect.y = position[1]
        self.speed_x = direction[0]
        self.speed_y = direction[1]

        self.lifetime = 0
        self.max_lifetime = 10
        self.can_hit = True  # Prevent ball from hitting an object more than intended
        self.player_owned = [False, None]  # Check for the ball to only hit enemies
        self.is_alive = True
        self.reflect = False
        self.random_buff = None
        self.wild_mode = False
        self.wild_tick = [0, randint(15, 60)]
        self.tick = 0
        self.times_reflected = 0

    # Constantly update the instance
    def update(self, game):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        self.tick += 1

        if abs(self.speed_x) < 1 and abs(self.speed_y) < 1: game.bullets.remove(self)

        if self.wild_mode:
            self.wild_tick[0] += 1
            if self.wild_tick[0] >= self.wild_tick[1]:
                self.wild_tick[0] = 0
                self.wild_tick[1] = randint(15, 60)
                self.speed_x = randint(-5, 5)
                self.speed_y = randint(-5, 5)
                if self.speed_x == 0 and self.speed_y == 0: self.speed_x = 3

    def shield_collide_check(self, game, player):
        if not player:
            return

        # Check if the player's shield is being hit
        shield_rect = player.shield_rect

        if self.rect.colliderect(shield_rect) and self.can_hit and player.shield_enabled:
            # Get the relative position of the collision
            relative_collision_x = (self.rect.centerx - shield_rect.left) / shield_rect.width
            relative_collision_y = (self.rect.centery - shield_rect.top) / shield_rect.height
            offset_y = (relative_collision_y - 0.5) * 2
            offset_x = (relative_collision_x - 0.5) * 2

            # Adjust direction depending on bullet movement
            self.speed_x = offset_x * MAX_BULLET_SPEED
            self.speed_y = offset_y * MAX_BULLET_SPEED

            # Convert bullet's ownership to the player, now allowing it to damage enemies
            self.can_hit = False
            self.player_owned[0] = True
            self.player_owned[1] = player
            self.reflect = True
            game.sound.play_sfx('bounce')

            if player.bullet_powerup[0] and self.times_reflected <= player.bullet_powerup[1]:
                self.size += 3 * player.bullet_powerup[1]
            elif player.bullet_powerup[0]:
                self.size += 2

            self.sprite = pg.image.load(f'assets/bullet_sprites/{self.name}.png').convert_alpha()
            self.sprite = pg.transform.scale(self.sprite, (self.size, self.size))
            self.rect = pg.Rect(self.rect.x, self.rect.y, self.size, self.size)
            self.color = player.shield_color
            if self.name == 'bullet': self.sprite.fill(self.color)

            self.times_reflected += 1


    def player_collide_check(self, game, player):
        if not player:
            return

        # Deactivate shield and start cooldown timer if hit player
        if self.rect.colliderect(player.rect) and not self.player_owned[0] and player.shield_enabled:
            player.shield_enabled = False
            player.shield_cooldown = 0
            self.can_hit = False
            self.is_alive = False
            game.sound.play_sfx('player_damage')

    def draw(self):
        SCREEN.blit(self.sprite, self.rect)

