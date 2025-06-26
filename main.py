import pygame
import quiz


pygame.init()

installed_fonts = pygame.font.get_fonts()
font_name = "consolas" if "consolas" in installed_fonts else "dejavusansmono"
font_name_jp = "notosansjp"

game = quiz.Game(640, 480, font_name, font_name_jp)

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
