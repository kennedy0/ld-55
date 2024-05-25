from engine import *

from entities.main_menu_entity import MainMenuEntity


class UiQuitGame(MainMenuEntity):
    def __init__(self) -> None:
        super().__init__()
        self.name = "UiQuitGame"

        self.text.text = "Exit"
        self.width = self.text.width
        self.height = self.text.height

        self.row = 5

    def update(self) -> None:
        super().update()
        if self.hovering:
            if Mouse.get_left_mouse_down():
                Engine.stop()
