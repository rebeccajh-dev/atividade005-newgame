import pygame as pg

from config import SCREEN


class Music:
    def __init__(self):
        pg.mixer.init()
        self.mute = False
        self.volume_offset = 0.5
        self.sfx_offset = 0.35
        self.button_pressed = False

    def play(self, song, loop=0):
        pg.mixer.stop()

        pg.mixer.music.load(f'assets/music/{song}.mp3')
        pg.mixer.music.set_volume(self.volume_offset)

        pg.mixer.music.play(loop)

    def play_sfx(self, sfx):
        sound = pg.mixer.Sound(f'assets/SFX/{sfx}.wav')
        sound.set_volume(self.sfx_offset)
        sound.play()

    def stop(self):
        pg.mixer.stop()

    def mute_music(self):
        if not self.button_pressed:
            if self.mute:
                self.mute = False
                self.volume_offset = 0.5
            else:
                self.mute = True
                self.volume_offset = 0
            self.button_pressed = True
            pg.mixer.music.set_volume(self.volume_offset)

    def change_volume(self, volume_change):
        if not self.button_pressed:
            self.button_pressed = True

            if volume_change == 'increase' and self.volume_offset < 1:
                self.volume_offset = round(self.volume_offset + 0.1, 2)
                pg.mixer.music.set_volume(self.volume_offset)
            if volume_change == 'decrease' and self.volume_offset > 0:
                self.volume_offset = round(self.volume_offset - 0.1, 2)
                pg.mixer.music.set_volume(self.volume_offset)