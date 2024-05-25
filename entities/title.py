from engine import *

from entities.main_menu_entity import MainMenuEntity

from entities.ui_tutorial import UiTutorial
from entities.ui_1p import Ui1p
from entities.ui_2p import Ui2p
from entities.ui_board import UiBoard
from entities.ui_sound import UiSound
from entities.ui_quit_game import UiQuitGame


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

        self.buttons: list[MainMenuEntity] = []

    def start(self) -> None:
        super().start()
        self.x = 0
        self.y = -10
        self.buttons = [
            self.find("UiTutorial"),
            self.find("Ui1p"),
            self.find("Ui2p"),
            self.find("UiBoard"),
            self.find("UiSound"),
            self.find("UiQuitGame"),
        ]

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
        self.blue.draw(camera, Point(80, 25))
        self.red.draw(camera, Point(242, 25))
