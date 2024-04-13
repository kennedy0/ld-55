from engine import *

from entities.bg import Bg
from entities.hex import Hex


class TestScene(Scene):
    def load_entities(self) -> None:
        self.entities.add(Bg())
        self.generate_board(2)

    def generate_board(self, radius: int) -> None:
        q = 0
        r = 0
        s = 0

        for i in range(q-radius, q+radius+1):
            for j in range(r-radius, r+radius+1):
                for k in range(s-radius, s+radius+1):
                    if i + j + k == 0:
                        self.entities.add(Hex(q, r, s))
