import sdl2

from engine import *


class Debugger(Entity):
    def __init__(self) -> None:
        super().__init__()

    def debug_draw(self, camera: Camera) -> None:
        if Keyboard.get_key_down(sdl2.SDLK_e):
            for e in self.scene.entities:
                Log.debug(e)
