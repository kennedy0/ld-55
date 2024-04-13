from engine import *

from entities.blue_skull import BlueSkull
from entities.board import Board
from entities.game_manager import GameManager
from entities.red_skull import RedSkull
from entities.tile import Tile


class SkullSpawner(Entity):
    def __init__(self) -> None:
        super().__init__()
        self.game_manager: GameManager | None = None
        self.board: Board | None = None

    def start(self) -> None:
        self.game_manager = self.find("GameManager")
        self.board = self.find("Board")

    def update(self) -> None:
        if self.game_manager.is_blue_turn():
            self.update_blue_turn()
        elif self.game_manager.is_red_turn():
            self.update_red_turn()

    def update_blue_turn(self) -> None:
        if Mouse.get_left_mouse_down():
            if self.board.hovered_tile and self.board.hovered_tile.is_free:
                self.spawn_blue_skull(self.board.hovered_tile)
                self.board.hovered_tile.is_free = False
                self.game_manager.end_blue_turn()

    def update_red_turn(self) -> None:
        if Mouse.get_left_mouse_down():
            if self.board.hovered_tile and self.board.hovered_tile.is_free:
                self.spawn_red_skull(self.board.hovered_tile)
                self.board.hovered_tile.is_free = False
                self.game_manager.end_red_turn()

    def spawn_blue_skull(self, tile: Tile) -> None:
        skull = BlueSkull()
        skull.x = tile.x
        skull.y = tile.y + 4
        self.scene.entities.add(skull)

    def spawn_red_skull(self, tile: Tile) -> None:
        skull = RedSkull()
        skull.x = tile.x
        skull.y = tile.y + 4
        self.scene.entities.add(skull)
