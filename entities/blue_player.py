from engine import *

from entities.player import Player


class BluePlayer(Player):
    def __init__(self) -> None:
        super().__init__()
        self.name = "BluePlayer"
        self.team = "blue"
        self.tile_hover_color = Color(0, 128, 255)
