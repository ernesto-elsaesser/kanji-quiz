import os
import json
import random
import sets


WHITE = (200, 200, 200)
DIM_WHITE = (150, 150, 150)
RED = (255, 0, 0)
GREEN = (0, 255, 0)


class Game:

    def __init__(self, show_text):

        self.show_text = show_text
        self.set_names = list(sets.SETS)
        self.set_index = 0
        self.kanji_dict = {}
        self.questions = None
        self.selected = None
        self.frames_to_next = None

        self.draw()

    def press(self, key):

        if self.questions is None:

            if key == "LEFT":
                self.set_index -= 1
            elif key == "RIGHT":
                self.set_index += 1
            elif key == "START":
                self.load_set()

            self.set_index %= len(self.set_names)
        else:

            correct = self.questions[0][1]

            if key in {"X", "UP"}:
                self.selected = 2
            if key in {"Y", "LEFT"}:
                self.selected = 1
            if key in {"A", "RIGHT"}:
                self.selected = 0
            if key in {"B", "DOWN"}:
                self.selected = 3
            if key == "START":
                self.questions = None

            if self.selected == correct:
                self.frames_to_next = 4

        self.draw()

    def tick(self):

        if self.frames_to_next is not None:
            if self.frames_to_next == 0:
                self.frames_to_next = None
                self.next_question()
            else:
                self.frames_to_next -= 1

    def next_question(self):

        self.selected = None

        if self.questions is not None:
            self.questions.pop(0)
            if len(self.questions) == 0:
                self.questions = None

        self.draw()

    def load_set(self):

        self.kanji_dict = sets.SETS[self.set_names[self.set_index]]

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

        texts = []

        if self.questions is None:

            set_name = "< " + self.set_names[self.set_index] + " >"
            texts.append((50, set_name, WHITE, 0.5, 0.5, 0.5))

        else:

            answers, correct = self.questions[0]

            correct_kanji = answers[correct]
            texts.append((120, correct_kanji, WHITE, 0.2, 0.25, 0.5))

            info = self.kanji_dict[correct_kanji]

            if len(info["pinyins"]):
                pinyin = ", ".join(info["pinyins"][:3])
                texts.append((22, pinyin, DIM_WHITE, 0.4, 0.15, 0.0))

            if len(info["ons"]):
                on = "、".join(info["ons"][:3])
                texts.append((22, on, WHITE, 0.4, 0.25, 0.0))

            if len(info["kuns"]):
                kun = "、".join(info["kuns"][:3])
                texts.append((22, kun, WHITE, 0.4, 0.35, 0.0))

            texts.append((28, "+", WHITE, 0.5, 0.7, 0.5))

            answer_coords = [
                (0.57, 0.7, 0.0),
                (0.43, 0.7, 1.0),
                (0.5, 0.55, 0.5),
                (0.5, 0.85, 0.5),
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
                texts.append((28, meaning, color, *answer_coords[i]))

        self.show_text(texts)
