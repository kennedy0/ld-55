from __future__ import annotations

from engine import *

from typing import Self, TYPE_CHECKING

if TYPE_CHECKING:
    from entities.skull import Skull


class SummonFx(Entity):
    def __init__(self) -> None:
        super().__init__()
        self.sprite = AnimatedSprite.empty()
        self.parent: Skull | None = None

    @classmethod
    def create(cls, parent: Skull) -> Self:
        fx = cls()
        fx.parent = parent
        parent.scene.entities.add(fx)
        fx.x = parent.x
        fx.y = parent.y - 6

        fx.sprite = AnimatedSprite.from_atlas("atlas.png", f"summon_fx_{parent.team}")
        fx.sprite.pivot.set_center()
        fx.sprite.play("default")
        fx.sprite.get_animation("default").loop = False

        return fx

    def update(self) -> None:
        self.sprite.update()
        if not self.sprite.is_playing:
            self.parent.visible = True
            self.destroy()

    def draw(self, camera: Camera) -> None:
        self.sprite.draw(camera, self.position())
