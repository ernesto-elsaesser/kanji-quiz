import pygame
import quiz


LATIN_FONTS = ["dejavusansmono", "consolas", "sfnsmono", "dejavusans"]
KANJI_FONTS = ["notosansjp", "hiraginosansgb"]

KANJI_SETS = {
    "GRADE 1": "grade1.json",
    "GRADE 2": "grade2.json",
    "GRADE 3": "grade3.json",
    "GRADE 4": "grade4.json",
    "GRADE 5": "grade5.json",
    "GRADE 6": "grade6.json",
}

pygame.init()

installed_fonts = pygame.font.get_fonts()
font_name = [n for n in LATIN_FONTS if n in installed_fonts][0]
font_name_jp = [n for n in KANJI_FONTS if n in installed_fonts][0]

game = quiz.Game(640, 480, font_name, font_name_jp, KANJI_SETS)
game.run()

pygame.quit()
