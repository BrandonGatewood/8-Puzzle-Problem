from copy import deepcopy
from queue import Queue
import numpy as np


# Node class will generate all successors, contains information about the heuristics
# The third heuristic I chose was Euclidean distance.
class Node:
    def __init__(self, puzzle_object, parent=None, move="", counter=0):
        self.puzzle_obj = puzzle_object
        self.parent = parent
        if parent is None:
            # Root
            self.depth = 0
            self.moves = move
            self.counter = counter
        else:
            # Expand
            self.depth = parent.depth + 1
            self.moves = parent.moves + " " + move
            self.counter = parent.counter + counter

    # Check if node reached goal state
    def check_goal_state(self):
        return self.puzzle_obj.check_puzzle()

    # Generate nodes successors
    def successor(self):
        successors = Queue()
        # track all future moves
        for m in self.puzzle_obj.moves:
            future_obj = deepcopy(self.puzzle_obj)
            future_obj.move(m)
            # Check if the move is valid
            if future_obj.zero_tile is not self.puzzle_obj.zero_tile:
                successors.put(Node(future_obj, self, m, 1))
        return successors

    # Call 1 of three different heuristics
    def call_heuristic(self, i):
        if i == 1:
            return self.num_of_misplaced_tiles()
        elif i == 2:
            return self.manhattan_distance()
        elif i == 3:
            return self.euclidean_distance()

    # heuristic 1: number of misplaced tiles
    def num_of_misplaced_tiles(self):
        # Return the total number of misplaced tiles.
        puzzle_state = self.puzzle_obj.puzzle_state
        goal_state = self.puzzle_obj.goal_state
        result = 0
        for i in range(2):
            for j in range(2):
                if puzzle_state[i][j] != goal_state[i][j]:
                    result += 1
        return result

    # heuristic 2: Manhattan distance
    def manhattan_distance(self):
        # Return sum of all possible distances from a current state tile to goal state tile.
        puzzle_state = self.puzzle_obj.puzzle_state
        result = 0
        for i in range(2):
            for j in range(2):
                index = puzzle_state[i][j] - 1
                distance = (2 - i) + (2 - j) if index == -1 else abs(i - (index / 3)) + abs(
                    j - (index % 3))
                result += distance
        return result

    # heuristic 3: Euclidean distance
    def euclidean_distance(self):
        # Return the shortest possible distance from a current state tile to goal state tile.
        puzzle_state = self.puzzle_obj.puzzle_state
        goal_state = self.puzzle_obj.goal_state
        result = 0

        for i in range(2):
            for j in range(2):
                dist = np.linalg.norm(puzzle_state[i][j] - goal_state[gi][gj])
                result += dist

        return result

    # used when printing a node object
    def __str__(self):
        return str(self.moves)
