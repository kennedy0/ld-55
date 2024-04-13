from engine import *

from entities.bg import Bg
from entities.board import Board
from entities.game_manager import GameManager
from entities.skull_spawner import SkullSpawner
from entities.summon_circle import SummonCircle
from entities.tile import Tile


class TestScene(Scene):
    def setup_cameras(self) -> None:
        # Center camera
        self.main_camera.x = -160
        self.main_camera.y = -90

    def load_entities(self) -> None:
        # Managers
        self.entities.add(GameManager())
        self.entities.add(SkullSpawner())

        # Background
        self.entities.add(Bg())

        # Board
        self.generate_board(3)

        # FX
        self.entities.add(SummonCircle())

    def generate_board(self, radius: int) -> None:
        # Create board
        board = Board()
        board.radius = radius
        self.entities.add(board)

        # Create tiles

        q = 0
        r = 0
        s = 0

        for i in range(q-radius, q+radius+1):
            for j in range(r-radius, r+radius+1):
                for k in range(s-radius, s+radius+1):
                    if i + j + k == 0:
                        tile = Tile()
                        tile.q = i
                        tile.r = j
                        tile.s = k
                        tile.coordinates = (i, j, k)
                        board.add_tile(tile)
                        self.entities.add(tile)

        # Setup board
        board.move_tiles()
