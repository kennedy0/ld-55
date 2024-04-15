from __future__ import annotations

from typing import TYPE_CHECKING

import sdl2

from engine import *

if TYPE_CHECKING:
    from entities.player import Player
    from entities.blue_player import BluePlayer
    from entities.red_player import RedPlayer
    from entities.board import Board
    from entities.ui_game_ended import UiGameEnded
    from entities.main_menu_entity import MainMenuEntity
    from entities.ui_tutorial_text import UiTutorialText


class GameManager(Entity):
    def __init__(self) -> None:
        super().__init__()
        self.name = "GameManager"

        # References
        self.board: Board | None = None
        self.ui_game_ended: UiGameEnded | None = None
        self.tutorial_text: UiTutorialText | None = None
        self.main_menu_entities: list[MainMenuEntity] = []
        self.game_ui_entities: list[Entity] = []

        # Game start
        self.board_setup_finished = False
        self.board_teardown_started = False
        self.board_teardown_finished = False

        # Current player
        self.current_player: Player | None = None
        self.next_player: Player | None = None
        self.blue_player: BluePlayer | None = None
        self.red_player: RedPlayer | None = None

        # Game state
        self.game_started = False
        self.game_ended = False
        self.turn_ended = False
        self.score_calculated = False

        # Between turns timer
        self.next_turn_delay = 0
        self.time_between_turns = .3
        self.turn_end_timer = 0

        # Forfeit
        self.forfeit_timer = 0
        self.forfeit_max_time = 1

        # Tutorial
        self.is_tutorial = False
        self.tutorial_step = 0
        self.tutorial_step_started = False
        self.tutorial_delay_timer = 0
        self.tutorial_game_end_message = ""
        self.tutorial_complete = False

    def start(self) -> None:
        self.board = self.find("Board")
        self.ui_game_ended = self.find("UiGameEnded")
        self.tutorial_text = self.find("UiTutorialText")
        self.blue_player = self.find("BluePlayer")
        self.red_player = self.find("RedPlayer")

        for entity in self.scene.entities:
            if "MainMenu" in entity.tags:
                self.main_menu_entities.append(entity)
                entity.active = False
            if "GameUI" in entity.tags:
                self.game_ui_entities.append(entity)

        self.hide_game_ui()

    def update(self) -> None:
        if self.game_ended:
            self.update_game_end()
            return

        if not self.game_started:
            return

        self.update_timers()

        # Board setup
        if not self.board_setup_finished:
            if self.board.revealed_tiles == self.board.enabled_tiles:
                self.board_setup_finished = True
                self.on_board_setup_finished()
            return

        # Forfeit
        if Keyboard.get_key(sdl2.SDLK_ESCAPE):
            self.forfeit_timer += Time.delta_time
            if self.forfeit_timer > self.forfeit_max_time:
                Log.info("Forfeited")
                self.forfeit_timer = 0
                self.game_ended = True
                if self.is_tutorial:
                    self.tutorial_complete = True
                    self.tutorial_game_end_message = "Tutorial\nCancelled"
                self.check_for_game_end()
                return
        else:
            self.forfeit_timer = 0

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

        if self.is_tutorial:
            self.update_tutorial()

    def update_timers(self) -> None:
        self.turn_end_timer -= Time.delta_time
        if self.turn_end_timer < 0:
            self.turn_end_timer = 0

        self.tutorial_delay_timer -= Time.delta_time
        if self.tutorial_delay_timer < 0:
            self.tutorial_delay_timer = 0

    def start_game(self) -> None:
        Log.info("Start Game!")
        self.blue_player.left_click_disabled = False
        self.blue_player.right_click_disabled = False
        if self.is_tutorial:
            Log.info("Tutorial mode")
            self.tutorial_complete = False
            self.tutorial_step = 0
            self.tutorial_step_started = True
            self.tutorial_game_end_message = "Tutorial\nComplete"
            self.tutorial_text.text.text = ""

        self.game_started = True
        self.game_ended = False
        self.turn_ended = False
        self.score_calculated = False
        self.hide_main_menu()

        # Do board setup
        self.board_setup_finished = False
        self.board.setup_board_for_new_game()
        self.board.reveal_tiles()

    def on_board_setup_finished(self) -> None:
        Log.info("Board setup finished")

        # UI
        self.show_game_ui()

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

        self.current_player.on_turn_start()

    def show_game_ui(self) -> None:
        for entity in self.game_ui_entities:
            entity.active = True

        if self.is_tutorial:
            self.find("UiScore").active = False
            self.find("UiTutorialText").active = True

    def hide_game_ui(self) -> None:
        for entity in self.game_ui_entities:
            entity.active = False

        if self.is_tutorial:
            self.find("UiTutorialText").active = False

    def show_main_menu(self) -> None:
        for i, entity in enumerate(self.main_menu_entities):
            entity.show(delay=i * .2)

    def hide_main_menu(self) -> None:
        for i, entity in enumerate(self.main_menu_entities):
            entity.hide(delay=i * .5)

    def check_for_game_end(self) -> None:
        # Force an update of the tile counts
        self.board.update_tile_counts()

        # Game never ends automatically in tutorial
        if self.is_tutorial and not self.tutorial_complete:
            return

        # Check end conditions
        if self.board.free_tiles == 0:
            Log.info("No more free tiles")
            self.game_ended = True
        if len(self.board.valid_blue_tiles) + len(self.board.valid_red_tiles) == 0:
            Log.info("No more valid tiles for either player")
            self.game_ended = True

        # Reset variables
        if self.game_ended:
            Log.info("Game Ended!")
            self.game_started = False
            self.board_setup_finished = False
            self.board_teardown_started = False
            self.board_teardown_finished = False
            self.score_calculated = False
            self.current_player = None
            self.next_player = None
            self.blue_player.left_click_disabled = False
            self.blue_player.right_click_disabled = False

    def update_game_end(self) -> None:
        # Calculate final score
        if not self.score_calculated:
            self.score_calculated = True
            blue_score = self.board.blue_tiles
            red_score = self.board.red_tiles
            if self.is_tutorial:
                self.ui_game_ended.set_tutorial(self.tutorial_game_end_message)
            elif blue_score > red_score:
                self.ui_game_ended.set_blue()
            elif red_score > blue_score:
                self.ui_game_ended.set_red()
            else:
                self.ui_game_ended.set_draw()

        # Show the winner
        if self.ui_game_ended.is_animating:
            return
        self.hide_game_ui()

        # Tear down the board
        if not self.board_teardown_started:
            Log.info("Tearing down board")
            self.board_teardown_started = True
            self.board.tear_down()
        if not self.board_teardown_finished:
            if self.board.revealed_tiles == 0:
                Log.info("Board teardown finished")
                self.board_teardown_finished = True
            return

        # Donezo
        self.game_ended = False

        # Show the main menu
        Log.info("Show Main Menu")
        self.show_main_menu()

    def update_tutorial(self) -> None:
        if self.tutorial_step == 0:
            self.blue_player.right_click_disabled = True
            if self.tutorial_step_started:
                self.tutorial_step_started = False
                self.tutorial_text.show_text("Summon a spirit")
            else:
                # Conditions to proceed
                if self.current_player == self.red_player:
                    self.next_tutorial_step()

        if self.tutorial_step == 1:
            if self.tutorial_step_started:
                self.tutorial_step_started = False
                self.red_player.tutorial_step_started = True
                self.tutorial_text.show_text("Now I summon")
            else:
                # Conditions to proceed
                if self.current_player == self.blue_player:
                    self.next_tutorial_step()

        if self.tutorial_step == 2:
            if self.tutorial_step_started:
                self.tutorial_step_started = False
                self.tutorial_text.show_text("Summon next to allies")
            else:
                # Conditions to proceed
                if self.current_player == self.red_player:
                    self.next_tutorial_step()

        if self.tutorial_step == 3:
            if self.tutorial_step_started:
                self.tutorial_step_started = False
                self.red_player.tutorial_step_started = True
            else:
                # Conditions to proceed
                if self.current_player == self.blue_player:
                    self.next_tutorial_step()

        if self.tutorial_step == 4:
            if self.tutorial_step_started:
                self.tutorial_step_started = False
                self.tutorial_text.show_text("Turn opponents into allies")
                self.board.update_valid_tiles_for_tutorial()
            else:
                # Conditions to proceed
                if self.current_player == self.red_player:
                    self.next_tutorial_step()

        if self.tutorial_step == 5:
            if self.tutorial_step_started:
                self.tutorial_step_started = False
                self.red_player.tutorial_step_started = True
                self.tutorial_text.show_text("You are vulnerable too")
            else:
                # Conditions to proceed
                if self.current_player == self.blue_player:
                    self.next_tutorial_step()

        if self.tutorial_step == 6:
            if self.tutorial_step_started:
                self.tutorial_step_started = False
                self.red_player.tutorial_step_started = True
                self.tutorial_text.show_text("Summon the most spirits to win")
            else:
                # Conditions to proceed
                if self.board.free_tiles == 0:
                    self.next_tutorial_step()

        if self.tutorial_step == 7:
            if self.tutorial_step_started:
                self.tutorial_step_started = False
                self.blue_player.left_click_disabled = True
                self.blue_player.right_click_disabled = False
                self.tutorial_text.show_text("One final lesson")
                coordinates = [(-1, 1, 0), (-1, 0, 1), (0, 1, -1), (0, 0, 0), (0, -1, 1)]
                for i, c in enumerate(coordinates):
                    if tile := self.board.get_tile(*c):
                        if skull := tile.skull:
                            skull.kill(i * .5)
                coordinates = [(1, 0, -1), (1, -1, 0), (2, -1, -1)]
                for c in coordinates:
                    if tile := self.board.get_tile(*c):
                        if skull := tile.skull:
                            if skull.team == "blue":
                                skull.convert()
            else:
                # Conditions to proceed
                self.board.update_tile_counts()
                if self.board.free_tiles == 5:
                    self.next_tutorial_step()

        if self.tutorial_step == 8:
            if self.tutorial_step_started:
                self.tutorial_step_started = False
                self.tutorial_text.show_text("Sacrifice a spirit (right-click)")
            else:
                # Conditions to proceed
                if self.blue_player.skull_marked_for_sacrifice:
                    self.next_tutorial_step()

        if self.tutorial_step == 9:
            self.blue_player.left_click_disabled = False
            if self.tutorial_step_started:
                self.tutorial_step_started = False
                self.tutorial_text.show_text("Summon from afar")
            else:
                # Conditions to proceed
                if self.current_player == self.red_player:
                    self.next_tutorial_step()

        if self.tutorial_step == 10:
            if self.tutorial_step_started:
                self.game_ended = True
                self.tutorial_complete = True
                self.tutorial_game_end_message = "Tutorial\nComplete"
                self.tutorial_text.show_text("")
                self.check_for_game_end()

    def next_tutorial_step(self) -> None:
        self.tutorial_step += 1
        self.tutorial_step_started = True

    def tutorial_delay(self, delay: float) -> None:
        self.tutorial_delay_timer = delay
