from node import Node
from asset.finder import asset


class NoNode(Node):
    """
    An empty space, a placeholder for a past/future node.
    """

    def __init__(self, x: int, y: int):
        super().__init__(asset("no-node.png"), x, y)

