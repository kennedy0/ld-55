from engine import *


class Hex(Entity):
    def __init__(self, q: int, r: int, s: int) -> None:
        super().__init__()
        self.sprite = Sprite.from_atlas("atlas.png", "hex")
        self.sprite.pivot.set_center()

        self.q = q
        self.r = r
        self.s = s

    def draw(self, camera: Camera) -> None:
        self.sprite.draw(camera, self.position())
