import json
import random
import pygame


BLACK = (0, 0, 0)
WHITE = (200, 200, 200)
DIM_WHITE = (150, 150, 150)
RED = (255, 0, 0)
GREEN = (0, 255, 0)


class Game:

    def __init__(self, width, height, font_name, font_name_jp, sets):

        self.screen = pygame.display.set_mode((width, height))

        self.menu_font = pygame.font.SysFont(font_name, 60)
        self.meaning_font = pygame.font.SysFont(font_name, 35)
        self.kanji_font = pygame.font.SysFont(font_name_jp, 135)
        self.kana_font = pygame.font.SysFont(font_name_jp, 28)
        self.pinyin_font = pygame.font.SysFont(font_name, 28)

        self.set_files = sets
        self.set_names = list(sets)

        self.set_index = 0
        self.kanji_dict = {}
        self.questions = None
        self.selected = None
        self.frames_to_next = None
        self.function_pressed = False

        self.draw()

    def run(self):

        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_h:
                        self.function_pressed = True
                    elif event.key == pygame.K_RETURN:
                        if self.function_pressed:
                            self.draw_end()
                            return
                    elif event.key == pygame.K_ESCAPE:
                        return

                    if self.questions is None:

                        if event.key == pygame.K_LEFT:
                            if self.set_index > 0:
                                self.set_index -= 1
                        elif event.key == pygame.K_RIGHT:
                            if self.set_index < len(self.set_names) - 1:
                                self.set_index += 1
                        elif event.key == pygame.K_RETURN:
                            self.load_set()

                    else:

                        correct = self.questions[0][1]

                        if event.key in {pygame.K_x, pygame.K_UP}:
                            self.selected = 2
                        if event.key in {pygame.K_y, pygame.K_LEFT}:
                            self.selected = 1
                        if event.key in {pygame.K_a, pygame.K_RIGHT}:
                            self.selected = 0
                        if event.key in {pygame.K_b, pygame.K_DOWN}:
                            self.selected = 3
                        if event.key == pygame.K_RETURN:
                            self.questions = None

                        if self.selected == correct:
                            self.frames_to_next = 4

                    self.draw()

                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_h:
                        self.function_pressed = False

            if self.frames_to_next is not None:
                if self.frames_to_next == 0:
                    self.frames_to_next = None
                    self.selected = None
                    assert self.questions is not None
                    self.questions.pop(0)
                    if len(self.questions) == 0:
                        self.questions = None
                    self.draw()
                else:
                    self.frames_to_next -= 1

            pygame.time.Clock().tick(10)

    def load_set(self):

        set_file = self.set_files[self.set_names[self.set_index]]
        with open(set_file, encoding="utf-8") as f:
            self.kanji_dict = json.load(f)

        kanjis = list(self.kanji_dict)
        random.shuffle(kanjis)

        self.questions = []
        for kanji in kanjis:
            answers = [kanji]
            while len(answers) < 4:
                decoy = random.choice(kanjis)
                if decoy not in answers:
                    answers.append(decoy)
            random.shuffle(answers)
            lengths = {k: len(self.kanji_dict[k]["meaning"]) for k in answers}
            answers = sorted(answers, key=lengths.__getitem__)
            correct = answers.index(kanji)
            self.questions.append((answers, correct))

    def draw(self):

        self.screen.fill(BLACK)

        if self.questions is None:

            set_name = "< " + self.set_names[self.set_index] + " >"
            self.draw_text(self.menu_font, set_name, WHITE, 0.5, 0.5)

        else:

            answers, correct = self.questions[0]

            correct_kanji = answers[correct]
            self.draw_text(self.kanji_font, correct_kanji, WHITE, 0.2, 0.25)

            info = self.kanji_dict[correct_kanji]
            on = "、".join(info["ons"][:3])
            kun = "、".join(info["kuns"][:3])
            pinyin = ", ".join(info["pinyins"][:3])

            self.draw_text(self.pinyin_font, pinyin, DIM_WHITE, 0.4, 0.15, "l")
            self.draw_text(self.kana_font, on, WHITE, 0.4, 0.25, "l")
            self.draw_text(self.kana_font, kun, WHITE, 0.4, 0.35, "l")

            self.draw_text(self.meaning_font, "+", WHITE, 0.5, 0.7)

            answer_coords = [
                (0.57, 0.7, "l"),
                (0.43, 0.7, "r"),
                (0.5, 0.55),
                (0.5, 0.85),
            ]

            for i, option_kanji in enumerate(answers):
                info = self.kanji_dict[option_kanji]
                meaning = info["meaning"].upper()
                color = WHITE
                if i == self.selected:
                    if i == correct:
                        color = GREEN
                    else:
                        color = RED
                self.draw_text(self.meaning_font, meaning,
                               color, *answer_coords[i])

        pygame.display.flip()

    def draw_end(self):

        self.screen.fill(BLACK)
        self.draw_text(self.menu_font, "BYE", WHITE, 0.5, 0.5)
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
