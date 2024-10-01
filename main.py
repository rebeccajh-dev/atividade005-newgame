import pygame as pg
import random
import sys

pg.init()

# Screen & Interface configuration
SCREEN_WIDTH = 960
SCREEN_HEIGHT = 620
FRAMERATE = 60
SCREEN = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Constant variables
BASE_PLAYER_SIZE = (50, 50)
BASE_SHIELD_X = 130
BASE_SHIELD_Y = 20
SHIELD_DISTANCE = 70

BASE_PLAYER_SPEED = 3
BASE_ENEMY_SPEED = 2
MAX_BULLET_SPEED = 5

PLAYER_COLORS = [(120, 255, 120), (200, 120, 200)]
COLOR_RED = (255, 0, 0)
UFO_COLOR = (128, 128, 128)

# Global variables
background_color = (40, 20, 0)
game_instances = [] # Made to easily track and create different interactable objects
square_size = 30

# Class for player(s) functionalities, so we can make multiple players
# With their own properties
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

        self.shield_enabled = True
        self.facing_up = False
        self.moving = False
        self.last_key = ''
        self.eyes_offset = [0, 0]

    # Handle player behaviour depending on direction given
    # The self.last_key conditions allows the shield to not break on diagonal movement
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
        # Checking different keys depending on the current player controls
        self.rect.topleft = (self.rect.x, self.rect.y)

        if self.controls == 'WASD':
            if keys[pg.K_a]:
                self.change_direction('left')
            elif keys[pg.K_d]:
                self.change_direction('right')
            if keys[pg.K_s]:
                self.change_direction('down')
            elif keys[pg.K_w]:
                self.change_direction('up')
            else:
                self.facing_up = False
        elif self.controls == 'ARROWS':
            if keys[pg.K_LEFT]:
                self.change_direction('left')
            elif keys[pg.K_RIGHT]:
                self.change_direction('right')
            if keys[pg.K_DOWN]:
                self.change_direction('down')
            elif keys[pg.K_UP]:
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
            pg.draw.rect(SCREEN, self.shield_color, self.shield_rect)

# Class for spawning bullets and handling their behaviour,
# They have a position to be spawned at and a direction to constantly go
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
        self.player_owned = False  # Check for the ball to only hit enemies
        self.is_alive = True

    # Constantly update the instance (position, drawing, etc)
    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        pg.draw.rect(SCREEN, self.color, self.rect)

    def shield_collide_check(self, player):
        if not player:
            return

        # Check if the player's shield is being hit
        shield = player.shield_rect

        if self.rect.colliderect(shield) and self.can_hit and player.shield_enabled:
            # Get the relative position of the collision
            relative_collision_x = (self.rect.centerx - shield.left) / shield.width
            offset = (relative_collision_x - 0.5) * 2

            # Adjust direction depending on bullet movement
            self.speed_x = offset * MAX_BULLET_SPEED

            # Invert bullet direction
            self.speed_y *= -1

            # Convert bullet's ownership to the player, now allowing it to damage enemies
            self.color = player.shield_color
            self.can_hit = False
            self.player_owned = True


    def player_collide_check(self, player):
        if not player:
            return

        # Deactivate shield and start cooldown timer if hit player
        if self.rect.colliderect(player.rect) and not self.player_owned:
            player.shield_enabled = False
            player.shield_cooldown = 0
            self.can_hit = False
            self.is_alive = False

#Draw UFO
class Ufo:
    def __init__(self):
        self.live_ball = True
        self.width = square_size
        self.height = square_size
        self.ufos = []
        self.center_position()

    def center_position(self):
        # quantity of bricks
        top_row = 3
        middle_row = 5
        bottom_row = 3

        top_row_width = top_row * self.width
        middle_row_width = middle_row * self.width
        bottom_row_width = bottom_row * self.width

        y = (SCREEN_HEIGHT - (3 * self.height)) // 2

        # calculate the x positions
        top_row_x = (SCREEN_WIDTH - top_row_width) // 2
        middle_row_x = (SCREEN_WIDTH - middle_row_width) // 2
        bottom_row_x = (SCREEN_WIDTH - bottom_row_width) // 2

        # add bricks in top
        strength = 4
        for col in range(top_row):
            rect = pg.Rect(top_row_x + col * self.width, y, self.width, self.height)
            self.ufos.append([rect, strength])


        # add bricks in the middle
        strength = 3
        for col in range(middle_row):
            rect = pg.Rect(middle_row_x + col * self.width, y + self.height, self.width, self.height)
            self.ufos.append([rect, strength])

        # add bricks in the bottom
        strength = 2
        for col in range(bottom_row):
            rect = pg.Rect(bottom_row_x + col * self.width, y + 2 * self.height, self.width, self.height)
            self.ufos.append([rect, strength])


    def draw_UFO(self, surface):
        if self.live_ball:
            for brick in self.ufos:
                rect, strength = brick
                # change the color based in the strength
                color = UFO_COLOR if strength > 0 else COLOR_RED
                pg.draw.rect(surface, color, rect)
                pg.draw.rect(surface, background_color, rect, 2)

class Game:
    def __init__(self):
        self.on_menu = True
        self.clock = pg.time.Clock()
        self.player_1 = None
        self.player_2 = None
        self.player_count = 0
        self.game_tick = 0
        self.ufo = Ufo()

    def run(self):
        while True:
            self.update_game_state()
            self.handle_events()
            self.clock.tick(FRAMERATE)
            self.game_tick = pg.time.get_ticks()    # Save the game time in milliseconds

    def handle_events(self):
        keys = pg.key.get_pressed()

        # Detecting player joining the game
        if keys[pg.K_w] or keys[pg.K_a] or keys[pg.K_s] or keys[pg.K_d]:
            if not self.player_1:
                color = PLAYER_COLORS[self.player_count]
                self.player_count += 1
                self.player_1 = Player('WASD', self.player_count, color)
        if keys[pg.K_UP] or keys[pg.K_LEFT] or keys[pg.K_DOWN] or keys[pg.K_RIGHT]:
            if not self.player_2:
                color = PLAYER_COLORS[self.player_count]
                self.player_count += 1
                self.player_2 = Player('ARROWS', self.player_count, color)

        for event in pg.event.get():
            # Quit the game
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

    # Merged "draw" function with game state to make bullets possible
    def update_game_state(self):
        SCREEN.fill(background_color)
        self.create_instances()
        keys = pg.key.get_pressed()
        self.ufo.draw_UFO(SCREEN)

        # Player movement check
        if self.player_1:
            if keys[pg.K_w] or keys[pg.K_a] or keys[pg.K_s] or keys[pg.K_d]:
                self.player_1.move(keys)
                self.player_1.moving = True
            else:
                self.player_1.moving = False
        if self.player_2:
            if keys[pg.K_UP] or keys[pg.K_LEFT] or keys[pg.K_DOWN] or keys[pg.K_RIGHT]:
                self.player_2.move(keys)
                self.player_2.moving = True
            else:
                self.player_2.moving = False

        # Go through all instances and check their functions and constraints
        for instance in game_instances[:]:
            instance.update()
            if self.game_tick % FRAMERATE == 0:
                instance.lifetime += 1

            # Specifying functions for certain instances using their name
            if instance.name == 'BULLET':
                instance.player_collide_check(self.player_1)
                instance.shield_collide_check(self.player_1)
                instance.player_collide_check(self.player_2)
                instance.shield_collide_check(self.player_2)

            # Clearing objects if offscreen or lived too long
            if ((SCREEN_WIDTH < instance.rect.x or instance.rect.x < 0) or
                (SCREEN_HEIGHT < instance.rect.y or instance.rect.y < 0) or
                instance.lifetime > instance.max_lifetime) or not instance.is_alive:
                game_instances.remove(instance)

        # Drawing players if existing
        if self.player_1:
            self.player_1.draw()
        if self.player_2:
            self.player_2.draw()

        pg.display.flip()

    # Constantly making instances, spawning bullets should be replaced
    # With the cowboy NPCs instead, and they should fire the bullets
    def create_instances(self):
        if self.game_tick % 30 == 0:  # Frequency of bullets spawned
            bullet_side = random.randint(1, 4)
            bullet_position = [0, 0]
            bullet_direction = [0, 0]

            # Randomly spawn bullets in different sides of the screen
            if bullet_side == 1:  # Left
                bullet_position = [0, random.randint(0, SCREEN_HEIGHT)]
                bullet_direction = [random.randint(2, 4), random.randint(-3, 3)]
            elif bullet_side == 2:  # Right
                bullet_position = [SCREEN_WIDTH, random.randint(0, SCREEN_HEIGHT)]
                bullet_direction = [random.randint(-4, -2), random.randint(-3, 3)]
            elif bullet_side == 3:  # Up
                bullet_position = [random.randint(0, SCREEN_WIDTH), 0]
                bullet_direction = [random.randint(-3, 3), random.randint(2, 4)]
            elif bullet_side == 4:  # Down
                bullet_position = [random.randint(0, SCREEN_WIDTH), SCREEN_HEIGHT]
                bullet_direction = [random.randint(-3, 3), random.randint(-4, -2)]

            # Create the new bullet and add it into instances list
            new_bullet = Bullet(bullet_position, bullet_direction)
            game_instances.append(new_bullet)


if __name__ == '__main__':
    pg.init()
    game = Game()
    game.run()
