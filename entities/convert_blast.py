from __future__ import annotations

from typing import Self, TYPE_CHECKING

from engine import *

from entities.explosion import Explosion

if TYPE_CHECKING:
    from entities.skull import Skull


class ConvertBlast(Entity):
    def __init__(self) -> None:
        super().__init__()
        self.sprite = AnimatedSprite.empty()
        self.target: Skull | None = None
        self.converted_target = False
        self.color = ""

    @classmethod
    def create(cls, parent: Skull, direction: str) -> Self:
        cb = cls()
        cb.sprite = AnimatedSprite.from_atlas("atlas.png", f"{parent.team}_blast_{direction}")
        cb.color = parent.team
        cb.sprite.pivot.set_center()
        cb.sprite.play("default")
        cb.sprite.get_animation("default").loop = False
        cb.sprite.get_animation("default").set_duration(400)  # original duration = 500
        cb.x = parent.x
        cb.y = parent.y - 6
        parent.scene.entities.add(cb)
        return cb

    def update(self) -> None:
        self.sprite.update()
        if not self.sprite.is_playing:
            if not self.converted_target:
                self.converted_target = True
                self.target.convert()
                explosion = Explosion.create(self, self.color)
                explosion.x = self.target.x
                explosion.y = self.target.y - 6
                self.destroy()

    def draw(self, camera: Camera) -> None:
        self.sprite.draw(camera, self.position())
