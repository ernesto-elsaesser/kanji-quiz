import os
import pygame
import quiz


LATIN_FONTS = ["dejavusansmono", "consolas", "sfnsmono", "dejavusans"]
JAPANESE_FONTS = ["notosansjp", "hiraginosansgb"]

kanji_sets = {n[:-5]: "sets/" + n for n in sorted(os.listdir("sets"))}

pygame.init()

game = quiz.Game(640, 480, LATIN_FONTS, JAPANESE_FONTS, kanji_sets)
game.run()

pygame.quit()
