from __future__ import annotations
from typing import TYPE_CHECKING

import sdl2
from engine import *

if TYPE_CHECKING:
    from entities.board import Board
    from entities.game_manager import GameManager


class Debugger(Entity):
    def __init__(self) -> None:
        super().__init__()
        self.board: Board | None = None
        self.game_manager: GameManager | None = None

    def start(self) -> None:
        self.board = self.find("Board")
        self.game_manager = self.find("GameManager")

    def debug_draw(self, camera: Camera) -> None:
        if Keyboard.get_key_down(sdl2.SDLK_v):
            Log.debug(f"Valid Blue Tiles: {len(self.board.valid_blue_tiles)}")
            Log.debug(f"Valid Red Tiles: {len(self.board.valid_red_tiles)}")
