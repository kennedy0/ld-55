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
        self.width = 158
        self.height = 6

        self.blue_rect = Rect.empty()
        self.red_rect = Rect.empty()

        self.blue = Color(115, 150, 213)
        self.red = Color(192, 104, 82)

        self.blue_score = 0
        self.red_score = 0

    def start(self) -> None:
        self.game_manager = self.find("GameManager")
        self.board = self.find("Board")
        self.update_blue()
        self.update_red()

    def update(self) -> None:
        if self.board.blue_tiles != self.blue_score:
            self.blue_score = self.board.blue_tiles
            self.update_blue()

        if self.board.red_tiles != self.red_score:
            self.red_score = self.board.red_tiles
            self.update_red()

    def update_blue(self) -> None:
        if not self.board.total_tiles:
            self.blue_rect = Rect.empty()
        else:
            p = self.board.blue_tiles / self.board.total_tiles
            w = int(pmath.lerp(0, self.width, p))
            self.blue_rect = Rect(self.left, self.top, w, self.height)

    def update_red(self) -> None:
        if not self.board.total_tiles:
            self.red_rect = Rect.empty()
        else:
            p = self.board.red_tiles / self.board.total_tiles
            w = int(pmath.lerp(0, self.width, p))
            self.red_rect = Rect(self.right - w, self.top, w, self.height)

    def draw(self, camera: Camera) -> None:
        self.back.draw(camera, self.position())
        self.blue_rect.draw(camera, self.blue, solid=True)
        self.red_rect.draw(camera, self.red, solid=True)
        self.front.draw(camera, self.position())
