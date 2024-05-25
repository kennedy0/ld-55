from __future__ import annotations

from typing import TYPE_CHECKING

from engine import *

if TYPE_CHECKING:
    from entities.game_manager import GameManager


class UiForfeit(Entity):
    def __init__(self) -> None:
        super().__init__()
        self.tags.add("UI")

        self.game_manager: GameManager | None = None

        self.visible = False

        self.width = 180
        self.height = 16
        self.x = (Renderer.resolution()[0] // 2) - (self.width // 2)
        self.y = 4

        self.text = Text("fonts/NotJamOldStyle11.11.png")
        self.text.align_horizontal_center()
        self.text.align_vertical_center()
        self.text.text = "Forfeit"
        self.text.color = Color.from_hex("#2A152D")
        self.text_position = Point(self.x + self.width // 2, self.y + self.height // 2)

        self.hint_text = Text("fonts/NotJamOldStyle11.11.png")
        self.hint_text.align_horizontal_center()
        self.hint_text.align_vertical_center()
        self.hint_text.text = "(Hold ESC to forfeit)"
        self.hint_text.opacity = 16

        self.bg_color = Color(112, 123, 137)
        self.fg_color = Color.from_hex("#9D4343")

    def start(self) -> None:
        self.game_manager = self.find("GameManager")

    def draw(self, camera: Camera) -> None:
        if not self.game_manager.game_started:
            return

        if self.game_manager.game_ended:
            return

        if not self.game_manager.forfeit_timer:
            self.hint_text.draw(camera, self.text_position)
            return

        Rect(self.x, self.y, self.width, self.height).draw(camera, self.bg_color, solid=True)

        w = int(pmath.remap(self.game_manager.forfeit_timer, 0, 1, 0, self.width))
        Rect(self.x, self.y, w, self.height).draw(camera, self.fg_color, solid=True)

        self.text.draw(camera, self.text_position)
