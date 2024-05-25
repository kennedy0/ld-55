from __future__ import annotations

import math
import random
from typing import Iterator, Optional, TYPE_CHECKING

from engine import *

if TYPE_CHECKING:
    from entities.tile import Tile
    from entities.game_manager import GameManager


TILE_WIDTH = 14
TILE_HEIGHT = 11


class Board(Entity):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Board"
        self.game_manager: GameManager | None = None

        self.radius = 0
        self.tiles = {}
        self.hovered_tile: Tile | None = None

        self.total_tiles = 0     # Number of tiles in play
        self.enabled_tiles = 0   # Number of tiles that have been enabled
        self.revealed_tiles = 0  # Tiles that have been revealed during the board setup
        self.free_tiles = 0      # Empty tiles that can be played on
        self.blue_tiles = 0      # Tiles claimed by blue
        self.red_tiles = 0       # Tiles claimed by red

        self.new_game_tiles = []  # List of tiles to include when setting up a new game

        self.valid_blue_tiles = []  # List of tiles that are valid summon targets for blue
        self.valid_red_tiles = []   # List of tiles that are valid summon targets for red

        self.blue_start_coordinates = []  # Coordinates that blue can always start on
        self.red_start_coordinates = []   # Coordinates that red can always start on

        self.normal_blue_start_coordinates = [
            (-3, 3, 0),
            (3, 0, -3),
            (0, -3, 3),
        ]
        self.normal_red_start_coordinates = [
            (0, 3, -3),
            (-3, 0, 3),
            (3, -3, 0),
        ]

        self.tutorial_blue_start_coordinates = [(-2, 1, 1)]
        self.tutorial_red_start_coordinates = [(2, -1, -1)]

        self.board_layout = 0
        self.missing_tile_coordinates = [
            [(0, 1, -1), (-1, 0, 1), (1, -1, 0)],
            [(0, 0, 0), (-1, 1, 0), (1, 0, -1), (0, -1, 1)],
            [(-2, 3, -1), (-1, 3, -2), (1, 2, -3), (2, 1, -3), (3, -1, -2), (3, -2, -1), (2, -3, 1), (1, -3, 2), (-1, -2, 3), (-2, -1, 3), (-3, 1, 2), (-3, 2, 1)],
        ]

        self.missing_tile_coordinates_for_tutorial = [
            # Outer border
            (-2, 3, -1), (-1, 3, -2), (1, 2, -3), (2, 1, -3), (3, -1, -2), (3, -2, -1), (2, -3, 1), (1, -3, 2),
            (-1, -2, 3), (-2, -1, 3), (-3, 1, 2), (-3, 2, 1),
            (-3, 3, 0), (0, 3, -3), (3, 0, -3), (3, -3, 0), (0, -3, 3), (-3, 0, 3),

            # Top/bottom strip after
            (-2, 2, 0), (-1, 2, -1), (0, 2, -2), (1, 1, -2), (2, 0, -2),
            (-2, 0, 2), (-1, -1, 2), (0, -2, 2), (1, -2, 1), (2, -2, 0),
        ]

    def start(self) -> None:
        self.game_manager = self.find("GameManager")

    def add_tile(self, tile: Tile) -> None:
        self.tiles[tile.coordinates] = tile

    def set_neighbors(self) -> None:
        for tile in self.iter_tiles():
            q, r, s = tile.coordinates

            if northwest := self.get_tile(q-1, r+1, s):
                tile.northwest = northwest
                tile.neighbors['nw'] = northwest
            if north := self.get_tile(q, r+1, s-1):
                tile.north = north
                tile.neighbors['n'] = north
            if northeast := self.get_tile(q+1, r, s-1):
                tile.northeast = northeast
                tile.neighbors['ne'] = northeast
            if southwest := self.get_tile(q-1, r, s+1):
                tile.southwest = southwest
                tile.neighbors['sw'] = southwest
            if south := self.get_tile(q, r-1, s+1):
                tile.south = south
                tile.neighbors['s'] = south
            if southeast := self.get_tile(q+1, r-1, s):
                tile.northwest = southeast
                tile.neighbors['se'] = southeast

    def move_tiles(self) -> None:
        for tile in self.iter_tiles():
            tile.set_position(self.tile_to_world_position(tile.q, tile.r, tile.s))
            tile.z_depth = -tile.y + 100

    def setup_board_for_new_game(self) -> None:
        self.total_tiles = 0
        self.enabled_tiles = 0
        self.revealed_tiles = 0
        self.free_tiles = 0
        self.blue_tiles = 0
        self.red_tiles = 0
        self.new_game_tiles.clear()
        self.valid_blue_tiles.clear()
        self.valid_red_tiles.clear()

        self.blue_start_coordinates.clear()
        self.red_start_coordinates.clear()

        if self.game_manager.is_tutorial:
            for c in self.tutorial_blue_start_coordinates:
                self.blue_start_coordinates.append(c)
            for c in self.tutorial_red_start_coordinates:
                self.red_start_coordinates.append(c)
        else:
            for c in self.normal_blue_start_coordinates:
                self.blue_start_coordinates.append(c)
            for c in self.normal_red_start_coordinates:
                self.red_start_coordinates.append(c)

        if self.game_manager.is_tutorial:
            coordinates_to_remove = self.missing_tile_coordinates_for_tutorial
        elif self.board_layout in (0, 1, 2):
            coordinates_to_remove = self.missing_tile_coordinates[self.board_layout]
        else:
            coordinates_to_remove = random.choice(self.missing_tile_coordinates)

        for tile in self.iter_tiles():
            tile.enabled = False
            tile.init_sprite()
            if tile.coordinates not in coordinates_to_remove:
                self.new_game_tiles.append(tile)

        self.total_tiles = len(self.new_game_tiles)

    def reveal_tiles(self) -> None:
        self.revealed_tiles = 0
        self.enabled_tiles = 0
        random.shuffle(self.new_game_tiles)
        for i, tile in enumerate(self.new_game_tiles):
            self.enabled_tiles += 1
            tile.reveal(delay=i * .05)

    def tear_down(self) -> None:
        self.total_tiles = 0
        self.enabled_tiles = 0
        self.free_tiles = 0
        self.blue_tiles = 0
        self.red_tiles = 0
        self.new_game_tiles.clear()
        self.valid_blue_tiles.clear()
        self.valid_red_tiles.clear()

        tiles = list(self.iter_tiles())
        random.shuffle(tiles)

        for i, tile in enumerate(tiles):
            tile.clear_highlight()
            if skull := tile.skull:
                skull.kill(delay=i * .05)
            tile.hide(delay=.5 + (i * .05))

    def iter_tiles(self) -> Iterator[Tile]:
        """ Iterate over all tiles. """
        for tile in self.get_tiles(0, 0, 0, self.radius):
            yield tile

    def get_tile(self, q: int, r: int, s: int) -> Optional[Tile]:
        """ Get a single tile. """
        return self.tiles.get((q, r, s))

    def get_tiles(self, q: int, r: int, s: int, radius: int) -> list[Tile]:
        """ Get all tiles within a range of a coordinate. """
        for i in range(q-radius, q+radius+1):
            for j in range(r-radius, r+radius+1):
                for k in range(s-radius, s+radius+1):
                    if i + j + k == 0:
                        yield self.get_tile(i, j, k)

    def set_tile_highlights(self):
        if self.game_manager.tutorial_step == 8:
            for tile in self.iter_tiles():
                tile.clear_highlight()
            return

        if self.game_manager.red_auto_win or self.game_manager.blue_auto_win:
            for tile in self.iter_tiles():
                tile.clear_highlight()
            return

        player = self.game_manager.current_player
        if player:
            color = player.tile_highlight_color
            for tile in self.iter_tiles():
                tile.clear_highlight()
                if player:
                    if player.can_summon_on_tile(tile):
                        tile.set_highlight(color)

    def update_valid_tiles_for_summoning(self) -> None:
        self.valid_blue_tiles.clear()
        self.valid_red_tiles.clear()

        for tile in self.iter_tiles():
            tile.blue_can_summon = False
            tile.red_can_summon = False

            if tile.is_free():
                if tile.coordinates in self.blue_start_coordinates:
                    tile.blue_can_summon = True
                elif tile.coordinates in self.red_start_coordinates:
                    tile.red_can_summon = True
                else:
                    for n in tile.neighbors.values():
                        if s := n.skull:
                            if s.team == "blue":
                                tile.blue_can_summon = True
                            if s.team == "red":
                                tile.red_can_summon = True

                if tile.blue_can_summon:
                    self.valid_blue_tiles.append(tile)
                if tile.red_can_summon:
                    self.valid_red_tiles.append(tile)

        if Engine.debug_mode():
            print(f"Valid tiles for blue:")
            for t in self.valid_blue_tiles:  # type: Tile
                print(f"\t{t.coordinates}")
            print(f"Valid tiles for red:")
            for t in self.valid_red_tiles:  # type: Tile
                print(f"\t{t.coordinates}")

    def update_valid_tiles_for_sacrifice(self, sacrifice_tile: Tile) -> None:
        self.valid_blue_tiles.clear()
        self.valid_red_tiles.clear()

        for tile in self.iter_tiles():
            tile.blue_can_summon = False
            tile.red_can_summon = False

            if tile.is_free() and tile.distance_to(sacrifice_tile) == 2:
                if team := sacrifice_tile.skull.team:
                    if team == "blue" and tile.coordinates not in self.red_start_coordinates:
                        tile.blue_can_summon = True
                        self.valid_blue_tiles.append(tile)
                    if team == "red" and tile.coordinates not in self.blue_start_coordinates:
                        tile.red_can_summon = True
                        self.valid_red_tiles.append(tile)

        if Engine.debug_mode():
            print(f"Valid tiles for blue:")
            for t in self.valid_blue_tiles:  # type: Tile
                print(f"\t{t.coordinates}")
            print(f"Valid tiles for red:")
            for t in self.valid_red_tiles:  # type: Tile
                print(f"\t{t.coordinates}")

    def update_tile_counts(self) -> None:
        self.free_tiles = 0
        self.blue_tiles = 0
        self.red_tiles = 0
        for tile in self.iter_tiles():
            if tile.is_free():
                self.free_tiles += 1
            if skull := tile.skull:
                if skull.team == "blue":
                    self.blue_tiles += 1
                if skull.team == "red":
                    self.red_tiles += 1

    @staticmethod
    def tile_to_world_position(q: int, r: int, s: int) -> Point:
        """ Convert a tile coordinate to world position. """

        x = TILE_WIDTH * (3/2 * q)
        y = TILE_HEIGHT * (((math.sqrt(3)/2) * q) + (math.sqrt(3) * r)) * -1
        return Point(x, y)

    def update(self) -> None:
        # Unset the hovered tile if the mouse moves off of it
        if self.hovered_tile:
            if not self.hovered_tile.mouse_hovering():
                self.hovered_tile = None

    def update_valid_tiles_for_tutorial(self) -> None:
        if self.game_manager.tutorial_step == 4:
            for tile in self.valid_blue_tiles:
                tile.blue_can_summon = False

            self.valid_blue_tiles.clear()

            for coordinate in [(0, 0, 0)]:
                tile = self.get_tile(*coordinate)
                tile.blue_can_summon = True
                self.valid_blue_tiles.append(tile)

        self.set_tile_highlights()

    def blue_has_sacrifice_moves(self) -> bool:
        for tile in self.iter_tiles():
            if skull := tile.skull:
                if skull.team == "blue":
                    for t in self.iter_tiles():
                        if t.is_free():
                            if tile.distance_to(t) == 2:
                                if t.coordinates not in self.red_start_coordinates:
                                    return True
        return False

    def red_has_sacrifice_moves(self) -> bool:
        for tile in self.iter_tiles():
            if skull := tile.skull:
                if skull.team == "red":
                    for t in self.iter_tiles():
                        if t.is_free():
                            if tile.distance_to(t) == 2:
                                if t.coordinates not in self.blue_start_coordinates:
                                    return True
        return False
