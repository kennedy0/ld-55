from typing import Optional

import sdl2


def key_to_name(key: int) -> Optional[str]:
    """ Get the human-readable name for a key. """
    name = sdl2.SDL_GetKeyName(key)
    if isinstance(name, bytes):
        name = name.decode("utf-8")
        return name


def name_to_key(name: str) -> Optional[int]:
    """ Get the key code from its name. """
    key = sdl2.SDL_GetKeyFromName(name.encode("utf-8"))
    if key == sdl2.SDLK_UNKNOWN:
        return None
    else:
        return key
