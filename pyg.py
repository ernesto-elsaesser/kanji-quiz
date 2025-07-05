import pygame
import quiz


LATIN_FONTS = ["dejavusansmono", "consolas", "sfnsmono", "dejavusans"]
JAPANESE_FONTS = ["notosansjp", "hiraginosansgb"]

KEY_CODES = {
    pygame.K_LEFT: "LEFT",
    pygame.K_RIGHT: "RIGHT",
    pygame.K_UP: "UP",
    pygame.K_DOWN: "K_DOWN",
    pygame.K_a: "A",
    pygame.K_b: "B",
    pygame.K_x: "X",
    pygame.K_y: "Y",
    pygame.K_RETURN: "START",
}


class Screen(quiz.Screen):

    def __init__(self, width, height):

        super().__init__(width, height)

        self.display = pygame.display.set_mode((width, height))

        default_font = pygame.font.SysFont(None, 65)

        self.clear()
        self.text(default_font, "HI", (255, 255, 255), 0.5, 0.5)
        self.show()

        font_names = pygame.font.get_fonts()
        self.font_name = [n for n in LATIN_FONTS if n in font_names][0]
        self.font_name_jp = [n for n in JAPANESE_FONTS if n in font_names][0]
        self.font_cache = {}

        self.frames_to_callback = None
        self.callback = None

    def clear(self):

        self.display.fill((0, 0, 0))

    def latin(self, font_size, text, color, wp, hp, anchor=None):

        args = self.font_name, font_size
        font = self.font_cache.get(args)
        if font is None:
            font = pygame.font.SysFont(*args)
            self.font_cache[args] = font

        self.text(font, text, color, wp, hp, anchor)

    def japanese(self, font_size, text, color, wp, hp, anchor=None):

        args = self.font_name_jp, font_size
        font = self.font_cache.get(args)
        if font is None:
            font = pygame.font.SysFont(*args)
            self.font_cache[args] = font

        self.text(font, text, color, wp, hp, anchor)

    def text(self, font, text, color, wp, hp, anchor=None):

        x = self.width * wp
        y = self.height * hp
        text_surface = font.render(text, True, color)
        if anchor == "l":
            rect = text_surface.get_rect(midleft=(x, y))
        elif anchor == "r":
            rect = text_surface.get_rect(midright=(x, y))
        else:
            rect = text_surface.get_rect(center=(x, y))
        self.display.blit(text_surface, rect)

    def show(self):

        pygame.display.flip()

    def defer(self, callback, frames):

        self.frames_to_callback = frames
        self.callback = callback

    def tick(self):

        pygame.time.Clock().tick(10)

        if self.frames_to_callback is None:
            return

        if self.frames_to_callback == 0:
            screen.frames_to_callback = None
            if self.callback is not None:
                self.callback()
                self.callback = None
        else:
            self.frames_to_callback -= 1


pygame.init()

screen = Screen(640, 480)
game = quiz.Game(screen)

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

    screen.tick()

pygame.quit()
