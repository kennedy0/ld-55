from engine import *

from entities.main_menu_entity import MainMenuEntity


class UiSound(MainMenuEntity):
    def __init__(self) -> None:
        super().__init__()
        self.name = "UiSound"

        self.text.text = "Sound: On"
        self.width = self.text.width
        self.height = self.text.height

        self.row = 4

    def update(self) -> None:
        super().update()
        if self.hovering:
            if Mouse.get_left_mouse_down():
                if self.text.text == "Sound: On":
                    self.text.text = "Sound: Off"
                    Audio.set_sfx_volume(0)
                    return
                if self.text.text == "Sound: Off":
                    self.text.text = "Sound: On"
                    Audio.set_sfx_volume(128)
                    return
