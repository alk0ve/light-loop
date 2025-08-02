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
                 starting_mana: int,
                 turn_limit: int) -> None:
        self.board = initial_board
        self.available_nodes = available_nodes
        self.starting_mana = starting_mana
        self.turn_limit = turn_limit
        self.current_turn = 1

    def draw(self):
        self.board.draw()

        # TODO draw UI elements


SECOND_LEVEL = Level(Board(create_nodes([(NodeType.BROADCAST_ONCE, 200, 400),
                                         (NodeType.BROADCAST_ONCE, 400, 400),
                                         (NodeType.BROADCAST_ONCE, 500, 600),
                                         (NodeType.BROADCAST, 600, 400),
                                         (NodeType.BROADCAST_ONCE, 600, 200),
                                         (NodeType.BLOCK, 400, 200)]),
                           {(0, 1), (1, 2), (1, 3), (1, 5), (2, 3), (3, 4), (4, 5), (5, 1)}),
                     [],
                     10,
                     6)
