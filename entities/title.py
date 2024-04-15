from engine import *

from entities.main_menu_entity import MainMenuEntity


class Title(MainMenuEntity):
    def __init__(self) -> None:
        super().__init__()
        self.sprite = Sprite.from_atlas("atlas.png", "title")

        self.blue = AnimatedSprite.from_atlas("atlas.png", "blue_skull")
        self.blue.pivot.set_center()
        self.blue.play("default")
        self.blue.scale = 1

        self.red = AnimatedSprite.from_atlas("atlas.png", "red_skull")
        self.red.pivot.set_center()
        self.red.play("default")
        self.red.scale = 1

        self.row = -2

    def start(self) -> None:
        super().start()
        self.x = 0
        self.y = 0

    def animate(self) -> None:
        t = pmath.remap(self.timer, self.max_timer, 0, 0, 1)
        if self.fade_in:
            opacity = int(pmath.lerp(0, 255, t))
        else:
            opacity = int(pmath.lerp(255, 0, t))

        self.sprite.opacity = opacity

    def update(self) -> None:
        super().update()
        self.red.update()
        self.blue.update()

    def draw(self, camera: Camera) -> None:
        self.sprite.draw(camera, self.position())
        self.blue.draw(camera, Point(80, 35))
        self.red.draw(camera, Point(242, 35))
