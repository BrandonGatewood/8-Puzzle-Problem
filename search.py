from queue import PriorityQueue
import node


# Implements the informed search algorithms, A* search and best-first search. If a search limit is reached, the
# algorithms will return None, resulting in a failed search. Both search algorithms are implemented with a heuristic to
# determine which path to take next.

class SearchAlgorithm:
    def __init__(self, puzzle_object):
        self.start_node = node.Node(puzzle_object)

    # Best-first search algorithm
    def bfs(self, heuristic, limit):
        count = 0
        actual = self.start_node
        leaves = PriorityQueue()
        leaves.put((actual.call_heuristic(heuristic), count, actual))
        closed = list()
        search_limit = 0

        while search_limit < limit:
            if leaves.empty():
                return None

            actual = leaves.get()[2]
            if actual.check_goal_state():
                return actual
            elif actual.puzzle_obj.puzzle_state.tolist() not in closed:
                closed.append(actual.puzzle_obj.puzzle_state.tolist())
                succ = actual.successor()
                while not succ.empty():
                    child = succ.get()
                    count += 1
                    leaves.put((child.call_heuristic(heuristic), count, child))
            search_limit += 1
        return None

    # A* search algorithm
    def a_star(self, heuristic, limit):
        count = 0
        actual = self.start_node
        leaves = PriorityQueue()
        leaves.put((actual.call_heuristic(heuristic), count, actual))
        # Track previous seen puzzle states.
        closed = list()
        search_limit = 0
        while search_limit < limit:
            if leaves.empty():
                return None
            actual = leaves.get()[2]
            if actual.check_goal_state():
                return actual
            elif actual.puzzle_obj.puzzle_state.tolist() not in closed:
                closed.append(actual.puzzle_obj.puzzle_state.tolist())
                succ = actual.successor()
                while not succ.empty():
                    child = succ.get()
                    count += 1
                    leaves.put((child.call_heuristic(heuristic) + child.depth, count, child))
            search_limit += 1
        return None
