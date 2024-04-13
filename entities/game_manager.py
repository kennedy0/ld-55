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
        self.blue_player: BluePlayer | None = None
        self.red_player: RedPlayer | None = None

        self.turn_ended = False

    def start(self) -> None:
        self.blue_player = self.find("BluePlayer")
        self.red_player = self.find("RedPlayer")

    def update(self) -> None:
        # Switch turns
        if self.turn_ended:
            self.turn_ended = False
            if self.current_player == self.blue_player:
                self.current_player = self.red_player
            else:
                self.current_player = self.blue_player

    def end_blue_turn(self) -> None:
        self.current_player = self.red_player

    def end_red_turn(self) -> None:
        self.current_player = self.blue_player
