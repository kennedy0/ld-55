from engine import *

from entities.player import Player
from entities.blue_skull import BlueSkull


class BluePlayer(Player):
    def __init__(self) -> None:
        super().__init__()
        self.name = "BluePlayer"
        self.tile_hover_color = Color(0, 128, 255)

    def blue(self) -> bool:
        return True

    def create_skull(self) -> BlueSkull:
        skull = BlueSkull()
        self.scene.entities.add(skull)
        return skull
