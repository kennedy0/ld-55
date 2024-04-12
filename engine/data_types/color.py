from __future__ import annotations

import colorsys
import random
import re
from typing import Self, Optional

from engine.log import Log
from engine.utilities import pmath


_HEX_COLOR_RE = re.compile(r"^#(?P<r>[0-9a-f]{2})(?P<g>[0-9a-f]{2})(?P<b>[0-9a-f]{2})$", re.I)


class Color:
    """ A 32-bit color. """
    def __init__(self, r: int, g: int, b: int, a: int = 255):
        self._r = int(pmath.clamp(r, 0, 255))
        self._g = int(pmath.clamp(g, 0, 255))
        self._b = int(pmath.clamp(b, 0, 255))
        self._a = int(pmath.clamp(a, 0, 255))

    def __str__(self) -> str:
        return f"Color({self.r}, {self.g}, {self.b}, {self.a})"

    def __repr__(self) -> str:
        return str(self)

    def __len__(self):
        return self.to_tuple().__len__()

    def __getitem__(self, item):
        return self.to_tuple().__getitem__(item)

    def __iter__(self):
        return iter(self.to_tuple())
    
    @property
    def r(self) -> int:
        return self._r

    @r.setter
    def r(self, value: int) -> None:
        self._r = value

    @property
    def g(self) -> int:
        return self._g

    @g.setter
    def g(self, value: int) -> None:
        self._g = value

    @property
    def b(self) -> int:
        return self._b

    @b.setter
    def b(self, value: int) -> None:
        self._b = value

    @property
    def a(self) -> int:
        return self._a

    @a.setter
    def a(self, value: int) -> None:
        self._a = value

    def to_tuple(self) -> tuple[int, int, int, int]:
        """ Return a copy of the color as a tuple. """
        return self.r, self.g, self.b, self.a

    @classmethod
    def black(cls) -> Color:
        return Color(0, 0, 0, 255)

    @classmethod
    def white(cls) -> Color:
        return Color(255, 255, 255, 255)

    @classmethod
    def gray(cls) -> Color:
        return Color(128, 128, 128, 255)

    @classmethod
    def red(cls) -> Color:
        return Color(255, 0, 0, 255)

    @classmethod
    def green(cls) -> Color:
        return Color(0, 255, 0, 255)

    @classmethod
    def blue(cls) -> Color:
        return Color(0, 0, 255, 255)

    @classmethod
    def cyan(cls) -> Color:
        return Color(0, 255, 255, 255)

    @classmethod
    def magenta(cls) -> Color:
        return Color(255, 0, 255, 255)

    @classmethod
    def yellow(cls) -> Color:
        return Color(255, 255, 0, 255)

    @classmethod
    def orange(cls) -> Color:
        return Color(255, 128, 0, 255)

    @classmethod
    def transparent(cls) -> Color:
        return Color(0, 0, 0, 0)

    @classmethod
    def random(cls, saturation: Optional[float] = None, brightness: Optional[float] = None) -> Self:
        """ Generates a random color.

        Saturation and brightness can be specified (0-1 range) to prevent those values from being randomly generated.
        Allowing randomness in saturation and brightness often produces muddy results.

        Alpha is always 255.
        """
        # Set HSV values
        hue = random.random()

        if saturation:
            saturation = pmath.clamp(saturation, 0.0, 1.0)
        else:
            saturation = random.random()

        if brightness:
            brightness = pmath.clamp(brightness, 0.0, 1.0)
        else:
            brightness = random.random()

        # Convert to color
        color = cls.hsv(hue, saturation, brightness)
        return color

    @classmethod
    def lerp(cls, color_a: Color, color_b: Color, t: float) -> Self:
        """ Linearly interpolate between 2 colors. """
        r = int(pmath.lerp(color_a.r, color_b.r, t))
        g = int(pmath.lerp(color_a.g, color_b.g, t))
        b = int(pmath.lerp(color_a.b, color_b.b, t))
        a = int(pmath.lerp(color_a.a, color_b.a, t))
        return cls(r, g, b, a)

    @classmethod
    def hsv(cls, h: float, s: float, v: float) -> Self:
        """ Create a color from HSV values.
        HSV values are 0-1 range.
        Alpha will always be 255.
        """
        r, g, b = cls.hsv_to_rgb(h, s, v)
        return cls(r, g, b)

    @staticmethod
    def hsv_to_rgb(h: float, s: float, v: float) -> tuple[int, int, int]:
        """ Convert HSV values to RGB values.
        Hue value is 0-1 range, but wraps around if greater than 1.
        Saturation and value are 0-1 range.
        RGB values are 0-255 range.
        """
        # Clamp HSV to 0-1 range
        h = h % 1.0
        h = pmath.clamp(h, 0.0, 1.0)
        s = pmath.clamp(s, 0.0, 1.0)
        v = pmath.clamp(v, 0.0, 1.0)

        # Convert to RGB float values
        r, g, b = colorsys.hsv_to_rgb(h, s, v)

        # Convert to RGB int values
        r = int(r * 255)
        g = int(g * 255)
        b = int(b * 255)

        return r, g, b

    @classmethod
    def from_hex(cls, hex_code: str) -> Self:
        """ Create a color from a hex code.

        Hex code must be in the format: #RRGGBB
        Alpha will always be 255.
        """
        match = _HEX_COLOR_RE.match(hex_code)
        if not match:
            color = cls.black()
            Log.error(f"Invalid color hex code: {hex_code}; Defaulting to {color}")
            return color

        r_hex = match.group('r')
        g_hex = match.group('g')
        b_hex = match.group('b')

        r = int(f"0x{r_hex}", 0)
        g = int(f"0x{g_hex}", 0)
        b = int(f"0x{b_hex}", 0)

        return cls(r, g, b)

    @classmethod
    def from_int(cls, value: int) -> Self:
        """ Create a color from an integer value.

        The integer value is assumed to be the base-10 of a hex code.
        """
        hex_code = f"#{value:06x}"
        return cls.from_hex(hex_code)
