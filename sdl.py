import time
import ctypes
from pysdl import *
import quiz


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

while running:
    while SDL_PollEvent(ctypes.byref(event)) != 0:

        if event.type == SDL_KEYDOWN:
            print("KEYDOWN EVENT")
            code = event.key.keysym.scancode
            key = SCANCODE_MAP.get(code)
            print("- KEY", code, map)
            if key is None:
                running = False
                break
            else:
                game.press(key)
        elif event.type == SDL_KEYUP:
            print("KEYUP EVENT")
        elif event.type == SDL_QUIT:
            print("QUIT EVENT")
            running = False
            break
        else:
            print("OTHER EVENT", event.type)

    time.sleep(0.1)
    game.tick()

print("EXIT")
SDL_DestroyWindow(window)
SDL_Quit()
