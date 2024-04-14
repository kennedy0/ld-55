from engine import *

from entities.board import Board
from entities.game_manager import GameManager


class UiScore(Entity):
    def __init__(self) -> None:
        super().__init__()
        self.tags.add("UI")
        self.game_manager: GameManager | None = None
        self.board: Board | None = None

        self.front = Sprite.from_atlas("atlas.png", "score_bar_front")
        self.back = Sprite.from_atlas("atlas.png", "score_bar_back")

        self.x = 80
        self.y = 170

        self.top = 2 + self.y
        self.bottom = 7 + self.y
        self.left = 2 + self.x
        self.right = 160 + self.x
        self.width = 164
        self.height = 6

        self.blue_rect = Rect.empty()
        self.red_rect = Rect.empty()

        self.blue = Color.blue()
        self.red = Color.red()

        self.blue_score = 0
        self.red_score = 0

    def start(self) -> None:
        self.game_manager = self.find("GameManager")
        self.board = self.find("Board")
        self.update_blue()
        self.update_red()

    def update_blue(self) -> None:
        self.blue_rect = Rect(self.left, self.top, 1, self.height)

    def update_red(self) -> None:
        self.red_rect = Rect(self.right - 1, self.top, 1, self.height)

    def draw(self, camera: Camera) -> None:
        self.back.draw(camera, self.position())
        self.blue_rect.draw(camera, self.blue, solid=True)
        self.red_rect.draw(camera, self.red, solid=True)
        self.front.draw(camera, self.position())
