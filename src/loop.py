from typing import Iterable


def _normalize_path(paths: Iterable[tuple[int, int]]) -> frozenset[tuple[int, int]]:
    """
    Normalizes paths into a frozenset of tuples (i, j) where i < j.
    """
    normalized_path = [(min(*path), max(*path)) for path in paths]
    # print(f"normalized_path = {normalized_path}")
    normalized_set = frozenset(normalized_path)
    # print(f"_normalize_loop({paths}) = {normalized_set}")
    return normalized_set


def _find_all_loops_dfs(node_count: int,
                        neighbours: list[set[int]],
                        found_loops: set[frozenset[tuple[int, int]]],
                        current_node: int,
                        current_path: list[int],
                        depth: int = 0) -> None:
    # print(f"{'\t'*depth}exploring node {current_node}")
    # print(f"{'\t'*depth}current_path = {current_path}")
    if current_node in current_path:
        # print(f"{'\t'*depth}current_node in current_path")
        # find the loop by going back from the current node
        # to its previous appearance in current_path
        loop = []
        end_node = current_node
        for node in reversed(current_path):
            loop.append((node, end_node))
            if node == current_node:
                break
            end_node = node

        if len(loop) <= 2:
            # print(f"{'\t'*depth}skipping trivial loop: {loop}")
            pass
        else:
            # print(f"{'\t'*depth}found loop: {loop}")
            found_loops.add(_normalize_path(loop))

        # print(f"{'\t' * depth}current_node on current_path, returning")
        return

    # recurse
    for neighbour in neighbours[current_node]:
        # print(f"{'\t'*depth}recursing {current_node} --> {neighbour}")
        _find_all_loops_dfs(node_count, neighbours,
                            found_loops, neighbour,
                            current_path + [current_node],
                            depth+1)


def find_all_loops(node_count: int, neighbours: list[set[int]]) -> set[frozenset[tuple[int, int]]]:
    """
    Returns the set of all simple loops.
    Each loop is represented as a frozenset of normalized edges (a tuple (i, j) where i < j).
    """
    found_loops = set()
    _find_all_loops_dfs(node_count, neighbours, found_loops, 0, [])
    return found_loops


class LoopDetector(object):
    """
    Detects loops given paths.
    Reports each loop exactly once.
    """
    def __init__(self, node_count: int, neighbours: list[set[int]]) -> None:
        self.unreported_loops = find_all_loops(node_count, neighbours)
        # print(f"all loops: {self.unreported_loops}")
        self.visited_paths = set()

    def step(self, front: set[tuple[int, int]]) -> list[frozenset[tuple[int, int]]]:
        self.visited_paths.update(_normalize_path(front))

        detected_loops = []
        for loop in self.unreported_loops:
            if loop.issubset(self.visited_paths):
                detected_loops.append(loop)

        for loop in detected_loops:
            self.unreported_loops.remove(loop)

        if len(detected_loops) > 0:
           print(f"detected_loops = {detected_loops}")
        return detected_loops
