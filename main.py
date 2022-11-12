# Brandon Gatewood
# CS 441 AI
# Program 1: 8 Puzzle Problem

import numpy as np
from tqdm import tqdm
import search


# Puzzle class acts as a 3x3 board and moves the 'blank' tile up, down, left, and right until it reaches the goal state.
# The initial state is randomly permuted, so it may not always be solvable. A solvable method has been implemented to
# avoid searching a path for an unsolvable matrix. This function will continue permuting a new initial state until is it
# solvable and then run the search algorithms. However, a failed search may still happen when a search limit has been
# reached.
class Puzzle:
    generic_state = np.array([1, 2, 3, 4, 5, 6, 7, 8, 0])

    def __init__(self):
        # Generate random initial unitl it is solvable.
        self.puzzle_state = self.permute()

        while not self.is_solvable():
            self.puzzle_state = self.permute()

        # self.puzzle_state = np.array([[1, 2, 3], [4, 5, 6], [0, 8, 7]])
        self.goal_state = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 0]])

        # 4 allowed moves in puzzle problem
        self.moves = ["u", "d", "l", "r"]

        # Track 'blank' tile coordinates.
        self.zero_tile = np.where(self.puzzle_state == 0)

    # Permute generic state to get a random initial and goal state
    def permute(self):
        perm = np.random.permutation(self.generic_state)
        perm = np.reshape(perm, (-1, 3))
        return perm

    # Returns true if inversion count is even
    def is_solvable(self):
        inv_count = self.get_inv_count([j for sub in self.puzzle_state for j in sub])

        # return True if inversion count is even
        return inv_count % 2 == 0

    # Count the number of inversions
    @staticmethod
    def get_inv_count(arr):
        inv_count = 0
        empty_value = -1
        for i in range(0, 9):
            for j in range(i + 1, 9):
                check1 = arr[j] != empty_value
                check2 = arr[i] != empty_value
                check3 = arr[i] > arr[j]
                check = check1 + check2 + check3
                if check.all():
                    inv_count += 1
        return inv_count

    # Check if puzzle reached the goal state
    def check_puzzle(self):
        check = self.puzzle_state == self.goal_state
        return check.all()

    # Calls the appropriate move function for a given move
    def move(self, a_move):
        if a_move == "u":
            self.up()
        if a_move == "d":
            self.down()
        if a_move == "l":
            self.left()
        if a_move == "r":
            self.right()

    # Swap function that swaps the zero tile with another tile
    def swap(self, i1, j1, i2, j2):
        i1 = i1[0]
        j1 = j1[0]
        i2 = i2[0]
        j2 = j2[0]
        # Save value at zero_tiles new location
        temp = self.puzzle_state[i1][j1]
        # Update zero_tile's to new location within the puzzle state
        self.puzzle_state[i1][j1] = self.puzzle_state[i2][j2]
        # Update new location for temp
        self.puzzle_state[i2][j2] = temp

    # Move zero tile up 1 row and call swap function
    def up(self):
        if self.zero_tile[0] != 0:
            # Move up 1 row
            self.swap(self.zero_tile[0] - 1, self.zero_tile[1], self.zero_tile[0], self.zero_tile[1])
            # Update zero_tile coordinates
            self.zero_tile = (self.zero_tile[0] - 1, self.zero_tile[1])

    # Move zero tile down 1 row and call swap function
    def down(self):
        if self.zero_tile[0] != 2:
            # Move down 1 row
            self.swap(self.zero_tile[0] + 1, self.zero_tile[1], self.zero_tile[0], self.zero_tile[1])
            # Update zero_tile coordinates
            self.zero_tile = (self.zero_tile[0] + 1, self.zero_tile[1])

    # Move zero tile left 1 column
    def left(self):
        if self.zero_tile[1] != 0:
            # Move left 1 column
            self.swap(self.zero_tile[0], self.zero_tile[1] - 1, self.zero_tile[0], self.zero_tile[1])
            # Update zero_tile coordinates
            self.zero_tile = (self.zero_tile[0], self.zero_tile[1] - 1)

    # Move zero tile right 1 column
    def right(self):
        if self.zero_tile[1] != 2:
            # Move right 1 column
            self.swap(self.zero_tile[0], self.zero_tile[1] + 1, self.zero_tile[0], self.zero_tile[1])
            # Update zero_tile coordinates
            self.zero_tile = (self.zero_tile[0], self.zero_tile[1] + 1)

    # Print the puzzle state
    def print(self):
        print(self.puzzle_state.reshape(-1))


# Interface class is used to run the entire program and print out all path solutions for 5 trials.
# Interface contains the search limit that will stop the search algorithm once it's been reached.
class Interface:
    def __init__(self):
        # Play around with limit
        self.limit = 10000000
        self.bfs_heuristic_1 = [0, 0, 0, 0, 0]
        self.bfs_heuristic_2 = [0, 0, 0, 0, 0]
        self.bfs_heuristic_3 = [0, 0, 0, 0, 0]
        self.as_heuristic_1 = [0, 0, 0, 0, 0]
        self.as_heuristic_2 = [0, 0, 0, 0, 0]
        self.as_heuristic_3 = [0, 0, 0, 0, 0]
        self.puzzle_array = []

        # Generate 5 different puzzles
        for i in range(5):
            self.puzzle_array.append(Puzzle())

    # Run entire program
    def run(self):
        for i in tqdm(range(len(self.puzzle_array))):
            s = search.SearchAlgorithm(self.puzzle_array[i])
            self.bfs_heuristic_1[i] = s.bfs(1, self.limit)
            self.bfs_heuristic_2[i] = s.bfs(2, self.limit)
            self.bfs_heuristic_3[i] = s.bfs(3, self.limit)
            self.as_heuristic_1[i] = s.a_star(1, self.limit)
            self.as_heuristic_2[i] = s.a_star(2, self.limit)
            self.as_heuristic_3[i] = s.a_star(3, self.limit)
        self.results()

    def results(self):
        bfs_count = [0, 0, 0]
        as_count = [0, 0, 0]

        print("Best-first search:")
        print("\tHeuristic 1:")
        for i in range(len(self.puzzle_array)):
            if self.bfs_heuristic_1[i] is None:
                print("\t Failed.")
            else:
                print("\t", self.bfs_heuristic_1[i])
                bfs_count[0] += self.bfs_heuristic_1[i].counter
        print('\tAverage number of steps: ', bfs_count[0] / 5)

        print("\n\tHeuristic 2:")
        for i in range(len(self.puzzle_array)):
            if self.bfs_heuristic_2[i] is None:
                print("\t Failed.")
            else:
                print("\t", self.bfs_heuristic_2[i])
                bfs_count[1] += self.bfs_heuristic_2[i].counter
        print('\tAverage number of steps: ', bfs_count[1] / 5)

        print("\n\tHeuristic 3:")
        for i in range(len(self.puzzle_array)):
            if self.bfs_heuristic_3[i] is None:
                print("\t Failed.")
            else:
                print("\t", self.bfs_heuristic_3[i])
                bfs_count[2] += self.bfs_heuristic_3[i].counter
        print('\tAverage number of steps: ', bfs_count[2] / 5)

        print("\nA* search:")
        print("\tHeuristic 1:")
        for i in range(len(self.puzzle_array)):
            if self.as_heuristic_1[i] is None:
                print("\t Failed.")
            else:
                print("\t", self.as_heuristic_1[i])
                as_count[0] += self.as_heuristic_1[i].counter
        print('\tAverage number of steps: ', as_count[0] / 5)

        print("\n\tHeuristic 2:")
        for i in range(len(self.puzzle_array)):
            if self.as_heuristic_2[i] is None:
                print("\t Failed.")
            else:
                print("\t", self.as_heuristic_2[i])
                as_count[1] += self.as_heuristic_2[i].counter
        print('\tAverage number of steps: ', as_count[1] / 5)

        print("\n\tHeuristic 3:")
        for i in range(len(self.puzzle_array)):
            if self.as_heuristic_3[i] is None:
                print("\t Failed.")
            else:
                print("\t", self.as_heuristic_3[i])
                as_count[2] += self.as_heuristic_3[i].counter
        print('\tAverage number of steps: ', as_count[2] / 5)


run = Interface()
run.run()
