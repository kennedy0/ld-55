from __future__ import annotations

from typing import Optional, TYPE_CHECKING

from engine.bitmap_font import BitmapFont
from engine.content import Content
from engine.data_types.color import Color
from engine.data_types.point import Point
from engine.data_types.rect import Rect
from engine.glyph import Glyph
from engine.renderer import Renderer
from engine.text_effect import TextEffect
from engine.utilities import pmath

if TYPE_CHECKING:
    from engine.camera import Camera


ALIGN_CENTER = 0
ALIGN_LEFT = 1
ALIGN_RIGHT = 2
ALIGN_TOP = 3
ALIGN_BOTTOM = 4


class Text:
    """ Displays a string of text using a bitmap font. """
    def __init__(self, content_path: str) -> None:
        """ `content_path` is the path to the bitmap font texture file. """
        self._texture = Content.load_texture(content_path)
        self._font = BitmapFont.instance(content_path)
        self._text = ""
        self._width = 0
        self._height = 0
        self._word_wrap = False
        self._max_line_width = 0
        self._typewriter_mode = False
        self._visible_characters = 0
        self._color = None
        self._opacity = 255

        # List of characters to be rendered in the text string
        self._glyphs: list[Glyph] = []

        # Text alignment
        self._horizontal_alignment = ALIGN_LEFT
        self._vertical_alignment = ALIGN_TOP

    def __str__(self) -> str:
        character_limit = 25
        if len(self.text) > character_limit:
            return f"Text({self.text[:character_limit] + '...'})"
        else:
            return f"Text({self.text})"

    def __repr__(self) -> str:
        return str(self)

    @property
    def text(self) -> str:
        """ The text to display. """
        return self._text

    @text.setter
    def text(self, value: str) -> None:
        if value == self._text:
            return

        if not isinstance(value, str):
            value = str(value)

        self._text = value
        self._update_characters()

    # noinspection DuplicatedCode
    @property
    def offset_x(self) -> int:
        """ The pixel difference between the anchor point of the text and the left edge of the text.
        With the default left horizontal alignment this will be zero, but other alignments may push it negative.
        """
        if self._horizontal_alignment == ALIGN_LEFT:
            return 0
        elif self._horizontal_alignment == ALIGN_CENTER:
            return int(self.width / 2) * -1
        elif self._horizontal_alignment == ALIGN_RIGHT:
            return self.width * -1

    # noinspection DuplicatedCode
    @property
    def offset_y(self) -> int:
        """ The pixel difference between the anchor point of the text and the top edge of the text.
        With the default top vertical alignment this will be zero, but other alignments may push it negative.
        """
        if self._vertical_alignment == ALIGN_TOP:
            return 0
        elif self._vertical_alignment == ALIGN_CENTER:
            return int(self.height / 2) * -1
        elif self._vertical_alignment == ALIGN_BOTTOM:
            return self.height * -1

    @property
    def width(self) -> int:
        """ The width of the text. """
        return self._width

    @property
    def height(self) -> int:
        """ The height of the text. """
        return self._height

    @property
    def word_wrap(self) -> bool:
        """ If true, enables word wrap mode.
        In word wrap mode, the 'max_line_width' parameter controls the maximum width that a line can be before a line
        break is created.
        """
        return self._word_wrap

    @word_wrap.setter
    def word_wrap(self, value: bool) -> None:
        self._word_wrap = value
        self._update_characters()

    @property
    def max_line_width(self) -> int:
        """ In word wrap mode, this controls the maximum length a line can be before a line break is created. """
        return self._max_line_width

    @max_line_width.setter
    def max_line_width(self, value: int) -> None:
        self._max_line_width = value
        self._update_characters()

    @property
    def typewriter_mode(self) -> bool:
        """ If true, enables typewriter mode.
        In typewriter mode, the 'visible_characters' parameter controls the number of characters that are visible.
        """
        return self._typewriter_mode

    @typewriter_mode.setter
    def typewriter_mode(self, value: bool) -> None:
        self._typewriter_mode = value

    @property
    def visible_characters(self) -> int:
        """ In typewriter mode, this controls the number of characters that are visible.
        Increasing the value over time creates a typewriter effect.
        """
        return self._visible_characters

    @visible_characters.setter
    def visible_characters(self, value: int) -> None:
        self._visible_characters = value

    @property
    def color(self) -> Optional[Color]:
        """ Adds a color tint to the text. """
        return self._color

    @color.setter
    def color(self, value: Optional[Color]) -> None:
        self._color = value

    @property
    def opacity(self) -> int:
        """ The opacity of the text. """
        return self._opacity

    @opacity.setter
    def opacity(self, value: int) -> None:
        """ Opacity can be set as a 0-255 int value. """
        self._opacity = pmath.clamp(value, 0, 255)

    def align_horizontal_left(self) -> None:
        """ Left align. """
        self._horizontal_alignment = ALIGN_LEFT
        self._update_characters()

    def align_horizontal_center(self) -> None:
        """ Center align. """
        self._horizontal_alignment = ALIGN_CENTER
        self._update_characters()

    def align_horizontal_right(self) -> None:
        """ Right align. """
        self._horizontal_alignment = ALIGN_RIGHT
        self._update_characters()

    def align_vertical_top(self) -> None:
        """ Top align. """
        self._vertical_alignment = ALIGN_TOP
        self._update_characters()

    def align_vertical_center(self) -> None:
        """ Center align. """
        self._vertical_alignment = ALIGN_CENTER
        self._update_characters()

    def align_vertical_bottom(self) -> None:
        """ Bottom align. """
        self._vertical_alignment = ALIGN_BOTTOM
        self._update_characters()

    def draw(self, camera: Camera, position: Point) -> None:
        """ Draw the text at a given position. """
        # Convert world position to screen position
        anchor_position = camera.world_to_render_position(position)

        # Apply tint
        if self.color:
            Renderer.set_texture_color_mod(self._texture, self.color)

        # Apply opacity
        if self.opacity != 255:
            Renderer.set_texture_alpha_mod(self._texture, self.opacity)

        # Draw each glyph
        for i, glyph in enumerate(self._glyphs):
            # Stop drawing if we are in typewriter mode and we've reached the limit of visible characters
            if self.typewriter_mode and i >= self.visible_characters:
                break

            # Draw the glyph
            self._draw_glyph(glyph, anchor_position)

        # Clear tint
        if self.color:
            Renderer.clear_texture_color_mod(self._texture)

        # Clear tint and opacity
        if self.opacity != 255:
            Renderer.clear_texture_alpha_mod(self._texture)

    def _draw_glyph(self, glyph: Glyph, anchor_position: Point) -> None:
        """ Draw a glyph. """
        # Set destination
        glyph_position = self._get_glyph_position(glyph, anchor_position)
        destination = Rect(glyph_position.x, glyph_position.y, glyph.source_rect.width, glyph.source_rect.height)

        # Set color
        glyph_color = self._get_glyph_color(glyph)
        if glyph_color:
            Renderer.set_texture_color_mod(self._texture, glyph_color)

        # Render texture
        Renderer.copy(
            texture=self._texture,
            source_rect=glyph.source_rect,
            destination_rect=destination,
            rotation_angle=0,
            rotation_center=None,
            flip=0
        )

        # Clear color
        if glyph_color:
            Renderer.clear_texture_color_mod(self._texture)

    def _get_glyph_position(self, glyph: Glyph, anchor_position: Point) -> Point:
        """ Calculate the position that the glyph should be drawn at. """
        # Add the character offset to the text anchor position
        glyph_x = anchor_position.x + glyph.destination_offset_x
        glypy_y = anchor_position.y + glyph.destination_offset_y

        # Add text effect offset
        if glyph.tag:
            if text_effect := TextEffect.get(glyph.tag):
                glyph_offset = text_effect.glyph_offset(glyph)
                glyph_x += glyph_offset.x
                glypy_y += glyph_offset.y

        return Point(glyph_x, glypy_y)

    def _get_glyph_color(self, glyph: Glyph) -> Optional[Color]:
        """ Get the color that the glyph should be drawn as. """
        if glyph.tag:
            if text_effect := TextEffect.get(glyph.tag):
                return text_effect.glyph_color(glyph)

        return None

    def _get_glyph_opacity(self, glyph: Glyph) -> Optional[int]:
        """ Get the opacity that the glyph should be drawn at. """
        if glyph.tag:
            if text_effect := TextEffect.get(glyph.tag):
                return text_effect.glyph_opacity(glyph)

        return None

    def _update_characters(self) -> None:
        """ Update the character source positions and destination offsets when the text changes """
        # Reset text data
        self._width = 0
        self._height = 0
        self._glyphs.clear()

        # The current index of the source text that the cursor is at
        cursor = 0

        # The line that the current glyph will be drawn on
        line = 0

        # The X and Y position that the current glyph will be drawn at
        x = 0
        y = 0

        # The current tag that we're in
        tag = None

        # Newline height.
        # For now, just borrow the space height, since all characters *should* have the same height.
        newline_height = self._font.get_source_rect(' ').height

        while cursor < len(self.text):
            # Get the current character
            char = self.text[cursor]

            # Handle newline characters
            if char == '\n':
                x = 0
                y += newline_height
                line += 1
                cursor += 1
                continue

            # Handle tags
            if self._is_cursor_at_start_of_tag(cursor):
                # Read current tag
                tag_str = self._read_tag(cursor)

                # Set (or clear) the current tag
                if len(tag_str) and tag_str[0] == '/':
                    tag = None
                else:
                    tag = tag_str

                # Advance cursor to end of tag
                cursor_advance = len(tag_str) + 2
                cursor += cursor_advance
                continue

            # Handle word wrap
            # If we're at the start of a new word, and the next word would exceed the max line width, do carriage return
            if self.word_wrap and self._is_cursor_at_start_of_new_word(cursor):
                next_word = self._get_next_word(cursor)
                next_word_width = self._get_word_width(next_word)
                if x + next_word_width > self.max_line_width:
                    x = 0
                    y += newline_height
                    line += 1

            # Get source rect for character
            source_rect = self._font.get_source_rect(char)
            glyph = Glyph(
                character=char,
                source_rect=source_rect,
                destination_offset_x=x,
                destination_offset_y=y,
                source_index=cursor,
                index=len(self._glyphs),
                line=line,
                tag=tag,
            )
            self._glyphs.append(glyph)

            # Advance the cursor
            x += source_rect.width
            cursor += 1

        # Now that all glyphs have been generated, alignment and text size can be calculated
        if len(self._glyphs):
            self._apply_horizontal_alignment()
            self._update_text_size()
            self._apply_vertical_alignment()

    def _is_cursor_at_start_of_new_word(self, cursor: int) -> bool:
        """ Check if the cursor is at the start of a new word. """
        # If this is the very first character, we never want this to be true, otherwise it would always start by
        #   inserting a newline.
        if cursor == 0:
            return False

        current_char = self.text[cursor]
        previous_char = self.text[cursor-1]

        if previous_char.isspace() and not current_char.isspace():
            return True
        else:
            return False

    def _get_next_word(self, cursor: int) -> str:
        """ Find the next word in the text.
        This assumes the cursor position is on the first character of the next word.
        """
        text_remainder = self.text[cursor:]
        next_word = text_remainder.split(maxsplit=1)[0]
        return next_word

    def _get_word_width(self, word: str) -> int:
        """ Calculate the width in pixels of a word. """
        word_width = 0
        for char in word:
            word_width += self._font.get_source_rect(char).width

        return word_width

    def _is_cursor_at_start_of_tag(self, cursor: int) -> bool:
        """ Check if the cursor is at the start of a tag. """
        current_char = self.text[cursor]
        if cursor > 0:
            previous_char = self.text[cursor - 1]
        else:
            previous_char = ''

        if current_char == '<' and previous_char != '\\':
            return True
        else:
            return False

    def _read_tag(self, cursor: int) -> str:
        """ Read a tag and return its value.
        This assumes the cursor position is on the left angle bracket of the tag.
        """
        i = cursor + 1
        tag = ""
        while (char := self.text[i]) != '>':
            tag += char
            i += 1
        return tag

    def _apply_horizontal_alignment(self) -> None:
        """ Adjust the horizontal position of each character to align each line. """
        # Get the number of lines
        num_lines = self._glyphs[-1].line + 1

        # Initialize line widths
        line_widths = []
        for _ in range(num_lines):
            line_widths.append(0)

        # Find the width of each line
        for char in self._glyphs:
            x = char.destination_offset_x + char.source_rect.width
            if x > line_widths[char.line]:
                line_widths[char.line] = x

        # Calculate each line offset based on alignment
        line_offsets = []
        for line_width in line_widths:
            if self._horizontal_alignment == ALIGN_LEFT:
                offset_x = 0
            elif self._horizontal_alignment == ALIGN_CENTER:
                offset_x = int(line_width / 2)
            elif self._horizontal_alignment == ALIGN_RIGHT:
                offset_x = line_width
            else:
                raise NotImplementedError(self._horizontal_alignment)

            line_offsets.append(offset_x)

        # Apply alignment offset to characters
        for char in self._glyphs:
            line_offset = line_offsets[char.line]
            char.destination_offset_x -= line_offset

    def _update_text_size(self) -> None:
        """ Update the size of the text by finding the min and max X and Y positions of all characters. """
        x_min = None
        x_max = None
        y_min = None
        y_max = None

        for char in self._glyphs:
            left = char.destination_offset_x
            top = char.destination_offset_y
            right = char.destination_offset_x + char.source_rect.width
            bottom = char.destination_offset_y + char.source_rect.height
            if x_min is None or left < x_min:
                x_min = left
            if x_max is None or right > x_max:
                x_max = right
            if y_min is None or top < y_min:
                y_min = top
            if y_max is None or bottom > y_max:
                y_max = bottom

        self._width = x_max - x_min
        self._height = y_max - y_min

    def _apply_vertical_alignment(self) -> None:
        """ Adjust the vertical position of each character.
        This is done after the characters are updated.
        """
        # Calculate Y offset
        if self._vertical_alignment == ALIGN_TOP:
            offset_y = 0
        elif self._vertical_alignment == ALIGN_CENTER:
            offset_y = int(self._height / 2)
        elif self._vertical_alignment == ALIGN_BOTTOM:
            offset_y = self._height
        else:
            raise NotImplementedError(self._vertical_alignment)

        # Apply alignment offset to characters
        for char in self._glyphs:
            char.destination_offset_y -= offset_y
