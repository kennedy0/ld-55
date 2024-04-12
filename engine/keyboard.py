from engine.input_manager import InputManager
from engine.internal_utilities import keyboard_utils


class Keyboard:
    """ Get information about the keyboard state. """
    @classmethod
    def get_key(cls, key: int) -> bool:
        """ Check if a key is pressed. """
        return InputManager.get_key(key)

    @classmethod
    def get_key_down(cls, key: int) -> bool:
        """ Check if a key was pressed this frame. """
        return InputManager.get_key_down(key)

    @classmethod
    def get_key_up(cls, key: int) -> bool:
        """ Check if a key was released this frame. """
        return InputManager.get_key_up(key)

    @classmethod
    def get_keys_pressed(cls) -> tuple[int]:
        """ Get a list of all keys that are currently pressed. """
        return InputManager.get_keys_pressed()

    @classmethod
    def get_key_names_pressed(cls) -> tuple[str]:
        """ Get a list of all key names that are currently pressed. """
        key_names = []

        for key in cls.get_keys_pressed():
            key_name = keyboard_utils.key_to_name(key)
            if key_name:
                key_names.append(key_name)

        return tuple(key_names)

    @classmethod
    def key_code(cls, key_name: str) -> int:
        """ Get the key code from the name of a key. """
        return keyboard_utils.name_to_key(key_name)
