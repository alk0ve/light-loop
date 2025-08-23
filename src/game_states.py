from debug_print import DebugCategory, DebugPrintMixin
from levels import Level
from boards import Board
from nodes import create_nodes
from loop_detector import LoopDetector
from loops import Loop
from delayed_action import DelayedAction


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

    class ManaGainAction(DelayedAction):
        def __init__(self, game_state: "GameState", mana_gain: int):
            super().__init__()
            self.game_state = game_state
            self.mana_gain = mana_gain

        def act(self) -> None:
            self.game_state.mana += self.mana_gain

    def create_loop(self, loop_edges: frozenset[tuple[int, int]]) -> Loop:
        mana_gain = len(loop_edges)  # TODO formula

        return self.board.create_loop(loop_edges, GameState.ManaGainAction(self, mana_gain))
