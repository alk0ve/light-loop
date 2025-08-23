from nodes import NodeType


class Level(object):
    """
    A level is the saved, readonly state of a game before the player acts.
    It consists of:
     - the initial board
     - starting mana
     - turn limit
     - initial fog-of-war (TBD)
     - available nodes (TBD)
    """

    def __init__(self,
                 nodes: list[tuple[NodeType, int, int]],
                 paths: set[tuple[int, int]],
                 starting_mana: int,
                 turn_limit: int) -> None:
        self.nodes = nodes
        self.paths = paths
        self.starting_mana = starting_mana
        self.turn_limit = turn_limit


#  wrap levels in functions to avoid creating sprites before a pyglet window exists

def test_level() -> Level:
    return Level([(NodeType.BROADCAST_ONCE, 200, 400),
                  (NodeType.BROADCAST_ONCE, 400, 400),
                  (NodeType.BROADCAST_ONCE, 500, 600),
                  (NodeType.BROADCAST, 600, 400),
                  (NodeType.BROADCAST_ONCE, 600, 200),
                  (NodeType.BLOCK, 400, 200)],
                 {(0, 1), (1, 2), (1, 3), (1, 5), (2, 3), (3, 4), (4, 5), (5, 1)},
                 10,
                 6)
