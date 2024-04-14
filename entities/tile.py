from __future__ import annotations

import random
from typing import TYPE_CHECKING

from engine import *

if TYPE_CHECKING:
    from entities.board import Board
    from entities.game_manager import GameManager
    from entities.skull import Skull


class Tile(Entity):
    def __init__(self) -> None:
        super().__init__()
        self.sprite = Sprite.empty()

        self.q = 0
        self.r = 0
        self.s = 0
        self.coordinates = (0, 0, 0)

        self.reveal_started = False
        self.reveal_finished = False
        self.visible = False
        self.enabled = False

        self.northwest: Tile | None = None
        self.north: Tile | None = None
        self.northeast: Tile | None = None
        self.southwest: Tile | None = None
        self.south: Tile | None = None
        self.southeast: Tile | None = None
        self.neighbors: dict[str, Tile] = {}

        self.game_manager: GameManager | None = None
        self.board: Board | None = None

        self.skull: Skull | None = None

        self.blue_can_summon = False
        self.red_can_summon = False

        self.reveal_delay = 0
        self.reveal_timer = 0
        self.reveal_max_time = 2

        self.reveal_y_start = 0
        self.reveal_y_offset = 0

        self.debug_text = Text("fonts/NotJamOldStyle11.11.png")

    def start(self) -> None:
        self.game_manager = self.find("GameManager")
        self.board = self.find("Board")
        self.init_sprite()

    def init_sprite(self) -> None:
        if self.coordinates in self.board.blue_start_coordinates:
            self.sprite = Sprite.from_atlas("atlas.png", "hex_blue_starter")
        elif self.coordinates in self.board.red_start_coordinates:
            self.sprite = Sprite.from_atlas("atlas.png", "hex_red_starter")
        else:
            self.sprite = Sprite.from_atlas("atlas.png", "hex")

        self.sprite.pivot.set_center()

    def mouse_hovering(self) -> bool:
        if Mouse.world_position().distance_to(self.position()) < 10:
            return True
        return False

    def is_free(self) -> bool:
        if not self.enabled:
            return False

        if self.skull:
            return False

        return True

    def update(self) -> None:
        if self.reveal_started:
            if self.reveal_timer > 0:
                self.update_timers()
                self.animate_reveal()
            elif not self.reveal_finished:
                self.reveal_finished = True
                self.enabled = True
                self.board.revealed_tiles += 1
                self.sprite.color = None
                self.sprite.opacity = 255
                self.clear_highlight()

        if self.enabled:
            if self.mouse_hovering():
                self.board.hovered_tile = self

    def update_timers(self) -> None:
        self.reveal_delay -= Time.delta_time
        if self.reveal_delay <= 0:
            self.reveal_delay = 0

        if self.reveal_delay <= 0:
            self.visible = True
            self.reveal_timer -= Time.delta_time
            if self.reveal_timer <= 0:
                self.reveal_timer = 0

    def animate_reveal(self) -> None:
        if self.visible:
            t = (self.reveal_max_time - self.reveal_timer) / self.reveal_max_time
            self.sprite.flash_color = Color.white()
            self.sprite.flash_opacity = int(pmath.lerp(255, 0, t))
            self.sprite.opacity = int(pmath.lerp(0, 255, t))
            self.reveal_y_offset = int(pmath.lerp(self.reveal_y_start, 0, t))

    def set_highlight(self, color: Color) -> None:
        self.sprite.flash_color = color
        self.sprite.flash_opacity = 32

    def clear_highlight(self) -> None:
        self.sprite.flash_color = Color.white()
        self.sprite.flash_opacity = 0

    def reveal(self, delay: float) -> None:
        self.reveal_started = True
        self.reveal_finished = False
        self.reveal_delay = delay
        self.reveal_timer = self.reveal_max_time

        self.reveal_y_start = random.randint(20, 90)
        self.reveal_y_offset = self.reveal_y_start

    def hide(self) -> None:
        self.reveal_started = False
        self.reveal_finished = False
        self.visible = False
        self.enabled = False

    def draw(self, camera: Camera) -> None:
        if self.visible:
            x = self.x
            y = self.y + self.reveal_y_offset
            self.sprite.draw(camera, Point(x, y))

    def debug_draw(self, camera: Camera) -> None:
        if self.mouse_hovering():
            self.position().draw(camera, Color.white())
            self.debug_text.text = self.coordinates
            bg = Color(0, 0, 0, 128)
            Rect(self.x, self.y, self.debug_text.width + 4, self.debug_text.height + 4).draw(camera, bg, solid=True)
            self.debug_text.draw(camera, self.position() + Point(2, 2))
        else:
            self.position().draw(camera, Color.gray())
