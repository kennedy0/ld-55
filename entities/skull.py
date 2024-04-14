from __future__ import annotations

import random
from typing import TYPE_CHECKING

from engine import *

from entities.convert_blast import ConvertBlast
from entities.summon_fx import SummonFx

if TYPE_CHECKING:
    from entities.board import Board
    from entities.tile import Tile


class Skull(Entity):
    def __init__(self) -> None:
        super().__init__()
        self.board: Board | None = None

        self.sprite = AnimatedSprite.empty()

        self.tile: Tile | None = None
        self.team: str = ""

        self.neighbors_to_convert: list[tuple[str, Skull]] = []
        self.convert_neighbor_delay = .1
        self.convert_neighbor_timer = 0
        self.summoned_by_player = False

        self.summon_sfx: list[SoundEffect] = [
            SoundEffect("sfx/summon1.wav"),
            SoundEffect("sfx/summon2.wav"),
            SoundEffect("sfx/summon3.wav"),
            SoundEffect("sfx/summon4.wav"),
            SoundEffect("sfx/summon5.wav"),
            SoundEffect("sfx/summon6.wav"),
            SoundEffect("sfx/summon7.wav"),
        ]

        self.explosion_sfx: list[SoundEffect] = [
            SoundEffect("sfx/explosion1.wav"),
            SoundEffect("sfx/explosion2.wav"),
            SoundEffect("sfx/explosion3.wav"),
            SoundEffect("sfx/explosion4.wav"),
        ]

        self.shoot_sfx: list[SoundEffect] = [
            SoundEffect("sfx/shoot1.wav"),
            SoundEffect("sfx/shoot2.wav"),
            SoundEffect("sfx/shoot3.wav"),
            SoundEffect("sfx/shoot4.wav"),
            SoundEffect("sfx/shoot5.wav"),
        ]

        self.is_killed = False
        self.kill_timer = 0

    def awake(self) -> None:
        self.sprite.pivot.set_bottom_center()
        self.sprite.play("default")

    def start(self) -> None:
        self.board = self.find("Board")

        if self.team == "blue":
            self.board.blue_tiles += 1  # noqa
        if self.team == "red":
            self.board.red_tiles += 1  # noqa

        summon_fx = SummonFx.create(self)

        if self.summoned_by_player:
            sfx = random.choice(self.summon_sfx)
            sfx.play()

    def get_neighboring_opponents(self) -> None:
        for direction, tile in self.tile.neighbors.items():
            if skull := tile.skull:
                if self.team != skull.team:
                    self.neighbors_to_convert.append((direction, skull))
        random.shuffle(self.neighbors_to_convert)

    def convert(self) -> None:
        from entities.blue_skull import BlueSkull
        from entities.red_skull import RedSkull

        sfx = random.choice(self.explosion_sfx)
        sfx.play()

        if self.team == "blue":
            new_skull = RedSkull()
        else:
            new_skull = BlueSkull()

        self.scene.entities.add(new_skull)
        new_skull.x = self.x
        new_skull.y = self.y
        new_skull.tile = self.tile
        self.tile.skull = new_skull
        self.destroy()

    def kill(self, delay: float) -> None:
        self.is_killed = True
        self.kill_timer = delay
        self.tile.skull = None
        self.tile = None

    def update(self) -> None:
        self.update_timers()

        if self.is_killed:
            if self.kill_timer <= 0:
                self.destroy()
                return

        if self.neighbors_to_convert:
            if self.convert_neighbor_timer <= 0:
                self.convert_neighbor_timer = self.convert_neighbor_delay
                direction, neighbor = self.neighbors_to_convert.pop()
                self.convert_neighbor(direction, neighbor)

        self.sprite.update()

    def update_timers(self) -> None:
        self.convert_neighbor_timer -= Time.delta_time
        if self.convert_neighbor_timer < 0:
            self.convert_neighbor_timer = 0

        if self.is_killed:
            self.kill_timer -= Time.delta_time
            if self.kill_timer < 0:
                self.kill_timer = 0

    def convert_neighbor(self, direction: str, neighbor: Skull) -> None:
        blast = ConvertBlast.create(self, direction)
        blast.target = neighbor
        sfx = random.choice(self.shoot_sfx)
        sfx.play()

    def draw(self, camera: Camera) -> None:
        self.sprite.draw(camera, self.position())

    def on_deactivate(self) -> None:
        if self.team == "blue":
            self.board.blue_tiles -= 1
        if self.team == "red":
            self.board.red_tiles -= 1
