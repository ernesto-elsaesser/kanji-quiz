import sdl2
import sdl2.ext
import quiz


FONT_NAME = "DejaVuSansMono.ttf"

KEY_CODES = {
    sdl2.SDLK_LEFT: "LEFT",
    sdl2.SDLK_RIGHT: "RIGHT",
    sdl2.SDLK_UP: "UP",
    sdl2.SDLK_DOWN: "DOWN",
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
        self.font_cache = {}

    def clear(self):

        sdl2.ext.fill(self.surface, sdl2.ext.Color(0, 0, 0))

    def text(self, font_size, text, color, wp, hp, anchor=None):

        font = self.font_cache.get(font_size)
        if font is None:
            font = sdl2.ext.ttf.FontTTF(FONT_NAME, font_size, color)
            self.font_cache[font_size] = font

        text_surface = font.render_text(text)

        if anchor == "l":
            hf = 0.0
        elif anchor == "r":
            hf = 1.0
        else:
            hf = 0.5

        ry = (self.height * hp) - (text_surface.h * hf)
        rx = (self.width * wp) - (text_surface.w * 0.5)
        rect = sdl2.rect.SDL_Rect(rx, ry, text_surface.w, text_surface.h)
        sdl2.SDL_BlitSurface(text_surface, rect, self.surface, None)

    def show(self):

        self.window.refresh()

    def delay(self):

        sdl2.SDL_Delay(100)


sdl2.ext.init()

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

    game.tick()

sdl2.ext.quit()
