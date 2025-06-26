import pygame
import json
import quiz

pygame.init()

font_kanji = pygame.font.SysFont("notosansjp", 128)
font_latin = pygame.font.SysFont("consolas", 32)

with open("kanji.json", encoding='utf-8') as f:
    kanji_dict = json.load(f)

game = quiz.Game(640, 480, font_latin, font_kanji, kanji_dict)
game.press(0)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            else:
                game.press(event.key)

    pygame.time.Clock().tick(60)

pygame.quit()
