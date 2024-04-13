from engine import *

from entities.player import Player
from entities.red_skull import RedSkull


class RedPlayer(Player):
    def __init__(self) -> None:
        super().__init__()
        self.name = "RedPlayer"
        self.tile_hover_color = Color.red()

    def create_skull(self) -> RedSkull:
        skull = RedSkull()
        self.scene.entities.add(skull)
        return skull
