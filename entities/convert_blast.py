from __future__ import annotations

from typing import Self, TYPE_CHECKING

from engine import *

if TYPE_CHECKING:
    from entities.skull import Skull


class ConvertBlast(Entity):
    def __init__(self) -> None:
        super().__init__()
        self.sprite = AnimatedSprite.empty()

    @classmethod
    def create(cls, parent: Skull, direction: str) -> Self:
        cb = cls()
        cb.sprite = AnimatedSprite.from_atlas("atlas.png", f"{parent.team}_blast_{direction}")
        cb.sprite.pivot.set_center()
        cb.sprite.play("default")
        cb.sprite.get_animation("default").loop = False
        cb.x = parent.x
        cb.y = parent.y - 6
        parent.scene.entities.add(cb)
        return cb

    def update(self) -> None:
        self.sprite.update()
        if not self.sprite.is_playing:
            self.destroy()

    def draw(self, camera: Camera) -> None:
        self.sprite.draw(camera, self.position())
