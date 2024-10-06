"""
Class made to handle managing text and applying effects or changes
"""
from config import SCREEN

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
            render_text = self.size.render(self.text, True, self.current_color)
            render_rect = render_text.get_rect(center=self.rect)

            SCREEN.blit(render_text, render_rect)
