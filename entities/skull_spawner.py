from engine import *

from entities.blue_skull import BlueSkull
from entities.game_manager import GameManager
from entities.tile import Tile


class SkullSpawner(Entity):
    def __init__(self) -> None:
        super().__init__()
        self.game_manager: GameManager | None = None

    def start(self) -> None:
        self.game_manager = self.find("GameManager")

    def update(self) -> None:
        if self.game_manager.is_blue_turn():
            pass

    def spawn_blue_skull(self, tile: Tile) -> None:
        skull = BlueSkull()
        skull.x = tile.x
        skull.y = tile.y
        self.scene.entities.add(skull)
