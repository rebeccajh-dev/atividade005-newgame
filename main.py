import math
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
square_size = 50

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
            self.reflect = True


    def player_collide_check(self, player):
        if not player:
            return

        # Deactivate shield and start cooldown timer if hit player
        if self.rect.colliderect(player.rect) and not self.player_owned:
            player.shield_enabled = False
            player.shield_cooldown = 0
            self.can_hit = False
            self.is_alive = False

class Bandit:
    def __init__(self, start_x, start_y):
        self.name = 'BANDIT'
        self.live_bandit = True
        self.rect = pg.Rect(start_x, start_y, 40, 40)  # bandit size
        self.bullets = []
        self.shoot_timer = 0
        self.move_timer = 0
        self.interval = 300 #(300 ticks is equal a 5 sec)
        self.direction = (random.choice([-1, 1]), random.choice([-1, 1]))
        self.in_screen = False

    def move_bandit(self):
        if self.live_bandit:
            new_x = self.rect.x + self.direction[0] * 2
            new_y = self.rect.y + self.direction[1] * 2

            # verify the limits of the screen
            if new_x < 0 or new_x + self.rect.width > SCREEN_WIDTH:
                self.direction = (-self.direction[0], self.direction[1])
            if new_y < 0 or new_y + self.rect.height > SCREEN_HEIGHT:
                self.direction = (self.direction[0], -self.direction[1])

            self.rect.x += self.direction[0] * 2
            self.rect.y += self.direction[1] * 2
        
    def update(self, target_position):
        self.shoot_timer += 1

       # move each 5 secs
        if self.move_timer >= self.interval:
            self.move_bandit()
            self.direction = (random.choice([-5, 5]), random.choice([-5, 5]))
            self.move_timer = 0

        self.shoot_timer += 1

        if self.shoot_timer >= 100:
            self.shoot(target_position)
            self.shoot_timer = 0


    def shoot(self, target_position):
        direction_x = target_position[0] - self.rect.centerx
        direction_y = target_position[1] - self.rect.centery
        magnitude = math.sqrt(direction_x**2 + direction_y**2)
        if magnitude != 0:
            direction = (direction_x / magnitude * 3, direction_y / magnitude * 3)  
            bullet_position = (self.rect.centerx, self.rect.bottom)
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
                bullets_to_remove.append(bullet)
                break

            if not bullet.is_alive:
                bullets_to_remove.append(bullet)

        for bullet in bullets_to_remove:
            if bullet in self.bullets:
                self.bullets.remove(bullet)

    def draw_bandit(self):
        pg.draw.rect(SCREEN, (255, 0, 0), self.rect) 

#Draw UFO
class Ufo:
    def __init__(self):
        self.live_ball = True
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

        # check the collides by the lists
        for i in range(len(self.ufos)):
            rect, strength = self.ufos[i]

            # Checks if the bullets collides w ufo
            if bullet.rect.colliderect(rect) and bullet.can_hit:
                bullet.can_hit = False
                bullet.is_alive = False
                self.take_damage(i)
                break

    def take_damage(self, index):
        if index < len(self.ufos):
            self.ufos[index][1] -= 1
            if self.ufos[index][1] < 0:
                self.ufos[index][1] = 0  # Manter a força em zero

    def center_position(self):
        # Define the UFO grid as a list of lists
        ufo_grid = [
            [1, 1, 1, 1, 1],
            [1, 1],
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
            self.bandits = []
            self.max_bandits = 2
            self.left_bandits_count = 0
            self.right_bandits_count = 0

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

        # just for now, trying to change for the class Bandit
        def bandit_position(self):
            if self.game_tick % 300 == 0:  # add a bandit each 300 ticks
                if self.left_bandits_count < self.max_bandits:
                    start_x = 10
                    start_y = random.randint(10, SCREEN_HEIGHT - 40)
                    bandit = Bandit(start_x, start_y)
                    self.bandits.append(bandit)
                    self.left_bandits_count += 1

                if self.right_bandits_count < self.max_bandits:
                    start_x = SCREEN_WIDTH - 50
                    start_y = random.randint(10, SCREEN_HEIGHT - 40)
                    bandit = Bandit(start_x, start_y)
                    self.bandits.append(bandit)
                    self.right_bandits_count += 1

        # Merged "draw" function with game state to make bullets possible
        def update_game_state(self):
            SCREEN.fill(background_color)
            keys = pg.key.get_pressed()
            self.ufo.draw_UFO(SCREEN)
            self.bandit_position()

            for bandit in self.bandits:
                if bandit.live_bandit:
                    bandit.update(self.ufo.rect.topleft)  # Pass ufo as target
                    bandit.update_bullets()
                    bandit.draw_bandit()

                # collision of bullets w ufo
                for bullet in bandit.bullets:
                    bullet.shield_collide_check(self.player_1)  # collision w shield player 1
                    bullet.player_collide_check(self.player_1)
                    bullet.player_collide_check(self.player_2)
                    bullet.shield_collide_check(self.player_2)
                    self.ufo.ufo_collide_check(bullet)

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

            # probably we will not gonna need that
            # # Go through all instances and check their functions and constraints
            # for instance in game_instances[:]:
            #     instance.update()
            #     if self.game_tick % FRAMERATE == 0:
            #         instance.lifetime += 1

            #     # Specifying functions for certain instances using their name
            #     if instance.name == 'BULLET':
            #         instance.player_collide_check(self.player_1)
            #         instance.shield_collide_check(self.player_1)
            #         instance.player_collide_check(self.player_2)
            #         instance.shield_collide_check(self.player_2)
            #         self.ufo.ufo_collide_check(instance)

            #     # Clearing objects if offscreen or lived too long
            #     if ((SCREEN_WIDTH < instance.rect.x or instance.rect.x < 0) or
            #         (SCREEN_HEIGHT < instance.rect.y or instance.rect.y < 0) or
            #         instance.lifetime > instance.max_lifetime) or not instance.is_alive:
            #         game_instances.remove(instance)

            # Drawing players if existing
            if self.player_1:
                self.player_1.draw()
            if self.player_2:
                self.player_2.draw()

            pg.display.flip()


if __name__ == '__main__':
    pg.init()
    game = Game()
    game.run()
