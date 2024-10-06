import pygame as pg

from config import SCREEN


class Objects:
    def __init__(self, name, spawn_pos):
        self.name = name
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

        self.collected = False
        self.visible = True
        self.blink = False

        self.lifetime = 0
        self.despawn_time = 10
        self.frame_tick = 0
        self.blink_tick = 0
        self.blink_cd = 15

        self.frame.fill((255, 255, 0), self.rect, special_flags=pg.BLEND_RGBA_MULT)

    def check_collect(self, player, ufo):
        if not player:
            return

        # Apply different functions depending on the object, if player collected
        if self.rect.colliderect(player.rect) and not self.collected:
            self.collected = True

            # Check for any ufo bricks to heal, if not then give points to player
            if self.name == 'brick':
                brick_healed = False
                brick_amount = len(ufo.ufos)

                for i in range(brick_amount):
                    if ufo.ufos[i][1] <= 0 and not brick_healed:
                        brick_healed = True
                        ufo.ufos[i][1] = 1

                if not brick_healed:
                    player.score += 25
            if self.name == 'brick_pu':
                brick_amount = len(ufo.ufos)

                for i in range(brick_amount):
                    if ufo.ufos[i][1] < 3:
                        ufo.ufos[i][1] += 1
                    else:
                        player.score += 15
            if self.name == 'bullet_pu':
                player.bullet_powerup[0] = True

                if player.bullet_powerup[1] < 3:
                    player.bullet_powerup[1] += 1
                else:
                    player.score += 100
            if self.name == 'shield_pu':
                player.shield_powerup[0] = True

                if player.shield_powerup[1] < 3:
                    player.shield_powerup[1] += 1
                else:
                    player.score += 100
            if self.name == 'shoot_pu':
                player.shoot_powerup[0] = True

                if player.shoot_powerup[1] < 3:
                    player.shoot_powerup[1] += 1
                else:
                    player.score += 100


    def update(self):
        if self.lifetime >= self.despawn_time - self.blink_seconds:
            self.blink = True

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
            if self.has_frame and self.frame_visible:
                SCREEN.blit(self.frame, self.rect)
