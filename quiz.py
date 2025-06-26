import csv
import random
import pygame


KANJI_CSV = "kanjis.csv"
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

    def __init__(self, width, height, latin_font, kanji_font):

        self.screen = pygame.display.set_mode((width, height))

        self.latin_font = latin_font
        self.kanji_font = kanji_font

        self.labels = {
            "1": "GRADE 1",
            "2": "GRADE 2",
            "3": "GRADE 3",
            "4": "GRADE 4",
        }

        self.options = ["1", "2", "3", "4"]
        self.grade = None
        self.correct = None
        self.selected = None
        self.debug = None

        self.draw()

    def press(self, key_code):

        # self.debug = str(key_code)

        if self.grade is None:
            if key_code not in DPAD_COORDS:
                return

            index = list(DPAD_COORDS).index(key_code)
            self.grade = self.options[index]

            self.labels = {}
            with open(KANJI_CSV, encoding='utf-8') as f:
                reader = csv.reader(f)
                next(reader)
                for index, kanji, kanji_old, radical, strokes, grade, year, meanings, on, kun, frequency, jlpt in reader:
                    if grade == self.grade:
                        self.labels[kanji] = meanings.upper()

            self.options = random.sample(list(self.labels), 4)
            self.correct = random.choice(self.options)

        elif self.selected is None:
            if key_code not in DPAD_COORDS:
                return
            self.selected = key_code

        else:
            self.options = random.sample(list(self.labels), 4)
            self.correct = random.choice(self.options)
            self.selected = None

        self.draw()

    def draw(self):

        self.screen.fill(BACKGROUND_COLOR)

        self.draw_text(self.kanji_font, self.correct, TEXT_COLOR, 0.5, 0.25)

        for key_code, option in zip(DPAD_COORDS, self.options):
            option_color = TEXT_COLOR
            if self.selected is not None:
                if option == self.correct:
                    option_color = CORRECT_COLOR
                elif key_code == self.selected:
                    option_color = INCORRECT_COLOR

            self.draw_text(self.latin_font, self.labels[option],
                           option_color, *DPAD_COORDS[key_code])

        if self.debug is not None:
            self.draw_text(self.latin_font, self.debug,
                           INCORRECT_COLOR, 0.95, 0.05)

        pygame.display.flip()

    def draw_text(self, font, text, color, wp, hp):

        x = self.screen.get_width() * wp
        y = self.screen.get_height() * hp
        text_surface = font.render(text, True, color)
        rect = text_surface.get_rect(center=(x, y))
        self.screen.blit(text_surface, rect)
