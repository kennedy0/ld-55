from engine import *


class Bg(Entity):
    def __init__(self) -> None:
        super().__init__()
        self.sprite = Sprite.from_atlas("atlas.png", "bg")
        self.x = -160
        self.y = -90
        self.z_depth = 1000

    def draw(self, camera: Camera) -> None:
        self.sprite.draw(camera, self.position())
