from __future__ import annotations

import json
from typing import Self

from engine.content import Content
from engine.data_types.rect import Rect


class BitmapFont:
    """ A texture that contains a sprite for each drawable character.
    The data needed to recreate the original textures are stored in frames.
    """

    __instances: dict[str, Self] = {}

    def __init__(self, content_path: str) -> None:
        """ `content_path` is the path to the bitmap font texture file. """
        self._name = content_path
        self._texture = Content.load_texture(content_path)
        self._character_map: dict[str, Rect] = {}
        self._init_character_map(content_path)

    def __str__(self) -> str:
        return f"BitmapFont({self._name})"

    def __repr__(self) -> str:
        return str(self)

    @classmethod
    def instance(cls, content_path: str) -> Self:
        """ Get or create a new bitmap font.
        This should always be used instead of instantiating creating a new BitmapFont object, because it is expensive.

        `content_path` is the path to the bitmap font texture file.
        """
        # Get font from instance cache if it exists
        if font := cls.__instances.get(content_path):
            return font

        # Create and cache new font
        font = BitmapFont(content_path)
        cls.__instances[content_path] = font
        return font

    def _init_character_map(self, content_path: str) -> None:
        """ Set character positions by reading font data file.
        `content_path` is the path to the bitmap font texture file.
        """
        # Get path to fontdata file
        fontdata_file = Content.with_suffix(content_path, ".fontdata")

        # Make sure fontdata file exists
        if not Content.is_file(fontdata_file):
            raise FileNotFoundError(f"Could not find fontdata file: {fontdata_file}")

        # Read frame data from file
        with Content.open(fontdata_file) as fp:
            font_data = json.load(fp)

        # Create frames from frame data
        for char, glyph_dict in font_data.items():
            bbox = Rect(glyph_dict['x'], glyph_dict['y'], glyph_dict['width'], glyph_dict['height'])
            self._character_map.update({char: bbox})

    def get_source_rect(self, char: str) -> Rect:
        """ Get the source rect for a character. """
        source_rect = self._character_map.get(char)
        if not source_rect:
            raise RuntimeError(f"{self} has no character '{char}'")
        return source_rect
