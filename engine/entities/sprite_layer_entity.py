from __future__ import annotations

from math import ceil, floor
from typing import TYPE_CHECKING

from engine.data_types.point import Point
from engine.entity import Entity
from engine.sprite import Sprite

if TYPE_CHECKING:
    from engine.camera import Camera


class SpriteLayerEntity(Entity):
    """ An entity that contains a single non-collidable sprite. """
    def __init__(self) -> None:
        super().__init__()
        self._sprite = Sprite.empty()
        self._repeat_x = False
        self._repeat_y = False
        self._tile_positions: dict[str, list[Point]] = {}
        self._cached_camera_positions: dict[str, Point] = {}

    @property
    def sprite(self) -> Sprite:
        """ The sprite to draw. """
        return self._sprite

    @sprite.setter
    def sprite(self, value: Sprite) -> None:
        self._sprite = value

    @property
    def repeat_x(self) -> bool:
        """ Whether to repeat the sprite on the X axis. """
        return self._repeat_x

    @repeat_x.setter
    def repeat_x(self, value: bool) -> None:
        self._repeat_x = value

    @property
    def repeat_y(self) -> bool:
        """ Whether to repeat the sprite on the Y axis. """
        return self._repeat_y

    @repeat_y.setter
    def repeat_y(self, value: bool) -> None:
        self._repeat_y = value

    def draw(self, camera: Camera) -> None:
        # Don't draw if there is no sprite set
        if not self.sprite:
            return

        # Cache tile positions if the camera position has changed
        last_camera_position = self._cached_camera_positions.get(camera.name)
        if last_camera_position is None or last_camera_position != camera.position():
            self._cache_tile_positions(camera)
            self._cached_camera_positions[camera.name] = camera.position()

        # Draw each tile
        for position in self._tile_positions[camera.name]:
            self.sprite.draw(camera, position)

    def _cache_tile_positions(self, camera: Camera) -> None:
        """ Calculate and cache a list of positions to draw the sprite at. """
        self._tile_positions[camera.name] = []

        # Calculate number of tiles needed on each axis
        if self.repeat_x:
            x_tiles = ceil(camera.resolution[0] / self.sprite.width()) + 1
        else:
            x_tiles = 1

        if self.repeat_y:
            y_tiles = ceil(camera.resolution[1] / self.sprite.height()) + 1
        else:
            y_tiles = 1

        # Use the top-left corner of the camera rect to figure out the starting position for tiles
        camera_x = floor(camera.rect().left() / self.sprite.width()) * self.sprite.width()
        camera_y = floor(camera.rect().top() / self.sprite.height()) * self.sprite.height()

        # Calculate the position for each tile
        for j in range(y_tiles):
            for i in range(x_tiles):
                # Get tile position
                if self.repeat_x:
                    x = camera_x + self.sprite.width() * i
                else:
                    x = self.x

                if self.repeat_y:
                    y = camera_y + self.sprite.height() * j
                else:
                    y = self.y

                # Add to draw position list
                self._tile_positions[camera.name].append(Point(x, y))
