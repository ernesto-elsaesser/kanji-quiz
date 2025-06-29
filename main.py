import os
import pygame
import quiz


LATIN_FONTS = ["dejavusansmono", "consolas", "sfnsmono", "dejavusans"]
KANJI_FONTS = ["notosansjp", "hiraginosansgb"]

pygame.init()

installed_fonts = pygame.font.get_fonts()
font_name = [n for n in LATIN_FONTS if n in installed_fonts][0]
font_name_jp = [n for n in KANJI_FONTS if n in installed_fonts][0]

kanji_sets = {n[:-5]: "sets/" + n for n in sorted(os.listdir("sets"))}

game = quiz.Game(640, 480, font_name, font_name_jp, kanji_sets)
game.run()

pygame.quit()
