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

        self.text.text = ""

        self.x = 160
        self.y = 171

        self.bg = Rect(0, 163, 320, 17)
        self.bg_color = Color(46, 46, 67)

        self.timer = 0
        self.max_timer = .5

        self.fading_out = False
        self.fading_in = False

        self.next_text = ""

    def awake(self) -> None:
        self.active = False

    def update(self) -> None:
        self.update_timers()
        self.animate_fading()

    def update_timers(self) -> None:
        self.timer -= Time.delta_time
        if self.timer <= 0:
            self.timer = 0

    def animate_fading(self) -> None:
        if not self.fading_out and not self.fading_in:
            return

        t = pmath.remap(self.timer, self.max_timer, 0, 0, 1)

        if self.fading_out:
            opacity = pmath.lerp(255, 0, t)
            if self.timer == 0:
                self.timer = self.max_timer
                self.fading_out = False
                self.fading_in = True
                self.text.text = self.next_text
                self.text.opacity = 0
                self.next_text = ""
                return
            opacity = int(opacity)
            self.text.opacity = opacity

        if self.fading_in:
            opacity = pmath.lerp(0, 255, t)
            if self.timer <= 0:
                self.fading_in = False
                opacity = 255
            opacity = int(opacity)
            self.text.opacity = opacity

    def show_text(self, text: str) -> None:
        self.text.opacity = 255
        self.fading_out = True
        self.fading_in = False
        self.timer = self.max_timer
        self.next_text = text

    def draw(self, camera: Camera) -> None:
        self.bg.draw(camera, self.bg_color, solid=True)
        self.text.draw(camera, self.position())
