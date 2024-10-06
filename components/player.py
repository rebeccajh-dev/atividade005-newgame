"""
Class for player(s) functionalities, so we can make multiple players
with their own properties.
"""
from config import BASE_PLAYER_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT, BASE_SHIELD_X, BASE_SHIELD_Y, BASE_PLAYER_SPEED, \
    SHIELD_DISTANCE, FRAMERATE, SCREEN
import pygame as pg


class Player:
    def __init__(self, choosen_controls, player_count, color):
        self.controls = choosen_controls
        self.player_id = player_count    # Used to get and manipulate each player with ease
        self.sprite = pg.image.load(f'assets/player_sprites/{player_count}/body.png')
        self.eyes = pg.image.load(f'assets/player_sprites/{player_count}/eyes.png')
        self.sprite = pg.transform.scale(self.sprite, BASE_PLAYER_SIZE)
        self.eyes = pg.transform.scale(self.eyes, BASE_PLAYER_SIZE)

        self.rect = self.sprite.get_rect()
        self.rect.topleft = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.width = self.sprite.get_width()
        self.height = self.sprite.get_height()

        # Player's shield
        self.shield_x = 0
        self.shield_y = 0
        self.shield_width = BASE_SHIELD_X
        self.shield_height = BASE_SHIELD_Y
        self.shield_color = color
        self.shield_rect = pg.Rect(
            (SCREEN_WIDTH // 2) - (self.shield_width // 2),
            SCREEN_HEIGHT // 2,
            self.shield_width,
            self.shield_height
        )
        self.shield_rect.topleft = self.rect.topleft

        # Player values
        self.score = 0
        self.speed = BASE_PLAYER_SPEED
        self.shield_cooldown = 0
        self.push_power = 15

        self.shield_enabled = True
        self.facing_up = False
        self.moving = False
        self.last_key = ''
        self.eyes_offset = [0, 0]

        """
            Handle player behaviour depending on direction given
            The self.last_key conditions allows the shield to not break on diagonal movement
        """
    def change_direction(self, direction):
        if direction == 'left':
            self.rect.x -= self.speed
            if self.last_key != 'up' and self.last_key != 'down':
                self.shield_y = 0
                self.shield_width = BASE_SHIELD_Y
                self.shield_height = BASE_SHIELD_X
            self.eyes_offset = [-4, 0]
            self.shield_x = -SHIELD_DISTANCE
        if direction == 'right':
            self.rect.x += self.speed
            if self.last_key != 'up' and self.last_key != 'dowm':
                self.shield_y = 0
                self.shield_width = BASE_SHIELD_Y
                self.shield_height = BASE_SHIELD_X
            self.eyes_offset = [4, 0]
            self.shield_x = SHIELD_DISTANCE
        if direction == 'down':
            self.rect.y += self.speed
            if self.last_key == 'left' or self.last_key == 'right':
                self.eyes_offset[1] = 4
            else:
                self.eyes_offset = [0, 4]
                self.shield_x = 0
                self.shield_width = BASE_SHIELD_X
                self.shield_height = BASE_SHIELD_Y
            self.shield_y = SHIELD_DISTANCE
        if direction == 'up':
            self.rect.y -= self.speed
            if self.last_key == 'left' or self.last_key == 'right':
                self.eyes_offset[1] = -4
            else:
                self.facing_up = True
                self.shield_x = 0
                self.shield_width = BASE_SHIELD_X
                self.shield_height = BASE_SHIELD_Y
            self.shield_y = -SHIELD_DISTANCE
        else:
            self.facing_up = False

        # Save the last direction key pressed
        self.last_key = direction

    # Handle controls and changing sprites (shield, eyes, etc.)
    def move(self, keys):

        # Define a dictionary that maps control types to their respective key mappings
        key_mappings = {
            'WASD': {
                'left': pg.K_a,
                'right': pg.K_d,
                'down': pg.K_s,
                'up': pg.K_w
            },
            'ARROWS': {
                'left': pg.K_LEFT,
                'right': pg.K_RIGHT,
                'down': pg.K_DOWN,
                'up': pg.K_UP
            }
        }

        # Checking different keys depending on the current player controls
        self.rect.topleft = (self.rect.x, self.rect.y)

        # Check if the control type is valid
        if self.controls in key_mappings:
            controls = key_mappings[self.controls]

            # Directional key checks based on control type
            if keys[controls['left']]:
                self.change_direction('left')
            elif keys[controls['right']]:
                self.change_direction('right')

            if keys[controls['down']]:
                self.change_direction('down')
            elif keys[controls['up']]:
                self.change_direction('up')
            else:
                self.facing_up = False

        # Update the shield rotation and position
        self.shield_rect.width = self.shield_width
        self.shield_rect.height = self.shield_height
        self.shield_rect.center = self.rect.center
        self.shield_rect.x += self.shield_x
        self.shield_rect.y += self.shield_y

        # Making sure the player stays on screen
        self.rect.x = max(0, min(self.rect.x, SCREEN_WIDTH - self.width))
        self.rect.y = max(0, min(self.rect.y, SCREEN_HEIGHT - self.height))

        # Applying shield cooldown timer
        if not self.shield_enabled:
            self.shield_cooldown += 1
            if self.shield_cooldown % (3 * FRAMERATE) == 0:
                self.shield_enabled = True

    def draw(self):
        SCREEN.blit(self.sprite, self.rect)
        rect_pos = self.rect

        # Conditions for certain things to be drawn
        if self.moving:
            rect_pos = (self.rect.x + self.eyes_offset[0], self.rect.y + self.eyes_offset[1])
        if not self.facing_up:
            SCREEN.blit(self.eyes, rect_pos)
        if self.shield_enabled:
            self.eyes.set_alpha(255)
            self.sprite.set_alpha(255)
            pg.draw.rect(SCREEN, self.shield_color, self.shield_rect)
        else:
            self.eyes.set_alpha(128)
            self.sprite.set_alpha(128)
