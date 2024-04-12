from __future__ import annotations

from typing import Optional, TYPE_CHECKING

from engine.data_types.point import Point
from engine.engine import Engine
from engine.input_manager import InputManager
from engine.window import Window


if TYPE_CHECKING:
    from engine.camera import Camera


class Mouse:
    """ Get information about the mouse state. """
    @classmethod
    def in_bounds(cls) -> bool:
        """ Check if the mouse is in bounds. """
        if InputManager.is_mouse_in_window():
            if Window.viewport().contains_point(cls.screen_position()):
                return True

        return False

    @classmethod
    def screen_position(cls) -> Point:
        """ Get the screen position of the mouse cursor. """
        return Point(InputManager.get_mouse_x(), InputManager.get_mouse_y())

    @classmethod
    def world_position(cls, camera: Optional[Camera] = None) -> Point:
        """ Get the world position of the mouse cursor.
        This has to be relative to a camera. If no camera is provided, the current scene's main camera will be implied.
        """
        if not camera:
            camera = Engine.scene().main_camera
        return camera.screen_to_world_position(cls.screen_position())

    @classmethod
    def get_left_mouse(cls) -> bool:
        """ Check if the left mouse button is pressed. """
        return InputManager.get_left_mouse()

    @classmethod
    def get_right_mouse(cls) -> bool:
        """ Check if the right mouse button is pressed. """
        return InputManager.get_right_mouse()

    @classmethod
    def get_middle_mouse(cls) -> bool:
        """ Check if the middle mouse button is pressed. """
        return InputManager.get_middle_mouse()

    @classmethod
    def get_left_mouse_down(cls) -> bool:
        """ Check if the left mouse button was pressed this frame. """
        return InputManager.get_left_mouse_down()

    @classmethod
    def get_left_mouse_up(cls) -> bool:
        """ Check if the left mouse button was released this frame. """
        return InputManager.get_left_mouse_up()

    @classmethod
    def get_right_mouse_down(cls) -> bool:
        """ Check if the right mouse button was pressed this frame. """
        return InputManager.get_right_mouse_down()

    @classmethod
    def get_right_mouse_up(cls) -> bool:
        """ Check if the right mouse button was released this frame. """
        return InputManager.get_right_mouse_up()

    @classmethod
    def get_middle_mouse_down(cls) -> bool:
        """ Check if the middle mouse button was pressed this frame. """
        return InputManager.get_middle_mouse_down()

    @classmethod
    def get_middle_mouse_up(cls) -> bool:
        """ Check if the middle mouse button was released this frame. """
        return InputManager.get_middle_mouse_up()

    @classmethod
    def get_mouse_scroll_wheel(cls) -> int:
        """ Get the mouse scroll wheel value this frame. """
        return InputManager.get_mouse_scroll_wheel()
