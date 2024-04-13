from engine import *

from entities.skull import Skull


class RedSkull(Skull):
    def __init__(self) -> None:
        super().__init__()
        self.sprite = AnimatedSprite.from_atlas("atlas.png", "red_skull")
        self.team = "red"
