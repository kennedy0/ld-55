from __future__ import annotations

from typing import TYPE_CHECKING

from engine import *

if TYPE_CHECKING:
    from entities.player import Player
    from entities.blue_player import BluePlayer
    from entities.red_player import RedPlayer
    from entities.board import Board


class GameManager(Entity):
    def __init__(self) -> None:
        super().__init__()
        self.name = "GameManager"
        self.board: Board | None = None
        self.current_player: Player | None = None
        self.next_player: Player | None = None
        self.blue_player: BluePlayer | None = None
        self.red_player: RedPlayer | None = None

        self.turn_ended = False

        self.time_between_turns = 1
        self.turn_end_timer = 0

    def start(self) -> None:
        self.board = self.find("Board")
        self.blue_player = self.find("BluePlayer")
        self.red_player = self.find("RedPlayer")

    def update(self) -> None:
        self.update_timers()

        if self.turn_ended:
            self.turn_ended = False
            self.on_turn_ended()

        if not self.current_player:
            if self.turn_end_timer <= 0:
                self.on_next_turn()

    def update_timers(self) -> None:
        self.turn_end_timer -= Time.delta_time
        if self.turn_end_timer < 0:
            self.turn_end_timer = 0

    def end_blue_turn(self) -> None:
        self.current_player = self.red_player

    def end_red_turn(self) -> None:
        self.current_player = self.blue_player

    def on_turn_ended(self) -> None:
        # Start in-between-turns timer
        self.turn_end_timer = self.time_between_turns

        # Set next player
        if self.current_player == self.blue_player:
            self.next_player = self.red_player
        else:
            self.next_player = self.blue_player

        # Unset current player
        self.current_player = None

    def on_next_turn(self) -> None:
        # Set current player
        self.current_player = self.next_player
        self.next_player = None
