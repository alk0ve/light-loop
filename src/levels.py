from board import Board
from nodes import Node, create_nodes, NodeType


class Level(object):
    """
    A level consists of:
     - the initial board
     - available nodes
     - starting mana
     - turn limit
    """

    def __init__(self,
                 initial_board: Board,
                 available_nodes: list[Node],
                 mana: int,
                 turn_limit: int) -> None:
        self.board = initial_board
        self.available_nodes = available_nodes
        self.mana = mana
        self.turn_limit = turn_limit
        self.current_turn = 1

    def draw(self):
        self.board.draw()

        # TODO draw UI elements


FIRST_LEVEL = Level(Board(create_nodes([NodeType.BROADCAST_ONCE, NodeType.BROADCAST_ONCE, NodeType.BROADCAST_ONCE],
                                       [(200, 200), (500, 200), (300, 500)]),
                          {(0, 1), (1, 2), (2, 0)}),
                    [],
                    0,
                    99)

SECOND_LEVEL = Level(Board(create_nodes([NodeType.BROADCAST_ONCE] * 5,
                                        [(100, 400), (300, 400), (500, 200), (500, 600), (700, 400)]),
                           {(0, 1), (1, 2), (1, 3), (2, 4), (3, 4), (4, 1)}),
                     [],
                     0,
                     99)
