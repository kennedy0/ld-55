from __future__ import annotations

import random
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
        self.normal_color = Color(112, 123, 137)
        self.hover_color = Color(230, 238, 237)

        self.fade_in = False
        self.fade_out = False
        self.is_animating = False
        self.delay = 0
        self.timer = 0
        self.max_timer = 1

        self.row = 0

        self.sfx: list[SoundEffect] = [
            SoundEffect("sfx/tone_1.wav"),
            SoundEffect("sfx/tone_2.wav"),
            SoundEffect("sfx/tone_3.wav"),
            SoundEffect("sfx/tone_4.wav"),
        ]

    def start(self) -> None:
        self.game_manager = self.find("GameManager")
        self.x = 160 - self.text.width / 2
        self.y = 60 + (self.row * 20)

    def show(self, delay: float) -> None:
        self.fade_in = True
        self.fade_out = False
        self.active = True
        self.is_animating = True
        self.hovering = False
        self.timer = self.max_timer
        self.delay = delay

    def hide(self, delay: float) -> None:
        self.fade_in = False
        self.fade_out = True
        self.active = False
        self.is_animating = True
        self.hovering = False
        self.timer = self.max_timer
        self.delay = delay

    def on_mouse_enter(self) -> None:
        if self.is_animating:
            return
        self.hovering = True
        random.choice(self.sfx).play()

    def on_mouse_exit(self) -> None:
        self.hovering = False

    def update(self) -> None:
        self.update_timers()
        if self.is_animating:
            self.animate()
            if self.timer <= 0:
                self.is_animating = False

        if self.hovering:
            if Mouse.get_left_mouse_down():
                pass

    def update_timers(self) -> None:
        self.delay -= Time.delta_time
        if self.delay <= 0:
            self.delay = 0
            self.timer -= Time.delta_time
            if self.timer <= 0:
                self.timer = 0

    def animate(self) -> None:
        t = pmath.remap(self.timer, self.max_timer, 0, 0, 1)

        if self.fade_in:
            opacity = int(pmath.lerp(0, 255, t))
        else:
            opacity = int(pmath.lerp(255, 0, t))

        self.text.opacity = opacity

    def draw(self, camera: Camera) -> None:
        if self.hovering:
            self.text.color = self.hover_color
        else:
            self.text.color = self.normal_color

        self.text.draw(camera, self.position())
