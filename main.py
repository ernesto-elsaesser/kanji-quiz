import sys
import pygame
import quiz


font_name = "dejavusansmono"
font_name_jp = "notosansjp"

if len(sys.argv) == 3:
    font_name = sys.argv[1]
    font_name_jp = sys.argv[2]

sets = {f"GRADE {i}": f"grade{i}.json" for i in range(1, 7)}

pygame.init()

game = quiz.Game(640, 480, font_name, font_name_jp, sets)
game.run()

pygame.quit()
