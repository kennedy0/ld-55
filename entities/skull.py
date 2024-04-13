from __future__ import annotations

from typing import TYPE_CHECKING

from engine import *

if TYPE_CHECKING:
    from entities.tile import Tile


class Skull(Entity):
    def __init__(self) -> None:
        super().__init__()
        self.sprite = AnimatedSprite.empty()
        self.tile: Tile | None = None
        self.team: str | None = None

    def awake(self) -> None:
        self.sprite.pivot.set_bottom_center()
        self.sprite.play("default")

    def convert_neighbors(self) -> None:
        for tile in self.tile.neighbors:
            if skull := tile.skull:
                if self.team != skull.team:
                    skull.convert()

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
        self.sprite.update()

    def draw(self, camera: Camera) -> None:
        self.sprite.draw(camera, self.position())
