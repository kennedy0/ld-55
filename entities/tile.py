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
        self.neighbors: dict[str, Tile] = {}

        self.game_manager: GameManager | None = None
        self.board: Board | None = None

        self.skull: Skull | None = None

        self.blue_can_summon = False
        self.red_can_summon = False

        self.debug_text = Text("fonts/NotJamOldStyle11.11.png")

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

    def set_highlight(self, color: Color) -> None:
        self.sprite.flash_color = color
        self.sprite.flash_opacity = 32

    def clear_highlight(self) -> None:
        self.sprite.flash_color = Color.white()
        self.sprite.flash_opacity = 0

    def draw(self, camera: Camera) -> None:
        self.sprite.draw(camera, self.position())

    def debug_draw(self, camera: Camera) -> None:
        if self.mouse_hovering():
            self.position().draw(camera, Color.white())
            self.debug_text.text = self.coordinates
            bg = Color(0, 0, 0, 128)
            Rect(self.x, self.y, self.debug_text.width + 4, self.debug_text.height + 4).draw(camera, bg, solid=True)
            self.debug_text.draw(camera, self.position() + Point(2, 2))
        else:
            self.position().draw(camera, Color.gray())
