from engine import *

from entities.board import Board
from entities.game_manager import GameManager
from entities.tile import Tile
from entities.red_skull import RedSkull
from entities.blue_skull import BlueSkull


class Player(Entity):
    def __init__(self) -> None:
        super().__init__()
        self.game_manager: GameManager | None = None
        self.board: Board | None = None
        self.team = ""

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
        if self.team == "red":
            skull = RedSkull()
        elif self.team == "blue":
            skull = BlueSkull()
        else:
            Log.error("Not red or blue")
            return

        self.scene.entities.add(skull)
        skull.x = tile.x
        skull.y = tile.y + 4
        tile.skull = skull
        skull.tile = tile
        skull.summoned_by_player = True
        skull.get_neighboring_opponents()
        self.game_manager.next_turn_delay = len(skull.neighbors_to_convert) * .3

    def end_turn(self) -> None:
        self.game_manager.turn_ended = True
