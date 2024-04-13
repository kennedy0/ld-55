from __future__ import annotations

import math
from typing import Iterator, Optional, TYPE_CHECKING

from engine import *

if TYPE_CHECKING:
    from entities.tile import Tile


TILE_WIDTH = 14
TILE_HEIGHT = 11


class Board(Entity):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Board"
        self.radius = 0
        self.tiles = {}
        self.hovered_tile: Tile | None = None

    def add_tile(self, tile: Tile) -> None:
        self.tiles[tile.coordinates] = tile

    def set_neighbors(self) -> None:
        for tile in self.iter_tiles():
            q, r, s = tile.coordinates

            if northwest := self.get_tile(q-1, r, s+1):
                tile.northwest = northwest
                tile.neighbors.append(northwest)
            if north := self.get_tile(q, r-1, s+1):
                tile.north = north
                tile.neighbors.append(north)
            if northeast := self.get_tile(q+1, r-1, s):
                tile.northeast = northeast
                tile.neighbors.append(northeast)
            if southwest := self.get_tile(q-1, r+1, s):
                tile.southwest = southwest
                tile.neighbors.append(southwest)
            if south := self.get_tile(q, r+1, s-1):
                tile.south = south
                tile.neighbors.append(south)
            if southeast := self.get_tile(q+1, r, s-1):
                tile.northwest = southeast
                tile.neighbors.append(southeast)

    def move_tiles(self) -> None:
        for tile in self.iter_tiles():
            tile.set_position(self.tile_to_world_position(tile.q, tile.r, tile.s))
            tile.z_depth = -tile.y + 100

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
