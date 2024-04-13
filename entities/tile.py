from engine import *


class Tile(Entity):
    def __init__(self) -> None:
        super().__init__()
        self.sprite = Sprite.from_atlas("atlas.png", "hex")
        self.sprite.pivot.set_center()

        self.q = 0
        self.r = 0
        self.s = 0
        self.coordinates = (0, 0, 0)

        self.hover_color_blue = Color(170, 238, 234)

    def mouse_hovering(self) -> bool:
        if Mouse.world_position().distance_to(self.position()) < 10:
            return True

        return False

    def update(self) -> None:
        self.update_color()

    def update_color(self) -> None:
        if self.mouse_hovering():
            self.sprite.flash_color = self.hover_color_blue
            self.sprite.flash_opacity = 64
        else:
            self.sprite.flash_opacity = 0

    def draw(self, camera: Camera) -> None:
        self.sprite.draw(camera, self.position())

    def debug_draw(self, camera: Camera) -> None:
        if self.mouse_hovering():
            self.position().draw(camera, Color.white())
        else:
            self.position().draw(camera, Color.gray())
