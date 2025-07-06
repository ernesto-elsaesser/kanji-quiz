import time
import ctypes
from pysdl import *
from pysdl.sdlttf import *
import quiz


VERSION = 8
FONT_PATH = b"DejaVuSansMono.ttf"

SCANCODE_MAP = {
    SDL_SCANCODE_LEFT: "LEFT",
    SDL_SCANCODE_RIGHT: "RIGHT",
    SDL_SCANCODE_UP: "UP",
    SDL_SCANCODE_DOWN: "DOWN",
    SDL_SCANCODE_A: "A",
    SDL_SCANCODE_B: "B",
    SDL_SCANCODE_X: "X",
    SDL_SCANCODE_Y: "Y",
    SDL_SCANCODE_RETURN: "START",
}


SDL_Init(SDL_INIT_VIDEO | SDL_INIT_JOYSTICK)

window = SDL_CreateWindow(b"Kanji Quiz", 0, 0, 640, 480, SDL_WINDOW_SHOWN)
wsurf = SDL_GetWindowSurface(window)
ww = wsurf.contents.w
wh = wsurf.contents.h
wrect = SDL_Rect(0, 0, ww, wh)

TTF_Init()

font = TTF_OpenFont(FONT_PATH, 16)


def show_text(texts):

    SDL_FillRect(wsurf, wrect, 0)

    for font_size, text, color, wp, hp, align in texts:

        TTF_SetFontSize(font, font_size)
        fg = SDL_Color(*color)
        utf8_bytes = text.encode('utf-8')
        tsurf = TTF_RenderUTF8_Blended(font, utf8_bytes, fg)
        tw = tsurf.contents.w
        th = tsurf.contents.h
        rx = (ww * wp) - (tw * align)
        ry = (wh * hp) - (th * 0.5)
        rect = SDL_Rect(int(rx), int(ry), tw, th)
        SDL_BlitSurface(tsurf, None, wsurf, rect)

    SDL_UpdateWindowSurface(window)


game = quiz.Game(show_text)

running = True
event = SDL_Event()

print("START", VERSION)

while running:
    while SDL_PollEvent(ctypes.byref(event)) != 0:

        if event.type == SDL_KEYDOWN:
            print("KEYDOWN EVENT")
            code = event.key.keysym.scancode
            key = SCANCODE_MAP.get(code)
            print("- KEY", code, key)
            if key is None:
                running = False
                break
            else:
                game.press(key)
        elif event.type == SDL_KEYUP:
            print("KEYUP EVENT")
        elif event.type == SDL_WINDOWEVENT:
            print("WINDOW EVENT", event.window.event)
        elif event.type == SDL_QUIT:
            print("QUIT EVENT")
            running = False
            break
        else:
            print("OTHER EVENT", event.type)

    SDL_Delay(100)
    game.tick()

print("EXIT")
SDL_DestroyWindow(window)
SDL_Quit()
