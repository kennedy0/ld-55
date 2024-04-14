from engine import *


class UiGameEnded(Entity):
    def __init__(self) -> None:
        super().__init__()
        self.tags.add("UI")
        self.text = Text("fonts/antiquity-print.13.png")

    def start(self) -> None:
        self.x = 160
        self.y = 90

    def set_draw(self) -> None:
        self.text.text = "Draw"
        self.text.color = Color(169, 188, 191)
        self.text.align_vertical_center()
        self.text.align_horizontal_center()

    def set_blue(self) -> None:
        self.text.text = "Blue Wins"
        self.text.color = Color(127, 187, 220)
        self.text.align_vertical_center()
        self.text.align_horizontal_center()

    def set_red(self) -> None:
        self.text.text = "Red Wins"
        self.text.color = Color(157, 67, 67)
        self.text.align_vertical_center()
        self.text.align_horizontal_center()

    def draw(self, camera: Camera) -> None:
        self.text.draw(camera, self.position())
