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
        self.kanjis = {}
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
                self.next_round()

            self.set_index %= len(SUBSETS)

        else:

            if key == "START":
                self.word = None
            elif self.resolve:
                self.next_round()
            elif key == "UP":
                self.left_pick = 2
            elif key == "LEFT":
                self.left_pick = 1
            elif key == "RIGHT":
                self.left_pick = 0
            elif key == "DOWN":
                self.left_pick = 3
            elif key == "X":
                self.right_pick = 2
            elif key == "Y":
                self.right_pick = 1
            elif key == "A":
                self.right_pick = 0
            elif key == "B":
                self.right_pick = 3

            if self.left_pick is not None and self.right_pick is not None:
                self.resolve = True

        self.draw()

    def load_set(self):

        levels = SUBSETS[self.set_index][1]
        self.vocab = {}
        self.kanjis = {}
        for level in levels:
            self.vocab.update(jukugo.WORDS[level])
            self.kanjis.update(jlpt.KANJIS[level])

    def next_round(self):

        words = list(self.vocab)

        self.word = random.choice(words)
        self.left_pick = None
        self.right_pick = None
        self.resolve = False

        others = [k for k in self.kanjis if k not in self.word]
        decoys = random.sample(others, 6)
        self.left_options = [self.word[0]] + decoys[:3]
        self.right_options = [self.word[1]] + decoys[3:]
        random.shuffle(self.left_options)
        random.shuffle(self.right_options)

        self.draw()

    def draw(self):

        texts = []

        if self.word is None:

            set_name = "< " + SUBSETS[self.set_index][0] + " >"
            texts.append((50, set_name, WHITE, 0.5, 0.5, 0.5))

        else:

            reading, *translations = self.vocab[self.word]

            lines = translations[0].split(" (")
            if len(lines) > 1:
                texts.append((22, lines[0], WHITE, 0.5, 0.1, 0.5))
                texts.append((18, "(" + lines[1], WHITE, 0.5, 0.18, 0.5))
            else:
                texts.append((22, lines[0], WHITE, 0.5, 0.15, 0.5))

            if self.resolve:
                texts.append((20, reading, WHITE, 0.5, 0.72, 0.5))
                texts.append((40, self.word, WHITE, 0.5, 0.85, 0.5))
                for i, wp in enumerate((0.2, 0.8)):
                    meanings = self.kanjis[self.word[i]]
                    font_size = 16 if len(meanings) > 12 else 20
                    texts.append((font_size, meanings, WHITE, wp, 0.85, 0.5))

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
                return (255, 255, 0)
        elif self.resolve and correct:
            return (0, 255, 0)
        else:
            return WHITE
