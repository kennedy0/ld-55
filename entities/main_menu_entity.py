from __future__ import annotations

from typing import TYPE_CHECKING

from engine import *

if TYPE_CHECKING:
    from entities.game_manager import GameManager


class MainMenuEntity(GuiWidgetEntity):
    def __init__(self) -> None:
        super().__init__()
        self.tags.add("MainMenu")
        self.game_manager: GameManager | None = None

        self.text = Text("fonts/NotJamOldStyle11.11.png")
        self.text.text = "Play"

        self.width = self.text.width
        self.height = self.text.height
        self.hovering = False

        self.normal_color = Color(169, 188, 191)
        self.hover_color = Color(230, 238, 237)

    def start(self) -> None:
        self.game_manager = self.find("GameManager")
        self.x = 160 - self.text.width / 2
        self.y = 0

    def on_mouse_enter(self) -> None:
        self.hovering = True

    def on_mouse_exit(self) -> None:
        self.hovering = False

    def update(self) -> None:
        if self.hovering:
            if Mouse.get_left_mouse_down():
                pass

    def draw(self, camera: Camera) -> None:
        if self.hovering:
            self.text.color = self.hover_color
        else:
            self.text.color = self.normal_color

        self.text.draw(camera, self.position())
