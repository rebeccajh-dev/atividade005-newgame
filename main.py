import math
import pygame as pg
import random
import sys

pg.init()

# Screen configuration
SCREEN_WIDTH = 960
SCREEN_HEIGHT = 620
FRAMERATE = 60
SCREEN = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Basic color configuration
PLAYER_COLORS = [(120, 255, 120), (200, 120, 200)]
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_RED = (255, 0, 0)
COLOR_DAMAGED = (160, 0, 0)
UFO_COLORS = [
    (240, 240, 240),
    (240, 240, 240),
    (240, 240, 240),
    (100, 200, 100),
    (100, 200, 100)
]

TERRAIN_COLORS = [
    (0, 0, 0),
    (40, 110, 60),
    (40, 110, 60),
    (80, 60, 40),
    (80, 60, 40)
]

# Constant variables
BASE_PLAYER_SIZE = (50, 50)
BASE_SHIELD_X = 130
BASE_SHIELD_Y = 20
SHIELD_DISTANCE = 70
ROUND_TIME = 180

BASE_PLAYER_SPEED = 4
BASE_ENEMY_SPEED = 2
MAX_BULLET_SPEED = 5
RANDOM_MOVE = [-1, -0.5, 0.25, 0, 0.25, 0.5, 1]

# Interface configuration
TEXT_FONT = pg.font.Font("assets/retro_font.ttf", 24)
NORMAL_FONT = pg.font.Font("assets/retro_font.ttf", 40)
TITLE_FONT = pg.font.Font("assets/retro_font.ttf", 72)

TITLE_SPRITE = pg.image.load(f'assets/player_sprites/1/body.png')
TITLE_SPRITE = pg.transform.scale(TITLE_SPRITE, BASE_PLAYER_SIZE)
TITLE_SPRITE_RECT = TITLE_SPRITE.get_rect()
TITLE_SPRITE_RECT.center = (SCREEN_WIDTH // 2, 440)

TITLE_SPRITE_EYES = pg.image.load(f'assets/player_sprites/1/eyes.png')
TITLE_SPRITE_EYES = pg.transform.scale(TITLE_SPRITE_EYES, BASE_PLAYER_SIZE)
TITLE_SPRITE_EYES_RECT = TITLE_SPRITE_EYES.get_rect()
TITLE_SPRITE_EYES_RECT.center = ((SCREEN_WIDTH // 2) - 4, 440)

# Global variables
menu_color = (10, 10, 30)
background_color = (40, 20, 0)
square_size = 25

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
        self.push_power = 15

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
            self.eyes.set_alpha(255)
            self.sprite.set_alpha(255)
            pg.draw.rect(SCREEN, self.shield_color, self.shield_rect)
        else:
            self.eyes.set_alpha(128)
            self.sprite.set_alpha(128)

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


    def player_collide_check(self, player):
        if not player:
            return

        # Deactivate shield and start cooldown timer if hit player
        if self.rect.colliderect(player.rect) and not self.player_owned[0] and player.shield_enabled:
            player.shield_enabled = False
            player.shield_cooldown = 0
            self.can_hit = False
            self.is_alive = False

class Bandit:
    def __init__(self, spawn_pos):
        random_size = random.choice([50, 60, 70])

        self.name = 'BANDIT'
        self.sprite = pg.image.load(f'assets/bandit_sprites/bandit1.png')
        self.sprite = pg.transform.scale(self.sprite, (random_size, random_size))
        self.rect = self.sprite.get_rect() # Bandit size
        self.rect.x = spawn_pos[0]
        self.rect.y = spawn_pos[1]

        self.live_bandit = True
        self.bullets = []
        self.spawnpoint = [spawn_pos[2], spawn_pos[3]]

        self.shoot_timer = 0
        self.move_timer = 0
        self.base_shoot_cd = 180
        self.shoot_cd = random.randint(self.base_shoot_cd, int(self.base_shoot_cd * 2))
        self.move_cd = random.randint(120, 200)
        self.moving_time = random.randint(30, 180)
        self.direction = (random.choice(RANDOM_MOVE), random.choice(RANDOM_MOVE))
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
            self.move_cd = random.randint(180, 900)
            self.moving_time = random.randint(30, 180)
            self.direction = (random.choice(RANDOM_MOVE), random.choice(RANDOM_MOVE))
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
            self.shoot_cd = random.randint(self.base_shoot_cd, int(self.base_shoot_cd * 2))
            self.shoot(target_position)
            self.shoot_timer = 0


    def shoot(self, target_position):
        direction_x = target_position[0] - self.rect.centerx
        direction_y = target_position[1] - self.rect.centery
        magnitude = math.sqrt(direction_x**2 + direction_y**2)

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

#Draw UFO
class Ufo:
    def __init__(self):
        self.live_ball = True
        self.fully_broken = False
        self.width = square_size
        self.height = square_size
        self.size = square_size
        self.ufos = []
        self.center_position()
        self.rect = pg.Rect(SCREEN_WIDTH // 2 - self.size // 2, SCREEN_HEIGHT // 2 - self.size // 2, self.size,
                            self.size)

    def ufo_collide_check(self, bullet):
        if not self.ufos:
            return

        brick_amount = len(self.ufos)
        broken_amount = 0

        # check the collides by the lists
        for i in range(brick_amount):
            rect, strength, brick_row = self.ufos[i]

            if self.ufos[i][1] <= 0:
                broken_amount += 1

            # Checks if the bullets collides w ufo
            if (bullet.rect.colliderect(rect) and bullet.can_hit
                and self.ufos[i][1] >= 1):
                bullet.can_hit = False
                bullet.is_alive = False
                self.take_damage(i)
                break

        if broken_amount >= brick_amount:
            self.fully_broken = True

    def take_damage(self, index):
        if index < len(self.ufos):
            self.ufos[index][1] -= 1
            if self.ufos[index][1] < 0:
                self.ufos[index][1] = 0  # Manter a força em zero

    def center_position(self):
        # Define the UFO grid as a list of lists
        ufo_grid = [
            [1, 1, 1],
            [1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1]
        ]

        # Calculate the total height of the UFOs
        total_height = sum(len(row) * self.height for row in ufo_grid)

        # Calculate the starting y position to center the rows
        y = (SCREEN_HEIGHT - 400)

        for row_index, strengths in enumerate(ufo_grid):
            strength = strengths[0]  # Assuming uniform strength for each column in this row
            row_width = len(strengths) * self.width

            # Calculate the starting x position for the current row
            x = (SCREEN_WIDTH - row_width) // 2

            # Add UFOs for the current row
            for col_index, strength in enumerate(strengths):
                rect = pg.Rect(x + col_index * self.width, y + row_index * self.height, self.width, self.height)
                self.ufos.append([rect, strength, row_index])

    def draw_UFO(self, surface):
        if self.live_ball:
            for brick in self.ufos:
                rect, strength, brick_row = brick
                # change the color based in the strength
                color = UFO_COLORS[brick_row] if strength > 0 else COLOR_DAMAGED
                pg.draw.rect(surface, color, rect)
                pg.draw.rect(surface, background_color, rect, 2)


class Terrain:
    def __init__(self, spawn_pos, index, size):
        self.name = 'TERRAIN'
        self.sprite = pg.image.load(f'assets/terrain_sprites/{index}.png').convert_alpha()
        self.sprite = pg.transform.scale(self.sprite, (size, size))
        self.sprite.fill(TERRAIN_COLORS[index], special_flags=pg.BLEND_RGBA_MULT)

        self.rect = self.sprite.get_rect() # Bandit size
        self.rect.x = spawn_pos[0]
        self.rect.y = spawn_pos[1]

    def draw(self):
        SCREEN.blit(self.sprite, self.rect)


# Class made to handle managing text and applying effects or changes
class Text:
    def __init__(self, text, rect, size, base_color=(255, 255, 255), blink_cd=15, blink_color=(255, 255, 200)):
        self.text = text
        self.rect = rect
        self.size = size
        self.enabled = True
        self.visible = True

        # Visual effects for text
        self.blink = False
        self.color_blink = False
        self.base_color = base_color
        self.current_color = base_color
        self.blink_color = blink_color
        self.blink_tick = 0
        self.blink_cd = blink_cd

    def blink_text(self):
        if self.enabled and self.blink:
            if self.blink_tick >= self.blink_cd == 0 and self.visible:
                self.visible = False
            elif self.blink_tick >= self.blink_cd * 2:
                self.visible = True
                self.blink_tick = 0

    def blink_text_color(self):
        if self.enabled and self.color_blink:
            if self.blink_tick >= self.blink_cd == 0 and self.visible:
                self.current_color = self.blink_color
            elif self.blink_tick >= self.blink_cd * 2:
                self.current_color = self.base_color
                self.blink_tick = 0

    def draw(self):
        if self.enabled and self.visible:
            self.blink_tick += 1
            self.blink_text()
            self.blink_text_color()

            render_text = self.size.render(self.text, True, self.base_color)
            render_rect = render_text.get_rect(center=self.rect)
            SCREEN.blit(render_text, render_rect)

class Game:
        def __init__(self):
            self.on_menu = True
            self.clock = pg.time.Clock()
            self.player_1 = None
            self.player_2 = None
            self.player_count = 0
            self.game_tick = 0
            self.game_timer = 0
            self.difficulty_time = 15   # Time in seconds of when difficulty increases
            self.ambush_time = random.randint(80, 100)   # Time in seconds of when ambush mode activates

            # Creating text as class objects
            self.title_text = Text('< WESTERN RAID >', (SCREEN_WIDTH / 2, 100), TITLE_FONT)
            self.start_text = Text('press WASD/ARROW keys to start',
                                   (SCREEN_WIDTH / 2, 300), TEXT_FONT, COLOR_WHITE, 30)

            self.p1_points_text = Text('00000', (90, 30), NORMAL_FONT)
            self.p2_points_text = Text('00000', (SCREEN_WIDTH - 90, 30), NORMAL_FONT)
            self.timer_text = Text('00:00', (SCREEN_WIDTH / 2, 30),
                                   NORMAL_FONT, COLOR_WHITE, 30, (0, 255, 0))
            self.ambush_text = Text('!! AMBUSH INCOMING !!', (SCREEN_WIDTH / 2, 80), TEXT_FONT,
                                    COLOR_RED, 15)

            self.start_text.blink = True
            self.ufo = Ufo()
            self.bandits = []
            self.terrain = []
            self.max_bandits = 0
            self.bandit_count = 0
            self.bandit_spawnrate = 120

            self.draw_map()

        def draw_map(self):
            self.ufo = Ufo()
            self.terrain = []

            # Grid used to spawn terrain, 1 allows spawning and 0 makes it empty
            # IMPORTANT: The rotation of the grid is different from the rotation
            # of the screen by 90 degrees clockwise
            terrain_grid = [
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1],
                [1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1],
                [1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1],
                [1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1],
                [1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1],
                [1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1],
                [1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1],
                [1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            ]
            terrain_counter = 1

            for row_index, row in enumerate(terrain_grid):
                for col_index, column in enumerate(row):
                    terrain_counter += 1

                    if column != 0 and terrain_counter % random.randint(1, 12) == 0:
                        random_index = random.randint(1, 4)

                        if random_index != 3:  # Condition for larger sprites
                            terrain_size = 70
                        else:
                            terrain_size = 140

                        pos_x = row_index * 80
                        pos_y = col_index * 80
                        new_asset = Terrain([pos_x, pos_y], random_index, terrain_size)
                        self.terrain.append(new_asset)

        def run(self):
            while True:
                self.update_game_state()
                self.handle_events()
                self.clock.tick(FRAMERATE)
                self.game_tick = pg.time.get_ticks()  # Save the game time in milliseconds

        def handle_events(self):
            keys = pg.key.get_pressed()

            # Detecting player joining the game
            if keys[pg.K_w] or keys[pg.K_a] or keys[pg.K_s] or keys[pg.K_d]:
                if not self.player_1:
                    self.on_menu = False
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

        # just for now, trying to change for the class Bandita
        def bandit_position(self):
            if (self.game_tick % self.bandit_spawnrate == 0
                and self.bandit_count < self.max_bandits):  # add a bandit each 300 ticks
                spawn_direction = random.choice(['left', 'right'])
                start_pos = [0, 0, # Position that spawns at first
                             0, 0] # Goal position to move to

                if spawn_direction == 'left':
                    start_pos[0] = -50
                    start_pos[1] = random.randint(10, SCREEN_HEIGHT - 40)
                    start_pos[2] = random.randint(30, 100)
                    start_pos[3] = start_pos[1]
                if spawn_direction == 'right':
                    start_pos[0] = SCREEN_WIDTH
                    start_pos[1] = random.randint(10, SCREEN_HEIGHT - 40)
                    start_pos[2] = SCREEN_WIDTH - random.randint(70, 140)
                    start_pos[3] = start_pos[1]

                bandit = Bandit(start_pos)
                self.bandits.append(bandit)

        # Merged "draw" function with game state to make bullets possible
        def update_game_state(self):
            keys = pg.key.get_pressed()

            if self.on_menu:
                SCREEN.fill(menu_color)
                self.title_text.draw()
                self.start_text.draw()
                SCREEN.blit(TITLE_SPRITE, TITLE_SPRITE_RECT)
                SCREEN.blit(TITLE_SPRITE_EYES, TITLE_SPRITE_EYES_RECT)
            else:
                SCREEN.fill(background_color)

                for terrain in self.terrain:
                    terrain.draw()

                self.ufo.draw_UFO(SCREEN)

                if self.ufo.fully_broken:
                    self.on_menu = True
                    self.game_timer = 0
                    self.bandits = []
                    self.player_1 = None
                    self.player_2 = None
                    return

                self.bandit_position()
                self.max_bandits = 2 + (2 * self.player_count)
                self.bandit_spawnrate = int(120 - (15 * self.player_count))
                self.bandit_count = len(self.bandits)

                if self.game_tick % FRAMERATE == 0:
                    self.game_timer += 1

                for bandit in self.bandits:
                    if bandit.live_bandit:
                        bandit.update(self.ufo.rect.topleft)  # Pass ufo as target
                        bandit.update_bullets()
                        bandit.shield_collide_check(self.player_1)
                        bandit.shield_collide_check(self.player_2)
                        bandit.draw_bandit()
                    else:
                        self.bandits.remove(bandit)

                    # collision of bullets w ufo
                    for bullet in bandit.bullets:
                        bullet.shield_collide_check(self.player_1)  # collision w shield player 1
                        bullet.player_collide_check(self.player_1)
                        bullet.player_collide_check(self.player_2)
                        bullet.shield_collide_check(self.player_2)
                        if self.game_tick % FRAMERATE == 0:
                            bullet.lifetime += 1

                        self.ufo.ufo_collide_check(bullet)

                    if self.game_tick % FRAMERATE == 0:
                        bandit.lifetime += 1

                # Player movement check and drawing
                if self.player_1:
                    if keys[pg.K_w] or keys[pg.K_a] or keys[pg.K_s] or keys[pg.K_d]:
                        self.player_1.move(keys)
                        self.player_1.moving = True
                    else:
                        self.player_1.moving = False

                    self.player_1.draw()
                    self.p1_points_text.text = str("{:05d}".format(self.player_1.score))
                    self.p1_points_text.draw()
                if self.player_2:
                    if keys[pg.K_UP] or keys[pg.K_LEFT] or keys[pg.K_DOWN] or keys[pg.K_RIGHT]:
                        self.player_2.move(keys)
                        self.player_2.moving = True
                    else:
                        self.player_2.moving = False

                    self.player_2.draw()
                    self.p2_points_text.text = str("{:05d}".format(self.player_2.score))
                    self.p2_points_text.draw()

                # Drawing UI
                time_left = ROUND_TIME - self.game_timer
                seconds = time_left % 60
                minutes = int(time_left / 60) % 60
                self.timer_text.text = f'{minutes:02}:{seconds:02}'
                self.timer_text.draw()

            pg.display.flip()



if __name__ == '__main__':
    pg.init()
    game = Game()
    game.run()
