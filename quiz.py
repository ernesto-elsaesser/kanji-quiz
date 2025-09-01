import random

import jlpt
import jukugo


KANJI_FONT_SIZE = 32
WHITE = (200, 200, 200)

SUBSETS = [
    ("JLPT N5", ["N5"]),
    ("JLPT N4", ["N4", "N5"]),
    ("JLPT N3", ["N3", "N4", "N5"]),
    ("JLPT N2", ["N2", "N3", "N4"]),
    ("JLPT N1", ["N1", "N2", "N3"]),
]


class Game:

    def __init__(self, show_text):

        self.show_text = show_text
        self.set_index = 0
        self.vocab = {}
        self.decoys = ""
        self.word = None
        self.left_options = []
        self.right_options = []
        self.left_pick = None
        self.right_pick = None
        self.resolve = False

        self.draw()

    def press(self, key):

        if self.word is None:

            if key == "LEFT":
                self.set_index -= 1
            elif key == "RIGHT":
                self.set_index += 1
            elif key == "START":
                self.load_set()
                self.next_question()

            self.set_index %= len(SUBSETS)
        else:

            if key == "UP":
                self.left_pick = 2
            if key == "LEFT":
                self.left_pick = 1
            if key == "RIGHT":
                self.left_pick = 0
            if key == "DOWN":
                self.left_pick = 3
            if key == "X":
                self.right_pick = 2
            if key == "Y":
                self.right_pick = 1
            if key == "A":
                self.right_pick = 0
            if key == "B":
                self.right_pick = 3
            if key == "START":
                self.word = None

            if self.left_pick is not None and self.right_pick is not None:
                self.resolve = True

        self.draw()

    def load_set(self):

        levels = SUBSETS[self.set_index][1]
        self.vocab = {}
        self.decoys = ""
        for level in levels:
            self.vocab.update(jukugo.WORDS[level])
            self.decoys += jlpt.KANJIS[level]

    def next_question(self):

        words = list(self.vocab)

        self.word = random.choice(words)
        self.left_pick = None
        self.right_pick = None

        # TODO: prevent duplicates
        self.left_options = [self.word[0]] + random.sample(self.decoys, 3)
        self.right_options = [self.word[1]] + random.sample(self.decoys, 3)
        random.shuffle(self.left_options)
        random.shuffle(self.right_options)

        self.draw()

    def draw(self):

        texts = []

        if self.word is None:

            set_name = "< " + SUBSETS[self.set_index][0] + " >"
            texts.append((50, set_name, WHITE, 0.5, 0.5, 0.5))

        else:

            reading, *meanings = self.vocab[self.word]

            texts.append((20, meanings[0], WHITE, 0.5, 0.15, 0.5))

            if self.resolve:
                texts.append((20, reading, WHITE, 0.5, 0.72, 0.5))
                texts.append((40, self.word, WHITE, 0.5, 0.85, 0.5))

            left_kanji, right_kanji = self.word

            left_cross = [
                (0.3, 0.5, 0.5),
                (0.1, 0.5, 0.5),
                (0.2, 0.35, 0.5),
                (0.2, 0.65, 0.5),
            ]

            right_cross = [
                (0.9, 0.5, 0.5),
                (0.7, 0.5, 0.5),
                (0.8, 0.35, 0.5),
                (0.8, 0.65, 0.5),
            ]

            texts.append((KANJI_FONT_SIZE, "+", WHITE, 0.2, 0.5, 0.5))
            for i, kanji in enumerate(self.left_options):
                color = self.get_color(kanji == left_kanji, i == self.left_pick)
                texts.append((KANJI_FONT_SIZE, kanji, color, *left_cross[i]))
            
            texts.append((KANJI_FONT_SIZE, "+", WHITE, 0.8, 0.5, 0.5))
            for i, kanji in enumerate(self.right_options):
                color = self.get_color(kanji == right_kanji, i == self.right_pick)
                texts.append((KANJI_FONT_SIZE, kanji, color, *right_cross[i]))

        self.show_text(texts)

    def get_color(self, correct, picked):

        if picked:
            if self.resolve:
                if correct:
                    return (0, 255, 0)
                else:
                    return (255, 0, 0)
            else:
                return (128, 128, 255)
        elif self.resolve and correct:
            return (0, 255, 0)
        else:
            return WHITE
