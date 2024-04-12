from __future__ import annotations

from typing import Optional, Self, TYPE_CHECKING

from engine.data_types.color import Color
from engine.entity import Entity
from engine.log import Log

if TYPE_CHECKING:
    from engine.camera import Camera


class GuiWidgetEntity(Entity):
    """ Base class for a GUI widget entity. """
    def __init__(self) -> None:
        super().__init__()

        # Pause
        self.pausable = False

        # Tags
        self.tags.add("UI")

        # Size
        self._width = 0
        self._height = 0

        # Navigation links
        self._up = None
        self._down = None
        self._left = None
        self._right = None

        # Behavior flags
        self._enabled = True
        self._selectable = False

        # State
        self._selected = False

        # Collision
        self.mouse_collisions_enabled = True

    @property
    def up(self) -> Optional[Self]:
        """ The selectable widget above this widget, for keyboard/gamepad navigation. """
        return self._up

    @up.setter
    def up(self, value: Optional[Self]) -> None:
        self._up = value

    @property
    def down(self) -> Optional[Self]:
        """ The selectable widget below this widget, for keyboard/gamepad navigation. """
        return self._down

    @down.setter
    def down(self, value: Optional[Self]) -> None:
        self._down = value

    @property
    def left(self) -> Optional[Self]:
        """ The selectable widget to the left of this widget, for keyboard/gamepad navigation. """
        return self._left

    @left.setter
    def left(self, value: Optional[Self]) -> None:
        self._left = value

    @property
    def right(self) -> Optional[Self]:
        """ The selectable widget to the right of this widget, for keyboard/gamepad navigation. """
        return self._right

    @right.setter
    def right(self, value: Optional[Self]) -> None:
        self._right = value

    @property
    def selectable(self) -> bool:
        """ If True, the widget can be selected. """
        return self._selectable

    @selectable.setter
    def selectable(self, value: bool) -> None:
        self._selectable = value

    @property
    def enabled(self) -> bool:
        """ An enabled widget is in its 'normal' state, and may be interacted with.
        A disabled widget is still visible, but cannot be interacted with.
        """
        return self._enabled

    @enabled.setter
    def enabled(self, value: bool) -> None:
        # Exit if no value changed
        if value == self._enabled:
            return

        # Set the new value
        self._enabled = value

        # Trigger callbacks
        if value:
            self.on_enabled()
        else:
            self.on_disabled()

    @property
    def selected(self) -> bool:
        """ The selection state of the widget. """
        return self._selected

    @selected.setter
    def selected(self, value: bool) -> None:
        # Error if we try to select an unselectable widget
        if value and not self.selectable:
            Log.error(f"{self} is not selectable")
            return

        # Exit if no value change
        if value == self._selected:
            return

        # Set the new value
        self._selected = value

        # Trigger callbacks
        if value:
            self.on_selected()
        else:
            self.on_deselected()

    def on_enabled(self) -> None:
        """ Called when the widget is enabled. """
        pass

    def on_disabled(self) -> None:
        """ Called when the widget is disabled. """
        pass

    def on_selected(self) -> None:
        """ Called when the widget is selected. """
        pass

    def on_deselected(self) -> None:
        """ Called when the widget is deselected. """
        pass

    def select_up(self) -> None:
        """ Select the widget above this one. """
        if self.up:
            self.selected = False
            self.up.selected = True

    def select_down(self) -> None:
        """ Select the widget below this one. """
        if self.down:
            self.selected = False
            self.down.selected = True

    def select_left(self) -> None:
        """ Select the widget to the left of this one. """
        if self.left:
            self.selected = False
            self.left.selected = True

    def select_right(self) -> None:
        """ Select the widget to the right of this one. """
        if self.right:
            self.selected = False
            self.right.selected = True

    def debug_draw(self, camera: Camera) -> None:
        """ Draw debug info for the widget. """
        # Selection
        if self.selected:
            self.bbox().draw(camera, Color(255, 255, 0, 128), solid=True)

        # Widget rect
        self.bbox().draw(camera, Color.white())
