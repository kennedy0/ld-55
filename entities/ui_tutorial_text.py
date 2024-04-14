from engine import *


class UiTutorialText(Entity):
    def __init__(self) -> None:
        super().__init__()
        self.name = "UiTutorialText"
        self.tags.add("UI")
        self.text = Text("fonts/NotJamOldStyle11.11.png")
        self.text.align_horizontal_center()
        self.text.align_vertical_center()
        self.text.color = Color(230, 238, 237)

        self.text.text = "Tutorial text, baby! Let's do this thing..."

        self.x = 160
        self.y = 171

        self.bg = Rect(0, 163, 320, 17)
        self.bg_color = Color(46, 46, 67)

    def awake(self) -> None:
        self.active = False

    def draw(self, camera: Camera) -> None:
        self.bg.draw(camera, self.bg_color, solid=True)
        self.text.draw(camera, self.position())
