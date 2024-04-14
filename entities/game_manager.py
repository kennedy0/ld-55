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

        # References
        self.board: Board | None = None
        self.main_menu_entities: list[Entity] = []

        # Game start
        self.board_setup_finished = False

        # Current player
        self.current_player: Player | None = None
        self.next_player: Player | None = None
        self.blue_player: BluePlayer | None = None
        self.red_player: RedPlayer | None = None

        # Game state
        self.game_started = False
        self.game_ended = False
        self.turn_ended = False

        # Between turns timer
        self.next_turn_delay = 0
        self.time_between_turns = .3
        self.turn_end_timer = 0

    def start(self) -> None:
        self.board = self.find("Board")
        self.blue_player = self.find("BluePlayer")
        self.red_player = self.find("RedPlayer")

        for entity in self.scene.entities:
            if "MainMenu" in entity.tags:
                self.main_menu_entities.append(entity)

    def update(self) -> None:
        if not self.game_started:
            return

        self.update_timers()

        # Board setup
        if not self.board_setup_finished:
            if self.board.revealed_tiles == self.board.enabled_tiles:
                self.board_setup_finished = True
                self.on_board_setup_finished()
            return

        # Check for no valid turns for current player - skip turn
        if not self.turn_ended:
            if self.current_player == self.blue_player and len(self.board.valid_blue_tiles) == 0:
                Log.info("No valid moves for blue - skipping turn")
                self.turn_ended = True
            elif self.current_player == self.red_player and len(self.board.valid_red_tiles) == 0:
                Log.info("No valid moves for red - skipping turn")
                self.turn_ended = True

        # End Turn
        if self.turn_ended:
            self.turn_ended = False
            self.on_turn_ended()

        # Start Turn
        if not self.current_player:
            if self.turn_end_timer <= 0:
                self.check_for_game_end()
                if not self.game_ended:
                    self.on_turn_start()

    def update_timers(self) -> None:
        self.turn_end_timer -= Time.delta_time
        if self.turn_end_timer < 0:
            self.turn_end_timer = 0

    def start_game(self) -> None:
        self.game_started = True
        self.game_ended = False
        self.hide_main_menu()

        # Do board setup
        self.board_setup_finished = False
        self.board.setup_board_for_new_game()
        self.board.reveal_tiles()

    def on_board_setup_finished(self) -> None:
        # Board updates
        self.board.update_tile_counts()
        self.board.update_valid_tiles_for_summoning()
        self.board.set_tile_highlights()

        # Set first player
        self.next_player = self.blue_player

    def on_turn_ended(self) -> None:
        # Start in-between-turns timer
        self.turn_end_timer = self.time_between_turns + self.next_turn_delay

        # Set next player
        if self.current_player == self.blue_player:
            self.next_player = self.red_player
        else:
            self.next_player = self.blue_player

        # Unset current player
        self.current_player = None

        # Board Updates
        self.board.set_tile_highlights()

    def on_turn_start(self) -> None:
        # Set current player
        self.current_player = self.next_player
        self.next_player = None

        # Board Updates
        self.board.update_valid_tiles_for_summoning()
        self.board.set_tile_highlights()

    def on_game_end(self) -> None:
        self.show_main_menu()

    def hide_main_menu(self) -> None:
        for entity in self.main_menu_entities:
            entity.active = False

    def show_main_menu(self) -> None:
        for entity in self.main_menu_entities:
            entity.active = True

    def check_for_game_end(self) -> None:
        self.board.update_tile_counts()

        if self.board.free_tiles == 0:
            Log.info("No more free tiles")
            self.game_ended = True
        if len(self.board.valid_blue_tiles) + len(self.board.valid_red_tiles) == 0:
            Log.info("No more valid tiles for either player")
            self.game_ended = True

        if self.game_ended:
            self.game_started = False
            Log.info("Game Ended!")
