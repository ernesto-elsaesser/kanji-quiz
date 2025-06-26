import json
import random
import pygame


SET_NAMES = [
    "GRADE 1",
    "GRADE 2",
]

SET_FILES = [
    "grade1.json",
    "grade2.json",
]

BLACK = (0, 0, 0)
WHITE = (200, 200, 200)
RED = (255, 0, 0)

ANSWER_KEYS = [
    pygame.K_UP,
    pygame.K_LEFT,
    pygame.K_RIGHT,
    pygame.K_DOWN
]

ANSWER_COORDS = [
    (0.5, 0.55),
    (0.45, 0.7, "r"),
    (0.55, 0.7, "l"),
    (0.5, 0.85)
]

END_KEYS = {
    pygame.K_h,  # MENU
    pygame.K_l,  # L1
    pygame.K_r,  # L2
}


class Game:

    def __init__(self, width, height, font_name, font_name_jp):

        self.screen = pygame.display.set_mode((width, height))

        self.latin_font = pygame.font.SysFont(font_name, 32)
        self.kanji_font = pygame.font.SysFont(font_name_jp, 128)
        self.kana_font = pygame.font.SysFont(font_name_jp, 24)

        self.set_index = 0
        self.kanji_dict = {}
        self.options = []
        self.correct = -1
        self.miss = -1

        self.bad_keys = set()

        self.draw_menu()

    def press(self, key_code):

        if len(self.kanji_dict) == 0:

            if key_code == pygame.K_LEFT:
                if self.set_index > 0:
                    self.set_index -= 1
                self.draw_menu()
            elif key_code == pygame.K_RIGHT:
                if self.set_index < len(SET_FILES) - 1:
                    self.set_index += 1
                self.draw_menu()
            elif key_code == pygame.K_DOWN:
                with open(SET_FILES[self.set_index], encoding="utf-8") as f:
                    self.kanji_dict = json.load(f)
                self.next_question()
                self.draw_quiz()

        else:

            try:
                index = ANSWER_KEYS.index(key_code)
                self.bad_keys = set()
                if index == self.correct:
                    self.next_question()
                else:
                    self.miss = index
                self.draw_quiz()

            except ValueError:
                self.bad_keys.add(key_code)
                if self.bad_keys == END_KEYS:
                    self.draw_end()
                    return False

        return True

    def next_question(self):

        self.options = random.sample(list(self.kanji_dict), 4)
        self.correct = random.randrange(4)
        self.miss = -1

    def draw_menu(self):

        self.screen.fill(BLACK)

        name = SET_NAMES[self.set_index]
        self.draw_text(self.latin_font, name, WHITE, 0.5, 0.5)

        pygame.display.flip()

    def draw_quiz(self):

        self.screen.fill(BLACK)

        correct_kanji = self.options[self.correct]
        self.draw_text(self.kanji_font, correct_kanji, WHITE, 0.2, 0.25)

        _, on, kun = self.kanji_dict[correct_kanji]
        self.draw_text(self.kana_font, on, WHITE, 0.4, 0.2, "l")
        self.draw_text(self.kana_font, kun, WHITE, 0.4, 0.3, "l")

        for i, option_kanji in enumerate(self.options):
            meaning = self.kanji_dict[option_kanji][0]
            color = RED if i == self.miss else WHITE
            self.draw_text(self.latin_font, meaning, color, *ANSWER_COORDS[i])

        pygame.display.flip()

    def draw_end(self):

        self.screen.fill(BLACK)

        self.draw_text(self.latin_font, "EXIT", RED, 0.5, 0.5)

        pygame.display.flip()

    def draw_text(self, font, text, color, wp, hp, anchor=None):

        x = self.screen.get_width() * wp
        y = self.screen.get_height() * hp
        text_surface = font.render(text, True, color)
        if anchor == "l":
            rect = text_surface.get_rect(midleft=(x, y))
        elif anchor == "r":
            rect = text_surface.get_rect(midright=(x, y))
        else:
            rect = text_surface.get_rect(center=(x, y))
        self.screen.blit(text_surface, rect)
