from level import Level, Board
from ..nodes.node_factory import create_nodes, NodeType

FIRST_LEVEL = Level(Board(create_nodes([NodeType.NO_NODE, NodeType.NO_NODE, NodeType.NO_NODE],
                                       [(200, 200), (400, 200), (300, 500)]),
                          [(0, 1), (1, 2), (2, 0)]),
                    [],
                    0,
                    99)
