from __future__ import annotations

from math import floor
from typing import Self, TYPE_CHECKING

import sdl2

from engine.data_types.blend_mode import BlendMode
from engine.data_types.point import Point
from engine.internal_utilities import geometry_utils
from engine.renderer import Renderer

if TYPE_CHECKING:
    from engine.camera import Camera
    from engine.data_types.color import Color
    from engine.data_types.circle import Circle


class Rect:
    """ A 2D rectangle. """
    def __init__(self, x: int, y: int, width: int, height: int) -> None:
        self._x = floor(x)
        self._y = floor(y)
        self._width = int(width)
        self._height = int(height)

    def __str__(self) -> str:
        return f"Rect(x={self.x}, y={self.y}, width={self.width}, height={self.height})"

    def __repr__(self) -> str:
        return str(self)

    @property
    def x(self) -> int:
        """ The X position of the top-left corner of the rectangle. """
        return self._x

    @property
    def y(self) -> int:
        """ The Y position of the top-left corner of the rectangle. """
        return self._y

    @property
    def width(self) -> int:
        """ The width of the rectangle. """
        return self._width

    @property
    def height(self) -> int:
        """ The height of the rectangle. """
        return self._height

    @classmethod
    def empty(cls) -> Self:
        """ Returns a rectangle with x=0, y=0, width=0, height=0. """
        return cls(0, 0, 0, 0)

    def top(self) -> int:
        """ The Y position of the top edge of the rectangle. """
        return self.y

    def bottom(self) -> int:
        """ The Y position of the bottom edge of the rectangle. """
        return self.y + self.height - 1

    def left(self) -> int:
        """ The X position of the left edge of the rectangle. """
        return self.x

    def right(self) -> int:
        """ The X position of the right edge of the rectangle. """
        return self.x + self.width - 1

    def position(self) -> Point:
        """ The position of the top-left corner of the rectangle. """
        return Point(self.x, self.y)

    def size(self) -> Point:
        """ The width and height of the rectangle. """
        return Point(self.width, self.height)

    def center(self) -> Point:
        """ The center point of the rectangle. """
        return self.position() + (self.size() / 2)

    def top_left(self) -> Point:
        """ The top-left corner of the rectangle. """
        return Point(self.left(), self.top())

    def top_right(self) -> Point:
        """ The top-right corner of the rectangle. """
        return Point(self.right(), self.top())

    def bottom_left(self) -> Point:
        """ The bottom-left corner of the rectangle. """
        return Point(self.left(), self.bottom())

    def bottom_right(self) -> Point:
        """ The bottom-right corner of the rectangle. """
        return Point(self.right(), self.bottom())

    def contains_point(self, point: Point) -> bool:
        """ Check if a point is inside the rectangle. """
        return self.left() <= point.x <= self.right() and self.top() <= point.y <= self.bottom()

    def intersects_rect(self, other: Rect) -> bool:
        """ Check if this rectangle intersects another. """
        return geometry_utils.rect_intersects_rect(self, other)

    def intersects_circle(self, circle: Circle) -> bool:
        """ Check if this rectangle intersects a circle. """
        return geometry_utils.rect_intersects_circle(self, circle)

    def to_sdl_rect(self) -> sdl2.SDL_Rect:
        """ Return a copy of the rect as an SDL_Rect. """
        return sdl2.SDL_Rect(self.x, self.y, self.width, self.height)

    def draw(self, camera: Camera, color: Color, solid: bool = False) -> None:
        """ Draw the rectangle. """
        position = camera.world_to_render_position(self.position())
        rect = Rect(position.x, position.y, self.width, self.height)

        if solid:
            Renderer.set_render_draw_blend_mode(BlendMode.BLEND)
            Renderer.draw_rect_solid(rect, color)
        else:
            Renderer.set_render_draw_blend_mode(BlendMode.BLEND)
            Renderer.draw_rect_outline(rect, color)
            Renderer.clear_render_draw_blend_mode()
