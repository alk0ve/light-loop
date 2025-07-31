from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..board import Board
    from ..nodes.node import Node


class Level(object):
    """
    A level consists of:
     - the initial board
     - available nodes
     - starting mana
     - turn limit
    """
    def __init__(self,
                 board: Board,
                 available_nodes: list[Node],
                 mana: int,
                 turn_limit: int) -> None:
        self.board = board
        self.available_nodes = available_nodes
        self.mana = mana
        self.turn_limit = turn_limit
        self.current_turn = 1

    def draw(self):
        # TODO
        pass