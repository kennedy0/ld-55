from engine import *

from entities.skull import Skull


class BlueSkull(Skull):
    def __init__(self) -> None:
        super().__init__()
        self.sprite = AnimatedSprite.from_atlas("atlas.png", "blue_skull")
        self.team = "blue"
