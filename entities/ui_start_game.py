from engine import *

from entities.main_menu_entity import MainMenuEntity


class UiStartGame(MainMenuEntity):
    def __init__(self) -> None:
        super().__init__()

        self.text.text = "Play"
        self.width = self.text.width
        self.height = self.text.height

    def start(self) -> None:
        self.game_manager = self.find("GameManager")
        self.x = 160 - self.text.width / 2
        self.y = 90

    def update(self) -> None:
        if self.hovering:
            if Mouse.get_left_mouse_down():
                self.game_manager.start_game()
