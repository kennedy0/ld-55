from __future__ import annotations

from typing import Self

from engine import *


class Explosion(Entity):
    def __init__(self) -> None:
        super().__init__()
        self.sprite = AnimatedSprite.empty()

    @classmethod
    def create(cls, parent: Entity, color: str) -> Self:
        e = cls()
        e.sprite = AnimatedSprite.from_atlas("atlas.png", f"{color}_explosion")
        e.sprite.pivot.set_center()
        e.sprite.play("default")
        e.sprite.get_animation("default").loop = False
        parent.scene.entities.add(e)
        return e

    def update(self) -> None:
        self.sprite.update()
        if not self.sprite.is_playing:
            self.destroy()

    def draw(self, camera: Camera) -> None:
        self.sprite.draw(camera, self.position())
