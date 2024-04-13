from engine import *

from entities.board import Board
from entities.game_manager import GameManager
from entities.tile import Tile
from entities.skull import Skull


class Player(Entity):
    def __init__(self) -> None:
        super().__init__()
        self.game_manager: GameManager | None = None
        self.board: Board | None = None

        self.tile_hover_color = Color.gray()

    def start(self) -> None:
        self.game_manager = self.find("GameManager")
        self.board = self.find("Board")

    def is_my_turn(self) -> bool:
        return self.game_manager.current_player == self

    def update(self) -> None:
        if not self.is_my_turn():
            return

        self.update_input()

    def update_input(self) -> None:
        if Mouse.get_left_mouse_down():
            if tile := self.board.hovered_tile:
                if tile.is_free():
                    self.summon_skull(tile)
                    self.end_turn()

    def summon_skull(self, tile: Tile) -> None:
        skull = self.create_skull()
        skull.x = tile.x
        skull.y = tile.y + 4
        tile.skull = skull

    def end_turn(self) -> None:
        self.game_manager.turn_ended = True

    def create_skull(self) -> Skull:
        raise NotImplementedError
