from __future__ import annotations

import random
from typing import TYPE_CHECKING

from engine import *

from entities.convert_blast import ConvertBlast

if TYPE_CHECKING:
    from entities.board import Board
    from entities.tile import Tile


class Skull(Entity):
    def __init__(self) -> None:
        super().__init__()
        self.board: Board | None = None

        self.sprite = AnimatedSprite.empty()
        self.tile: Tile | None = None
        self.team: str = ""

        self.neighbors_to_convert: list[tuple[str, Skull]] = []

        self.convert_neighbor_delay = .1
        self.convert_neighbor_timer = 0

    def awake(self) -> None:
        self.sprite.pivot.set_bottom_center()
        self.sprite.play("default")

    def start(self) -> None:
        self.board = self.find("Board")

    def get_neighboring_opponents(self) -> None:
        for direction, tile in self.tile.neighbors.items():
            if skull := tile.skull:
                if self.team != skull.team:
                    self.neighbors_to_convert.append((direction, skull))
        random.shuffle(self.neighbors_to_convert)

    def convert(self) -> None:
        from entities.blue_skull import BlueSkull
        from entities.red_skull import RedSkull

        if self.team == "blue":
            new_skull = RedSkull()
        else:
            new_skull = BlueSkull()

        self.scene.entities.add(new_skull)
        new_skull.x = self.x
        new_skull.y = self.y
        new_skull.tile = self.tile
        self.tile.skull = new_skull
        self.destroy()

    def update(self) -> None:
        self.update_timers()

        if self.neighbors_to_convert:
            if self.convert_neighbor_timer <= 0:
                self.convert_neighbor_timer = self.convert_neighbor_delay
                direction, neighbor = self.neighbors_to_convert.pop()
                self.convert_neighbor(direction, neighbor)

        self.sprite.update()

    def update_timers(self) -> None:
        self.convert_neighbor_timer -= Time.delta_time
        if self.convert_neighbor_timer < 0:
            self.convert_neighbor_timer = 0

    def convert_neighbor(self, direction: str, neighbor: Skull) -> None:
        blast = ConvertBlast.create(self, direction)
        blast.target = neighbor

    def draw(self, camera: Camera) -> None:
        self.sprite.draw(camera, self.position())
