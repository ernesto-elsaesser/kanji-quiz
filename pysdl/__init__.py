"""SDL2 wrapper package"""
from .dll import _bind

from ._sdl_init import *
from .error import *
from .events import *
from .keyboard import *
from .rect import *
from .stdinc import *
from .surface import *
from .timer import *
from .video import *
from .pixels import *
from .endian import *
from .keycode import *
from .scancode import *
from .ttf import *


# At least Win32 platforms need this now.
_SDL_SetMainReady = _bind("SDL_SetMainReady")
_SDL_SetMainReady()
