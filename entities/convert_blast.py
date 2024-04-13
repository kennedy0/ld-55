from engine import *


class ConvertBlast(Entity):
    def __init__(self) -> None:
        super().__init__()
        self.sprite = AnimatedSprite.empty()

    def update(self) -> None:
        self.sprite.update()

    def draw(self, camera: Camera) -> None:
        self.sprite.draw(camera, self.position())
