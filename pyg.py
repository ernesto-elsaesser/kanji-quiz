import pygame
import quiz


FONT_NAME = "DejaVuSansMono.ttf"

KEY_CODES = {
    pygame.K_LEFT: "LEFT",
    pygame.K_RIGHT: "RIGHT",
    pygame.K_UP: "UP",
    pygame.K_DOWN: "DOWN",
    pygame.K_a: "A",
    pygame.K_b: "B",
    pygame.K_x: "X",
    pygame.K_y: "Y",
    pygame.K_RETURN: "START",
}

FONT_CACHE = {}


pygame.init()

display = pygame.display.set_mode((640, 480))
w, h = display.get_size()


def show_text(texts):

    display.fill((0, 0, 0))

    for font_size, text, color, wp, hp, align in texts:

        font = FONT_CACHE.get(font_size)
        if font is None:
            font = pygame.font.Font(FONT_NAME, font_size)
            FONT_CACHE[font_size] = font

        text_surface = font.render(text, True, color)
        tw, th = text_surface.get_size()
        ry = (h * hp) - (th * 0.5)
        rx = (w * wp) - (tw * align)
        rect = pygame.Rect(rx, ry, tw, th)
        display.blit(text_surface, rect)

    pygame.display.flip()


game = quiz.Game(show_text)

running = True
function_pressed = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_h:
                function_pressed = True
            elif function_pressed and event.key == pygame.K_RETURN:
                running = False
            elif event.key == pygame.K_ESCAPE:
                running = False
            else:
                key = KEY_CODES.get(event.key)
                if key is not None:
                    game.press(key)

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_h:
                function_pressed = False

    pygame.time.Clock().tick(10)

pygame.quit()
