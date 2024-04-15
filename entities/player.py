import random

from engine import *

from entities.board import Board
from entities.game_manager import GameManager
from entities.tile import Tile
from entities.skull import Skull
from entities.red_skull import RedSkull
from entities.blue_skull import BlueSkull


class Player(Entity):
    def __init__(self) -> None:
        super().__init__()
        self.game_manager: GameManager | None = None
        self.board: Board | None = None
        self.team = ""
        self.controller = "human"

        self.tile_highlight_color = Color.gray()

        # Computer AI
        self.thinking_timer = 0
        self.thinking_timer_max = 1

        self.focus = Point(999, 999)
        self.possible_tiles = []
        self.target_tile: Tile | None = None

        self.has_focused_tile = False
        self.has_summoned = False

        self.tutorial_step_started = False
        self.left_click_disabled = False
        self.right_click_disabled = False

        self.skull_marked_for_sacrifice: Skull | None = None

    def start(self) -> None:
        self.game_manager = self.find("GameManager")
        self.board = self.find("Board")

    def is_my_turn(self) -> bool:
        return self.game_manager.current_player == self

    def on_turn_start(self) -> None:
        if self.controller == "computer":
            # Reset
            self.thinking_timer = self.thinking_timer_max
            self.focus = Point(999, 999)
            self.target_tile = None
            self.possible_tiles.clear()
            self.has_focused_tile = False
            self.has_summoned = False

            # Get list of possible moves
            for tile in self.board.valid_red_tiles:
                self.possible_tiles.append(tile)

            # Pick a move
            if self.possible_tiles:
                self.target_tile = random.choice(self.possible_tiles)

    def update(self) -> None:
        if not self.is_my_turn():
            return

        self.update_timers()

        if self.controller == "computer":
            self.update_computer_input()
        elif self.controller == "tutorial":
            self.update_tutorial_input()
        else:
            self.focus = Mouse.world_position()
            self.update_human_input()

    def update_timers(self) -> None:
        self.thinking_timer -= Time.delta_time
        if self.thinking_timer <= 0:
            self.thinking_timer = 0

    def can_summon_on_tile(self, tile: Tile) -> bool:
        if self.team == "blue" and tile.blue_can_summon:
            return True
        if self.team == "red" and tile.red_can_summon:
            return True

        return False

    def summon_skull(self, tile: Tile) -> None:
        if self.team == "red":
            skull = RedSkull()
        elif self.team == "blue":
            skull = BlueSkull()
        else:
            Log.error("Not red or blue")
            return

        if self.skull_marked_for_sacrifice:
            self.skull_marked_for_sacrifice.sacrifice()
            self.skull_marked_for_sacrifice = None

        self.scene.entities.add(skull)
        skull.x = tile.x
        skull.y = tile.y + 4
        tile.skull = skull
        skull.tile = tile
        skull.summoned_by_player = True
        skull.get_neighboring_opponents()
        self.game_manager.next_turn_delay = len(skull.neighbors_to_convert) * .3

    def mark_skull_for_sacrifice(self, skull: Skull) -> None:
        self.skull_marked_for_sacrifice = skull
        skull.mark_for_sacrifice()
        self.board.update_valid_tiles_for_sacrifice(skull.tile)
        self.board.set_tile_highlights()

    def unmark_skull_for_sacrifice(self, skull: Skull) -> None:
        self.skull_marked_for_sacrifice = None
        skull.unmark_for_sacrifice()
        self.board.update_valid_tiles_for_summoning()
        self.board.set_tile_highlights()

    def end_turn(self) -> None:
        self.game_manager.turn_ended = True

    def update_human_input(self) -> None:
        if self.skull_marked_for_sacrifice:
            if Mouse.get_right_mouse_down():
                if self.game_manager.is_tutorial:
                    # Force the player to go through with the action in the tutorial
                    return
                self.unmark_skull_for_sacrifice(self.skull_marked_for_sacrifice)
                return

        if not self.left_click_disabled:
            if Mouse.get_left_mouse_down():
                if tile := self.board.hovered_tile:
                    if tile.is_free():
                        if self.can_summon_on_tile(tile):
                            self.summon_skull(tile)
                            self.end_turn()
                            return
                if self.skull_marked_for_sacrifice:
                    self.unmark_skull_for_sacrifice(self.skull_marked_for_sacrifice)
                    return

        if not self.right_click_disabled:
            if Mouse.get_right_mouse_down():
                if tile := self.board.hovered_tile:
                    if skull := tile.skull:
                        if skull.team == self.team:
                            self.mark_skull_for_sacrifice(skull)

    def update_computer_input(self) -> None:
        # Delay when thinking
        if self.thinking_timer > 0:
            return

        # Set focus point on target tile so human player knows what the computer is thinking
        if not self.has_focused_tile:
            self.has_focused_tile = True
            self.thinking_timer = self.thinking_timer_max
            if self.target_tile:
                self.focus = self.target_tile.position()
            return

        # Make move
        if not self.has_summoned:
            self.has_summoned = True
            if self.target_tile:
                self.summon_skull(self.target_tile)
            self.end_turn()

    def update_tutorial_input(self) -> None:
        if self.thinking_timer > 0:
            return

        if self.game_manager.tutorial_step == 1:
            tile = self.board.get_tile(2, -1, -1)
            if self.tutorial_step_started:
                self.tutorial_step_started = False
                self.focus = tile.position()
                self.thinking_timer = 4
            else:
                self.summon_skull(tile)
                self.end_turn()

        if self.game_manager.tutorial_step == 3:
            tile = self.board.get_tile(1, 0, -1)
            if self.tutorial_step_started:
                self.tutorial_step_started = False
                self.focus = tile.position()
                self.thinking_timer = 2
            else:
                self.summon_skull(tile)
                self.end_turn()

        if self.game_manager.tutorial_step in (5, 6):
            if self.board.valid_red_tiles:
                tile = self.board.valid_red_tiles[0]
                if self.tutorial_step_started:
                    self.tutorial_step_started = False
                    self.focus = tile.position()
                    self.thinking_timer = 2
                else:
                    self.summon_skull(tile)
                    self.end_turn()
