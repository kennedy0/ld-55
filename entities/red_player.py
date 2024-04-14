from engine import *

from entities.player import Player


class RedPlayer(Player):
    def __init__(self) -> None:
        super().__init__()
        self.name = "RedPlayer"
        self.team = "red"
        self.tile_highlight_color = Color.red()
