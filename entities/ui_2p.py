from engine import *

from entities.main_menu_entity import MainMenuEntity


class Ui2p(MainMenuEntity):
    def __init__(self) -> None:
        super().__init__()

        self.text.text = "2 Players"
        self.width = self.text.width
        self.height = self.text.height

        self.row = 3

    def update(self) -> None:
        super().update()
        if self.hovering:
            if Mouse.get_left_mouse_down():
                self.game_manager.red_player.controller = "human"
                self.game_manager.start_game()
