from __future__ import annotations
from typing import TYPE_CHECKING

from engine import *

if TYPE_CHECKING:
    from entities.board import Board
    from entities.game_manager import GameManager


class SummonCircle(Entity):
    def __init__(self) -> None:
        super().__init__()
        self.name = "SummonCircle"

        self.blue_sprite = AnimatedSprite.from_atlas("atlas.png", "summon_circle_blue")
        self.blue_sprite.pivot.set_center()
        self.blue_sprite.play("default")

        self.red_sprite = AnimatedSprite.from_atlas("atlas.png", "summon_circle_red")
        self.red_sprite.pivot.set_center()
        self.red_sprite.play("default")

        self.game_manager: GameManager | None = None
        self.board: Board | None = None

        self.visible = False

    def start(self) -> None:
        self.game_manager = self.find("GameManager")
        self.board = self.find("Board")

    def update(self) -> None:
        self.blue_sprite.update()
        self.red_sprite.update()

        self.visible = False

        if self.game_manager.is_tutorial:
            if self.game_manager.tutorial_step == 8:
                return

        if player := self.game_manager.current_player:
            if tile := self.board.hovered_tile:
                if player.can_summon_on_tile(tile):
                    self.visible = True
                    self.x = tile.x
                    self.y = tile.y

    def draw(self, camera: Camera) -> None:
        if self.visible:
            if self.game_manager.current_player.team == "blue":
                sprite = self.blue_sprite
            else:
                sprite = self.red_sprite

            sprite.draw(camera, self.position())
            sprite.play("default")
        else:
            self.red_sprite.stop()
            self.blue_sprite.stop()
