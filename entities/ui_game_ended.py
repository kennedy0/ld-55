from engine import *


class UiGameEnded(Entity):
    def __init__(self) -> None:
        super().__init__()
        self.name = "UiGameEnded"
        self.tags.add("UI")
        self.text = Text("fonts/antiquity-print.13.png")
        self.text.opacity = 0
        self.banner = Rect.empty()
        self.banner_color = Color(46, 46, 67)

        self.timer = 0
        self.is_animating = False

    def start(self) -> None:
        self.active = False
        self.x = 160
        self.y = 90

    def set_tutorial(self, text: str) -> None:
        self.text.text = text
        self.text.color = Color(169, 188, 191)
        self.text.align_vertical_center()
        self.text.align_horizontal_center()
        self.timer = 0
        self.is_animating = True
        self.active = True

    def set_draw(self) -> None:
        self.text.text = "Draw"
        self.text.color = Color(169, 188, 191)
        self.text.align_vertical_center()
        self.text.align_horizontal_center()
        self.timer = 0
        self.is_animating = True
        self.active = True

    def set_blue(self) -> None:
        self.text.text = "Blue\nWins"
        self.text.color = Color(127, 187, 220)
        self.text.align_vertical_center()
        self.text.align_horizontal_center()
        self.timer = 0
        self.is_animating = True
        self.active = True

    def set_red(self) -> None:
        self.text.text = "Red\nWins"
        self.text.color = Color(157, 67, 67)
        self.text.align_vertical_center()
        self.text.align_horizontal_center()
        self.timer = 0
        self.is_animating = True
        self.active = True

    def update(self) -> None:
        self.timer += Time.delta_time

        # Banner
        banner_x = 0
        banner_w = 320
        if 0 <= self.timer < .5:
            t = pmath.remap(self.timer, 0, .5, 0, 1)
            banner_w = pmath.lerp(0, 320, t)
        elif 3 <= self.timer < 3.5:
            t = pmath.remap(self.timer, 3, 3.5, 0, 1)
            banner_x = pmath.lerp(0, 320, t)
        elif self.timer > 3.5:
            banner_w = 0
        self.banner = Rect(banner_x, 64, banner_w, 49)

        # Text
        text_opacity = 0
        if .5 < self.timer < 1:
            t = pmath.remap(self.timer, .5, 1, 0, 1)
            text_opacity = int(pmath.lerp(0, 255, t))
        elif 1 < self.timer < 2.5:
            text_opacity = 255
        elif 2.5 < self.timer < 3:
            t = pmath.remap(self.timer, 2.5, 3, 0, 1)
            text_opacity = int(pmath.lerp(255, 0, t))
        self.text.opacity = text_opacity

        # Deactivate
        if self.timer > 4:
            self.is_animating = False
            self.active = False

    def draw(self, camera: Camera) -> None:
        self.banner.draw(camera, self.banner_color, solid=True)
        self.text.draw(camera, self.position())
