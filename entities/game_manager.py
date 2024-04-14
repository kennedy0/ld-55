from __future__ import annotations

from typing import TYPE_CHECKING

from engine import *

if TYPE_CHECKING:
    from entities.player import Player
    from entities.blue_player import BluePlayer
    from entities.red_player import RedPlayer


class GameManager(Entity):
    def __init__(self) -> None:
        super().__init__()
        self.name = "GameManager"
        self.current_player: Player | None = None
        self.next_player: Player | None = None
        self.blue_player: BluePlayer | None = None
        self.red_player: RedPlayer | None = None

        self.turn_ended = False

        self.time_between_turns = 1
        self.turn_end_timer = 0

    def start(self) -> None:
        self.blue_player = self.find("BluePlayer")
        self.red_player = self.find("RedPlayer")

    def update(self) -> None:
        self.update_timers()

        # Set next player when turn ended
        if self.turn_ended:
            self.turn_end_timer = self.time_between_turns
            self.turn_ended = False
            if self.current_player == self.blue_player:
                self.next_player = self.red_player
            else:
                self.next_player = self.blue_player
            self.current_player = None

        # Set current player when timer is up
        if not self.current_player:
            if self.turn_end_timer <= 0:
                self.current_player = self.next_player
                self.next_player = None

    def update_timers(self) -> None:
        self.turn_end_timer -= Time.delta_time
        if self.turn_end_timer < 0:
            self.turn_end_timer = 0

    def end_blue_turn(self) -> None:
        self.current_player = self.red_player

    def end_red_turn(self) -> None:
        self.current_player = self.blue_player
