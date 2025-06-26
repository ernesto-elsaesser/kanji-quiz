import pygame
import random


BACKGROUND_COLOR = (0, 0, 0)
TEXT_COLOR = (200, 200, 200)
CORRECT_COLOR = (0, 200, 0)
INCORRECT_COLOR = (200, 0, 0)

DPAD_COORDS = {
    pygame.K_UP: (0.5, 0.55),
    pygame.K_LEFT: (0.3, 0.7),
    pygame.K_RIGHT: (0.7, 0.7),
    pygame.K_DOWN: (0.5, 0.85)
}


class Game:

    def __init__(self, width, height, latin_font, kanji_font, kanji_dict):

        self.screen = pygame.display.set_mode((width, height))

        self.latin_font = latin_font
        self.kanji_font = kanji_font

        self.meanings = kanji_dict
        self.kanjis = list(kanji_dict)

        self.options = []
        self.kanji = ""
        self.selected = 0
        self.debug = None

    def press(self, key_code):

        if self.selected is None:
            if key_code in DPAD_COORDS:
                self.selected = key_code
            else:
                self.debug = str(key_code)
        else:
            self.options = random.sample(self.kanjis, 4)
            self.kanji = random.choice(self.options)
            self.selected = None

        self.draw()

    def draw(self):

        self.screen.fill(BACKGROUND_COLOR)

        self.draw_text(self.kanji_font, self.kanji, TEXT_COLOR, 0.5, 0.25)

        for key_code, option in zip(DPAD_COORDS, self.options):
            option_color = TEXT_COLOR
            if key_code == self.selected:
                if option == self.kanji:
                    option_color = CORRECT_COLOR
                else:
                    option_color = INCORRECT_COLOR

            self.draw_text(self.latin_font, self.meanings[option],
                           option_color, *DPAD_COORDS[key_code])

        if self.debug is not None:
            self.draw_text(self.latin_font, self.debug,
                           INCORRECT_COLOR, 0.5, 0.05)

        pygame.display.flip()

    def draw_text(self, font, text, color, wp, hp):

        x = self.screen.get_width() * wp
        y = self.screen.get_height() * hp
        text_surface = font.render(text, True, color)
        rect = text_surface.get_rect(center=(x, y))
        self.screen.blit(text_surface, rect)
