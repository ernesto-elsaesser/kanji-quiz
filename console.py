import pygame
import json
import quiz


FONT_SIZE_KANJI = 128
FONT_SIZE_LATIN = 32


def log(msg):
    print(msg)
    # with open("log.txt", "a") as f:
    #     f.write(msg + "\n")


log("start")

pygame.init()

log("initialzed")


try:
    available_fonts = pygame.font.get_fonts()

    for font_name in available_fonts:
        log("sys font: " + font_name)

    fallback_font_name = pygame.font.get_default_font()
    log("default font: " + fallback_font_name)
except:
    fallback_font_name = "dejavusans"

try:
    font_kanji = pygame.font.Font(
        "/usr/share/fonts/truetype/NotoSansJP-VF.ttf", FONT_SIZE_KANJI)
    log("noto kanji font")
except:
    font_kanji = pygame.font.SysFont(fallback_font_name, FONT_SIZE_KANJI)
    log("fallback kanji font")

try:
    font_latin = pygame.font.SysFont("dejavusansmono", FONT_SIZE_LATIN)
    log("mono latin font")
except:
    font_latin = pygame.font.SysFont(fallback_font_name, FONT_SIZE_LATIN)
    log("fallback latin font")

with open("kanji.json", encoding='utf-8') as f:
    kanji_dict = json.load(f)

log("loaded kanjis")

game = quiz.Game(640, 480, font_latin, font_kanji, kanji_dict)
game.press(0)

log("game loop")

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == 104:  # MENU
                running = False
            else:
                game.press(event.key)

    pygame.time.Clock().tick(60)

log("end")

pygame.quit()
