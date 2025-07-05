import ctypes
from pysdl import *
import quiz


FONT_PATH = b"DejaVuSansMono.ttf"

KEY_CODES = {
    SDLK_LEFT: "LEFT",
    SDLK_RIGHT: "RIGHT",
    SDLK_UP: "UP",
    SDLK_DOWN: "DOWN",
    SDLK_a: "A",
    SDLK_b: "B",
    SDLK_x: "X",
    SDLK_y: "Y",
    SDLK_RETURN: "START",
}

FONT_CACHE = {}


SDL_Init(SDL_INIT_VIDEO)

window = SDL_CreateWindow(b"Kanji Quiz", 0, 0, 640, 480, SDL_WINDOW_SHOWN)
wsurf = SDL_GetWindowSurface(window)
ww = wsurf.contents.w
wh = wsurf.contents.h
wrect = SDL_Rect(0, 0, ww, wh)

ttf.TTF_Init()

font = ttf.TTF_OpenFont(FONT_PATH, 16)


def show_text(texts):

    SDL_FillRect(wsurf, wrect, 0)

    for font_size, text, color, wp, hp, align in texts:

        TTF_SetFontSize(font, font_size)
        fg = SDL_Color(*color)
        utf8_bytes = text.encode('utf-8')
        tsurf = TTF_RenderUTF8_Blended(font, utf8_bytes, fg)
        if not tsurf:
            print("ERROR:", text)
            continue
        tw = tsurf.contents.w
        th = tsurf.contents.h
        rx = (ww * wp) - (tw * align)
        ry = (wh * hp) - (th * 0.5)
        rect = SDL_Rect(int(rx), int(ry), tw, th)
        SDL_BlitSurface(tsurf, None, wsurf, rect)

    SDL_UpdateWindowSurface(window)


game = quiz.Game(show_text)

running = True
function_pressed = False
event = SDL_Event()

while running:
    while SDL_PollEvent(ctypes.byref(event)) != 0:

        if event.type == SDL_KEYDOWN:
            code = event.key.keysym.sym
            if code == SDLK_h:
                function_pressed = True
            elif function_pressed and code == SDLK_RETURN:
                running = False
            elif code == SDLK_ESCAPE:
                running = False
            else:
                key = KEY_CODES.get(code)
                if key is not None:
                    print(key)
                    game.press(key)

        elif event.type == SDL_KEYUP:
            if event.key.keysym.sym == SDLK_h:
                function_pressed = False

    SDL_Delay(100)
    game.tick()

SDL_DestroyWindow(window)
SDL_Quit()
