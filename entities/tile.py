from __future__ import annotations
from typing import TYPE_CHECKING

from engine import *

if TYPE_CHECKING:
    from entities.board import Board
    from entities.game_manager import GameManager
    from entities.skull import Skull


class Tile(Entity):
    def __init__(self) -> None:
        super().__init__()
        self.sprite = Sprite.from_atlas("atlas.png", "hex")
        self.sprite.pivot.set_center()

        self.q = 0
        self.r = 0
        self.s = 0
        self.coordinates = (0, 0, 0)

        self.northwest: Tile | None = None
        self.north: Tile | None = None
        self.northeast: Tile | None = None
        self.southwest: Tile | None = None
        self.south: Tile | None = None
        self.southeast: Tile | None = None
        self.neighbors: list[Tile] = []

        self.skull: Skull | None = None

        self.game_manager: GameManager | None = None
        self.board: Board | None = None

    def start(self) -> None:
        self.game_manager = self.find("GameManager")
        self.board = self.find("Board")

    def mouse_hovering(self) -> bool:
        if Mouse.world_position().distance_to(self.position()) < 10:
            return True
        return False

    def is_free(self) -> bool:
        if self.skull:
            return False

        return True

    def update(self) -> None:
        if self.mouse_hovering():
            self.board.hovered_tile = self

        self.update_hover_color()

    def update_hover_color(self) -> None:
        self.sprite.flash_opacity = 0
        if self.is_free():
            if self.game_manager.current_player:
                if self.board.hovered_tile == self:
                    self.sprite.flash_color = self.game_manager.current_player.tile_hover_color
                    self.sprite.flash_opacity = 64

    def draw(self, camera: Camera) -> None:
        self.sprite.draw(camera, self.position())

    def debug_draw(self, camera: Camera) -> None:
        if self.mouse_hovering():
            self.position().draw(camera, Color.white())
        else:
            self.position().draw(camera, Color.gray())
