import math

from engine import *


class SummonCircle(Entity):
    def __init__(self) -> None:
        super().__init__()

        self.sprite = AnimatedSprite.from_atlas("atlas.png", "summon_circle")
        self.sprite.pivot.set_center()
        self.sprite.play("default")

    def awake(self) -> None:
        self.active = True

    def update(self) -> None:
        self.sprite.update()

    def draw(self, camera: Camera) -> None:
        self.sprite.draw(camera, self.position())
