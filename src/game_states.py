from debug_print import DebugCategory, DebugPrintMixin
from levels import Level
from boards import Board
from nodes import create_nodes
from loop_detector import LoopDetector


class GameState(DebugPrintMixin):
    board: Board
    turns_left: int
    mana = int
    loop_detector: LoopDetector

    def __init__(self, level: Level) -> None:
        DebugPrintMixin.__init__(self, DebugCategory.GAME)
        self.level = level
        self.reset()

    def reset(self) -> None:
        self.board = Board(create_nodes(self.level.nodes), self.level.paths)
        self.turns_left = self.level.turn_limit
        self.mana = self.level.starting_mana
        self.loop_detector = LoopDetector(len(self.board.nodes), self.board.neighbours)

    def draw(self) -> None:
        self.board.draw()

    def reset_animation(self) -> None:
        self.board.reset_animation()
        self.loop_detector.reset()
