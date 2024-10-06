"""
Class for spawning bullets and handling their behaviour,
they have a position to be spawned at and a direction to constantly go.
"""
from config import SCREEN, MAX_BULLET_SPEED
import pygame as pg


class Bullet:
    def __init__(self, position, direction):
        self.name = 'BULLET'
        self.size = 8
        self.color = (255, 255, 255)
        self.rect = pg.Rect(position[0], position[1], self.size, self.size)
        self.speed_x = direction[0]
        self.speed_y = direction[1]

        self.lifetime = 0
        self.max_lifetime = 10
        self.can_hit = True  # Prevent ball from hitting an object more than intended
        self.player_owned = [False, None]  # Check for the ball to only hit enemies
        self.is_alive = True
        self.reflect = False

    # Constantly update the instance (position, drawing, etc)
    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        pg.draw.rect(SCREEN, self.color, self.rect)

    def shield_collide_check(self, player):
        if not player:
            return

        # Check if the player's shield is being hit
        shield_rect = player.shield_rect

        if self.rect.colliderect(shield_rect) and self.can_hit and player.shield_enabled:
            # Get the relative position of the collision
            relative_collision_x = (self.rect.centerx - shield_rect.left) / shield_rect.width
            offset = (relative_collision_x - 0.5) * 2

            # Adjust direction depending on bullet movement
            self.speed_x = offset * MAX_BULLET_SPEED

            # Invert bullet direction
            self.speed_y *= -1

            # Convert bullet's ownership to the player, now allowing it to damage enemies
            self.color = player.shield_color
            self.can_hit = False
            self.player_owned[0] = True
            self.player_owned[1] = player
            self.reflect = True

            if player.bullet_powerup[0]:
                self.size += 3 * player.bullet_powerup[1]
                self.rect = pg.Rect(self.rect.x, self.rect.y, self.size, self.size)


    def player_collide_check(self, player):
        if not player:
            return

        # Deactivate shield and start cooldown timer if hit player
        if self.rect.colliderect(player.rect) and not self.player_owned[0] and player.shield_enabled:
            player.shield_enabled = False
            player.shield_cooldown = 0
            self.can_hit = False
            self.is_alive = False
