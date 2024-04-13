from engine import *

STATE_BLUE_TURN = 0  # noqa
STATE_RED_TURN =  1  # noqa


class GameManager(Entity):
    def __init__(self) -> None:
        super().__init__()
        self.name = "GameManager"
        self.state = 0

    def is_blue_turn(self) -> bool:
        return self.state == STATE_BLUE_TURN

    def is_red_turn(self) -> bool:
        return self.state == STATE_RED_TURN
