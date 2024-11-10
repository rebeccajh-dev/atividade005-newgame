import pygame as pg

from components import text
from assets import TEXT_FONT
from config import SCREEN


class Objects:
    def __init__(self, name, spawn_pos):
        self.name = name
        self.type = 'item'
        self.sprite = pg.image.load(f'assets/item_sprites/{name}.png').convert_alpha()
        self.frame = pg.image.load(f'assets/item_frame.png').convert_alpha()
        self.color = (255, 255, 255)
        self.size = 40
        self.has_frame = True
        self.frame_visible = False
        self.blink_seconds = 3

        if name == 'brick':
            self.has_frame = False
            self.blink_seconds = 2
        if name == 'brick_pu':
            self.despawn_time = 15
        if name == 'bullet_pu':
            self.despawn_time = 15
        if name == 'shield_pu':
            self.despawn_time = 15
        if name == 'shoot_pu':
            self.despawn_time = 15

        self.sprite = pg.transform.scale(self.sprite, (self.size, self.size))
        self.frame = pg.transform.scale(self.frame, (self.size, self.size))

        self.rect = self.sprite.get_rect()
        self.rect.x = spawn_pos[0]
        self.rect.y = spawn_pos[1]
        self.pointer = text.Create('v', (self.rect.centerx, self.rect.centery - self.size),
                                   TEXT_FONT, (255, 255, 80))

        self.collected = False
        self.visible = True
        self.blink = False

        self.lifetime = 0
        self.despawn_time = 10
        self.frame_tick = 0
        self.blink_tick = 0
        self.blink_cd = 15

        self.pointer_tick = 0
        self.pointer_cd = 20
        self.pointer_down = False

        self.frame.fill((255, 255, 0), self.rect, special_flags=pg.BLEND_RGBA_MULT)

    def check_collect(self, game, player):
        if not player:
            return

        # Apply different functions depending on the object, if player collected
        if self.rect.colliderect(player.rect) and not self.collected:
            self.collected = True
            if self.name != 'brick':
                game.sound.play_sfx('powerup_get')

            # Check for any ufo bricks to heal, if not then give points to player
            if self.name == 'brick':
                brick_healed = False
                brick_amount = len(game.ufo.bricks)
                game.sound.play_sfx('brick_build')

                for i in range(brick_amount):
                    if game.ufo.bricks[i][1] <= 0 and not brick_healed:
                        brick_healed = True
                        game.ufo.bricks[i][1] = 1

                if not brick_healed:
                    game.sound.play_sfx('points')
                    player.score += 25
            if self.name == 'brick_pu':
                brick_amount = len(game.ufo.bricks)
                healed_bricks = 0
                game.sound.play_sfx('ufo_rebuild')

                for i in range(brick_amount):
                    if game.ufo.bricks[i][1] < 3:
                        game.ufo.bricks[i][1] += 1
                        healed_bricks += 1
                    else:
                        player.score += 15

                if healed_bricks < 1:
                    game.sound.play_sfx('points')
            if self.name == 'bullet_pu':
                player.bullet_powerup[0] = True
                game.sound.play_sfx('ufo_rebuild')

                if player.bullet_powerup[1] < 3:
                    player.bullet_powerup[1] += 1
                else:
                    player.score += 100
            if self.name == 'shield_pu':
                player.shield_powerup[0] = True

                if player.shield_powerup[1] < 3:
                    player.shield_powerup[1] += 1
                else:
                    game.sound.play_sfx('points')
                    player.score += 100
            if self.name == 'shoot_pu':
                player.shoot_powerup[0] = True

                if player.shoot_powerup[1] < 3:
                    player.shoot_powerup[1] += 1
                else:
                    game.sound.play_sfx('points')
                    player.score += 100


    def update(self):
        if self.lifetime >= self.despawn_time - self.blink_seconds:
            self.blink = True

        self.pointer_tick += 1
        if self.pointer_tick >= self.pointer_cd and self.pointer_down:
            self.pointer.rect = (self.rect.centerx, self.rect.centery - self.size - 10)
            self.pointer_tick = 0
            self.pointer_down = False
        elif self.pointer_tick >= self.pointer_cd and not self.pointer_down:
            self.pointer.rect = (self.rect.centerx, self.rect.centery - self.size)
            self.pointer_tick = 0
            self.pointer_down = True

    def blink_object(self):
        if self.blink:
            if self.blink_tick >= self.blink_cd and self.visible:
                self.visible = False
                self.blink_tick = 0
            elif self.blink_tick >= self.blink_cd and not self.visible:
                self.visible = True
                self.blink_tick = 0

    def blink_frame(self):
        if self.has_frame:
            if self.frame_tick >= self.blink_cd and self.frame_visible:
                self.frame_visible = False
                self.frame_tick = 0
            elif self.frame_tick >= self.blink_cd and not self.frame_visible:
                self.frame_visible = True
                self.frame_tick = 0

    def draw(self):
        self.blink_tick += 1
        self.frame_tick += 1
        self.blink_object()
        self.blink_frame()

        if self.visible:
            SCREEN.blit(self.sprite, self.rect)
            self.pointer.draw()
            if self.has_frame and self.frame_visible:
                SCREEN.blit(self.frame, self.rect)


class Explosion:
    def __init__(self, game, position, size):
        self.type = 'explosion'
        self.rect = pg.Rect(0, 0, size, size)
        self.rect.center = position
        self.life_tick = 0
        self.color_tick = 0
        self.max_lifetick = 40
        self.alive = True
        self.explosion_color = (255, 255, 255)

        self.ufo_collided = False

        game.sound.play_sfx('explode')

    def update(self):
        self.life_tick += 1
        self.color_tick += 1

        # Changing colors for explosion effect
        if self.color_tick >= 8 and self.explosion_color != (255, 130, 0):
            self.color_tick = 0
            self.explosion_color = (255, 130, 0)
        elif self.color_tick >= 8 and self.explosion_color != (255, 240, 0):
            self.color_tick = 0
            self.explosion_color = (255, 240, 0)

        if self.life_tick >= self.max_lifetick:
            self.alive = False

    def collide_player(self, game, player):
        if self.rect.colliderect(player.rect):
            player.damage_player(game)

    def collide_ufo(self, game):
        if not game.ufo.bricks:
            return

        brick_amount = len(game.ufo.bricks)

        # check the collides by the lists
        for i in range(brick_amount):
            rect, strength, brick_row, surface = game.ufo.bricks[i]

            # Checks if the bullet_sprites collides w ufo
            if self.rect.colliderect(rect) and strength >= 1:
                game.ufo.take_damage(game, i)

    def collide_check(self, game):
        if self.alive:
            # Checking collision with many different instances
            if game.player_1: self.collide_player(game, game.player_1)
            if game.player_2: self.collide_player(game, game.player_2)

            if not self.ufo_collided:
                self.ufo_collided = True
                self.collide_ufo(game)

            for terrain in game.level.map:
                if self.rect.colliderect(terrain.rect): terrain.destroy(game)

            for bandit in game.bandits:
                if self.rect.colliderect(bandit.rect): bandit.damage_bandit(game, 3)

            for bullet in game.bullets:
                if self.rect.colliderect(bullet.rect): bullet.is_alive = False

    def draw(self):
        if self.alive:
            pg.draw.rect(SCREEN, self.explosion_color, self.rect)
