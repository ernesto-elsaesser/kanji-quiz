import ctypes
from sdl2 import *
import sdl2.sdlttf
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
wrect = SDL_Rect(0, 0, wsurf.w, wsurf.h)

sdl2.sdlttf.TTF_Init()

font = sdl2.sdlttf.TTF_OpenFont(FONT_PATH, 16)


def show_text(texts):

    SDL_FillRect(wsurf, wrect, 0)

    for font_size, text, color, wp, hp, align in texts:

        sdl2.sdlttf.TTF_SetFontSize(font, font_size)
        fg = SDL_MapRGB(color)
        tsurf = sdl2.sdlttf.TTF_RenderUTF8_Blended(font, text, fg)

        tw = tsurf.w
        th = tsurf.h
        ry = (wsurf.h * hp) - (th * 0.5)
        rx = (wsurf.w * wp) - (tw * align)
        rect = SDL_Rect(rx, ry, tw, th)
        SDL_BlitSurface(tsurf, rect, wsurf, None)

    SDL_UpdateWindowSurface(window)


game = quiz.Game(show_text)

running = True
function_pressed = False
event = SDL_Event()

while running:
    while SDL_PollEvent(ctypes.byref(event)) != 0:
        if event.type == SDL_KEYDOWN:

            if event.key == SDLK_h:
                function_pressed = True
            elif function_pressed and event.key == SDLK_RETURN:
                running = False
            elif event.key == SDLK_ESCAPE:
                running = False
            else:
                key = KEY_CODES.get(event.key)
                if key is not None:
                    game.press(key)

        elif event.type == SDL_KEYUP:
            if event.key == SDLK_h:
                function_pressed = False

    SDL_Delay(100)
    game.tick()

SDL_DestroyWindow(window)
SDL_Quit()
