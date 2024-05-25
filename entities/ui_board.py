from engine import *

from entities.board import Board
from entities.main_menu_entity import MainMenuEntity


class UiBoard(MainMenuEntity):
    def __init__(self) -> None:
        super().__init__()
        self.name = "UiBoard"
        self.board: Board | None = None

        self.option = 0
        self.options = ["Board: A", "Board: B", "Board: C", "Board: Random"]
        self.text.text = self.options[self.option]
        self.width = self.text.width
        self.height = self.text.height

        self.sprite_opacity = 0
        self.sprite_a = Sprite.from_atlas("atlas.png", "board_layout_a")
        self.sprite_b = Sprite.from_atlas("atlas.png", "board_layout_b")
        self.sprite_c = Sprite.from_atlas("atlas.png", "board_layout_c")
        self.sprite_random = Sprite.from_atlas("atlas.png", "board_layout_random")
        self.sprite_a.pivot.set_center()
        self.sprite_b.pivot.set_center()
        self.sprite_c.pivot.set_center()
        self.sprite_random.pivot.set_center()

        self.row = 3

    def start(self) -> None:
        super().start()
        self.board = self.find("Board")

    def update(self) -> None:
        super().update()
        if self.hovering:
            if Mouse.get_left_mouse_down():
                if self.option == 3:
                    self.option = 0
                else:
                    self.option += 1

                self.text.text = self.options[self.option]
                self.board.board_layout = self.option

                self.width = self.text.width
                self.height = self.text.height

        if self.hovering:
            self.sprite_opacity += 20
        else:
            self.sprite_opacity -= 20
        self.sprite_opacity = pmath.clamp(self.sprite_opacity, 0, 255)

    def draw(self, camera: Camera) -> None:
        super().draw(camera)
        if self.option == 0:
            sprite = self.sprite_a
        elif self.option == 1:
            sprite = self.sprite_b
        elif self.option == 2:
            sprite = self.sprite_c
        else:
            sprite = self.sprite_random

        sprite.opacity = self.sprite_opacity
        sprite.draw(camera, self.position() + Point(-20, 4))
