import sdl2
import sdl2.ext
import sdl2.sdlttf
import quiz


# TODO
FONT_FILE_LATIN = "dejavusansmono"
FONT_FILE_JAPANESE = "notosansjp"

KEY_CODES = {
    sdl2.SDLK_LEFT: "LEFT",
    sdl2.SDLK_RIGHT: "RIGHT",
    sdl2.SDLK_UP: "UP",
    sdl2.SDLK_DOWN: "K_DOWN",
    sdl2.SDLK_a: "A",
    sdl2.SDLK_b: "B",
    sdl2.SDLK_x: "X",
    sdl2.SDLK_y: "Y",
    sdl2.SDLK_RETURN: "START",
}


class Screen(quiz.Screen):

    def __init__(self, width, height):

        super().__init__(width, height)

        self.window = sdl2.ext.Window("Kanji Quiz", size=(width, height))
        self.window.show()

        self.surface = self.window.get_surface()

        default_font = sdl2.sdlttf.TTF_OpenFont(FONT_FILE_LATIN, 65)

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

        sdl2.ext.fill(self.surface, sdl2.ext.Color(0, 0, 0))

    def text(self, font_name, font_size, text, color, wp, hp, anchor=None):

        font_args = font_name, font_size
        font = self.font_cache.get(font_args)
        if font is None:
            pt_size = sdl2.sdlttf.TTF_GlyphMetrics(
                font, ch, minx, maxx, miny, maxy, advance)
            font = sdl2.sdlttf.TTF_OpenFont(FONT_FILE_LATIN, pt_size)
            self.font_cache[font_args] = font

        sdl_color = sdl2.ext.Color(*color)
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

        self.window.refresh()

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


sdl2.ext.init()
sdl2.sdlttf.TTF_Init()

screen = Screen(640, 480)
game = quiz.Game(screen)

running = True
function_pressed = False

while running:
    for event in sdl2.ext.get_events():
        if event.type == sdl2.SDL_KEYDOWN:

            if event.key == sdl2.SDLK_h:
                function_pressed = True
            elif function_pressed and event.key == sdl2.SDLK_RETURN:
                running = False
            elif event.key == sdl2.SDLK_ESCAPE:
                running = False
            else:
                key = KEY_CODES.get(event.key)
                if key is not None:
                    game.press(key)

        elif event.type == sdl2.SDL_KEYUP:
            if event.key == sdl2.SDLK_h:
                function_pressed = False

    screen.tick()

sdl2.ext.quit()
sdl2.sdlttf.TTF_Quit()
