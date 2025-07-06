import ctypes
from pysdl import *
from pysdl.sdlttf import *
import quiz


VERSION = 10
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

JHAT_MAP = {
    SDL_HAT_LEFT: "LEFT",
    SDL_HAT_RIGHT: "RIGHT",
    SDL_HAT_UP: "UP",
    SDL_HAT_DOWN: "DOWN",
}

JBUTTON_MAP = {
    0: "A",
    1: "B",
    2: "X",
    3: "Y",
    7: "START",
    # 6: SELECT
    # 8: MENU
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
        if not tsurf:
            err = SDL_GetError()
            print("FONT RENDER ERROR", text, font_size, err)
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
event = SDL_Event()
jstick = None

print("START", VERSION)

while running:
    while SDL_PollEvent(ctypes.byref(event)) != 0:

        if event.type == SDL_KEYDOWN:
            print("KEYDOWN EVENT")
            code = event.key.keysym.scancode
            if code in (SDL_SCANCODE_POWER, SDL_SCANCODE_ESCAPE):
                print("- ESCAPE")
                running = False
                break
            key = SCANCODE_MAP.get(code)
            print("- KEY", code, key)
            if key is not None:
                game.press(key)
        elif event.type == SDL_KEYUP:
            print("KEYUP EVENT")
        elif event.type == SDL_WINDOWEVENT:
            print("WINDOW EVENT", event.window.event)
        elif event.type == SDL_JOYDEVICEADDED:
            print("JDEVICE EVENT", event.jdevice.which)
            jstick = SDL_JoystickOpen(event.jdevice.which)
        elif event.type == SDL_JOYHATMOTION:
            print("JOYHATMOTION EVENT")
            dir = event.jhat.value
            key = JHAT_MAP.get(dir)
            print("- DIR", dir, key)
            if key is not None:
                game.press(key)
        elif event.type == SDL_JOYBUTTONDOWN:
            print("JOYBUTTONDOWN EVENT")
            button = event.jbutton.button
            key = JBUTTON_MAP.get(button)
            print("- BUTTON", button, key)
            if key is not None:
                game.press(key)
        elif event.type == SDL_JOYBUTTONUP:
            print("JOYBUTTONUP EVENT")
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
