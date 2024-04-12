from typing import Optional

import sdl2


def button_to_name(key: int) -> Optional[str]:
    """ Get the human-readable name for a key. """
    name = sdl2.SDL_GameControllerGetStringForButton(key)
    if isinstance(name, bytes):
        name = name.decode("utf-8")
        return name


def controller_name(controller: int) -> Optional[str]:
    """ Get the human-readable name for a controller. """
    name = sdl2.SDL_GameControllerName(controller)
    if isinstance(name, bytes):
        name = name.decode("utf-8")
        return name
