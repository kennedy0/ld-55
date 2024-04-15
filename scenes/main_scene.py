from engine import *

from entities.bg import Bg
from entities.blue_player import BluePlayer
from entities.board import Board
from entities.game_manager import GameManager
from entities.red_player import RedPlayer
from entities.summon_circle import SummonCircle
from entities.tile import Tile

from entities.ui_score import UiScore
from entities.ui_game_ended import UiGameEnded
from entities.ui_tutorial_text import UiTutorialText

from entities.title import Title
from entities.ui_tutorial import UiTutorial
from entities.ui_1p import Ui1p
from entities.ui_2p import Ui2p
from entities.ui_quit_game import UiQuitGame
from entities.ui_sound import UiSound


class MainScene(Scene):
    def setup_cameras(self) -> None:
        # Center camera
        self.main_camera.x = -160
        self.main_camera.y = -90

    def load_entities(self) -> None:
        if __debug__:
            from entities.debugger import Debugger
            self.entities.add(Debugger())

        # Managers
        game_manager = GameManager()
        self.entities.add(game_manager)

        # Background
        self.entities.add(Bg())

        # Board
        self.generate_board(3)

        # Summon Circle
        self.entities.add(SummonCircle())

        # Players
        blue_player = BluePlayer()
        self.entities.add(blue_player)

        red_player = RedPlayer()
        self.entities.add(red_player)

        # UI
        self.entities.add(UiScore())
        self.entities.add(UiTutorialText())

        # Main Menu
        self.entities.add(Title())
        self.entities.add(UiTutorial())
        self.entities.add(Ui1p())
        self.entities.add(Ui2p())
        self.entities.add(UiSound())
        self.entities.add(UiQuitGame())

        # End Game
        self.entities.add(UiGameEnded())

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
        board.set_neighbors()

    def start(self) -> None:
        super().start()
        self.entities.get("GameManager").show_main_menu()
