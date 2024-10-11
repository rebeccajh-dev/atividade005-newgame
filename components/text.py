"""
Class made to handle managing text and applying effects or changes
"""
from assets import TITLE_FONT, TEXT_FONT, NORMAL_FONT, SMALL_FONT
from config import SCREEN_WIDTH, COLOR_WHITE, COLOR_RED, SCREEN_HEIGHT, SCREEN

class Create:
    def __init__(self, text, rect, size, base_color=(255, 255, 255), blink_cd=15, blink_color=(255, 255, 200)):
        self.string = text
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
            if self.blink_tick >= self.blink_cd and self.visible:
                self.visible = False
                self.blink_tick = 0
            elif self.blink_tick >= self.blink_cd and not self.visible:
                self.visible = True
                self.blink_tick = 0

    def blink_text_color(self):
        if self.enabled and self.color_blink:
            if self.blink_tick >= self.blink_cd and self.current_color != self.blink_color:
                self.current_color = self.blink_color
                self.blink_tick = 0
            elif self.blink_tick >= self.blink_cd and self.current_color != self.base_color:
                self.current_color = self.base_color
                self.blink_tick = 0

    def draw(self):
        self.blink_tick += 1
        self.blink_text()
        self.blink_text_color()

        if self.enabled and self.visible:
            render_text = self.size.render(self.string, True, self.current_color)
            render_rect = render_text.get_rect(center=self.rect)

            SCREEN.blit(render_text, render_rect)

class Text:
    def __init__(self):
        # Creating text as class objects
        # Menu messages
        self.survived_text = Create('-=[ YOU SURVIVED ]=-', (SCREEN_WIDTH / 2, 100), TITLE_FONT,
                                  COLOR_WHITE, 30, (120, 255, 160))
        self.lost_text = Create('~X CAPTURED X~', (SCREEN_WIDTH / 2, 100), TITLE_FONT,
                            (255, 160, 50))
        self.final_message = Create('CONGRATULATIONS AND', (190, SCREEN_HEIGHT - 150),
                                TEXT_FONT, (255, 255, 255))
        self.final_message2 = Create('THANKS FOR PLAYING! :]', (185, SCREEN_HEIGHT - 115),
                                 TEXT_FONT, (255, 255, 255))

        self.title_text = Create('< WESTERN RAID >', (SCREEN_WIDTH / 2, 100), TITLE_FONT)
        self.player1_text = Create('PLAYER 1', (SCREEN_WIDTH / 2 - 100, 350), TEXT_FONT, COLOR_WHITE)
        self.player2_text = Create('PLAYER 2', (SCREEN_WIDTH / 2 + 100, 350), TEXT_FONT, COLOR_WHITE)
        self.select_text = Create('SELECT THE PLAYER(S)',
                              (SCREEN_WIDTH / 2, 270), TEXT_FONT, COLOR_WHITE, 30)
        self.choose_text = Create('use WASD or ARROW keys to select your player',
                              (SCREEN_WIDTH / 2, 300), TEXT_FONT, (120, 200, 255), 30)
        self.move_tip = Create(' WASD/ARROW keys to move !',
                           (SCREEN_WIDTH / 2, 430), TEXT_FONT, (255, 255, 255), 10)
        self.volume_text = Create('0 = Mute & -/+ keys to change volume',
                              (SCREEN_WIDTH / 2, 600), SMALL_FONT, (200, 200, 200), 30)
        self.start_text = Create('PRESS ENTER TO START',
                             (SCREEN_WIDTH / 2, 270), TEXT_FONT, COLOR_WHITE, 30)
        self.return_text = Create('PRESS ENTER TO GO BACK TO MENU',
                              (SCREEN_WIDTH / 2, SCREEN_HEIGHT - 40), TEXT_FONT, COLOR_WHITE, 30)

        self.full_score_text = Create('SCORE: 0000000', (SCREEN_WIDTH / 2, 180), NORMAL_FONT)
        self.new_best_text = Create('NEW BEST!', (SCREEN_WIDTH / 2, 220),
                                TEXT_FONT, (250, 230, 100), 10, (150, 255, 100))

        # Round stats messages
        self.p1_points_text = Create('00000', (90, 30), NORMAL_FONT)
        self.p2_points_text = Create('00000', (SCREEN_WIDTH - 90, 30), NORMAL_FONT)
        self.timer_text = Create('00:00', (SCREEN_WIDTH / 2, 30),
                             NORMAL_FONT, COLOR_WHITE, 30, (0, 255, 0))

        # In-round messages
        self.begin_message = Create("Bandits approaching, protect your ship until timer runs out!",
                                (SCREEN_WIDTH / 2, 170), TEXT_FONT, (255, 255, 0), 10)
        self.ambush_text = Create('!! AMBUSH INCOMING !!', (SCREEN_WIDTH / 2, 80), TEXT_FONT,
                              COLOR_RED, 15)
        self.get_in = Create('- THE SPACESHIP HAS BEEN FIXED! GET IN!! -', (SCREEN_WIDTH / 2, 80),
                         TEXT_FONT, COLOR_WHITE, 15, 8)

        # Error messages
        self.select_error = Create('SELECT A PLAYER', (SCREEN_WIDTH / 2, SCREEN_HEIGHT - 100),
                               TEXT_FONT, COLOR_RED, 8, (200, 100, 0))

        self.new_best_text.enabled = False
        self.select_error.enabled = False
        self.survived_text.color_blink = True
        self.new_best_text.color_blink = True
        self.select_error.color_blink = True
        self.ambush_text.blink = True
        self.start_text.blink = True
        self.select_text.blink = True
        self.return_text.blink = True
        self.get_in.blink = True