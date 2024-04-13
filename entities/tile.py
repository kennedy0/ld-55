from __future__ import annotations
from typing import TYPE_CHECKING

from engine import *

if TYPE_CHECKING:
    from entities.board import Board
    from entities.game_manager import GameManager


TEAM_NONE = 0  # noqa
TEAM_BLUE = 1  # noqa
TEAM_RED =  2  # noqa


class Tile(Entity):
    def __init__(self) -> None:
        super().__init__()
        self.sprite = Sprite.from_atlas("atlas.png", "hex")
        self.sprite.pivot.set_center()

        self.q = 0
        self.r = 0
        self.s = 0
        self.coordinates = (0, 0, 0)

        self.is_free = True
        self.team = TEAM_NONE

        self.hover_color_neutral = Color.gray()
        self.hover_color_blue = Color(0, 128, 255)
        self.hover_color_red = Color.red()

        self.game_manager: GameManager | None = None
        self.board: Board | None = None

    def start(self) -> None:
        self.game_manager = self.find("GameManager")
        self.board = self.find("Board")

    def mouse_hovering(self) -> bool:
        if Mouse.world_position().distance_to(self.position()) < 10:
            return True
        return False

    def update(self) -> None:
        if self.mouse_hovering():
            self.set_hovered_color()
            self.board.hovered_tile = self
        else:
            self.set_normal_color()

    def set_hovered_color(self) -> None:
        if self.is_free:
            if self.game_manager.is_blue_turn():
                self.sprite.flash_color = self.hover_color_blue
            elif self.game_manager.is_red_turn():
                self.sprite.flash_color = self.hover_color_red
        else:
            self.sprite.flash_color = self.hover_color_neutral

        self.sprite.flash_opacity = 64

    def set_normal_color(self) -> None:
        self.sprite.flash_opacity = 0

    def draw(self, camera: Camera) -> None:
        self.sprite.draw(camera, self.position())

    def debug_draw(self, camera: Camera) -> None:
        if self.mouse_hovering():
            self.position().draw(camera, Color.white())
        else:
            self.position().draw(camera, Color.gray())
