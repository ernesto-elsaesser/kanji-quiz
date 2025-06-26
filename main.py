import pygame
import quiz


pygame.init()

installed_fonts = pygame.font.get_fonts()

if "consolas" in installed_fonts:
    latin_font = pygame.font.SysFont("consolas", 32)
else:
    latin_font = pygame.font.SysFont("dejavusansmono", 36)

kanji_font = pygame.font.SysFont("notosansjp", 128)

game = quiz.Game(640, 480, latin_font, kanji_font)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_ESCAPE, 104):  # MENU
                running = False
            else:
                game.press(event.key)

    pygame.time.Clock().tick(60)

pygame.quit()
