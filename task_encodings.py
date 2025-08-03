from pathless_tree_search import PathlessTreeSearch, encode_problem
import numpy as np
from connect4.connect_state import ConnectState


def get_tree_search_for_sudoku(sudoku):
    """
    Prepares a tree search to solve a Sudoku puzzle.

    Args:
        sudoku (np.ndarray): 9x9 numpy array representing the Sudoku board.

    Returns:
        tuple: (PathlessTreeSearch, decoder)
            - search: Search object for solving the Sudoku.
            - decoder: Function to decode final node to 9x9 board.
    """
    domains = {
        (row,col): list(range(1,10))

        for row in range(9)
        for col in range(9)

        if sudoku[row,col] == 0
    }

    def constraints(p_assignment):
        for (row, col), value in p_assignment.items():
            for c in range(9):
                if c != col and (row, c) in p_assignment and p_assignment[(row, c)] == value:
                    return False
                
            for r in range(9):
                if r != row and (r, col) in p_assignment and p_assignment[(r, col)] == value:
                    return False
                
            box_row = (row // 3) * 3
            box_col = (col // 3) * 3

            for r in range(box_row, box_row + 3):
                for c in range(box_col, box_col + 3):
                    if (r, c) != (row, col) and (r, c) in p_assignment and p_assignment[(r, c)] == value:
                        return False
                    
            if sudoku[row, col] != 0 and sudoku[row, col] != value:
                return False
            
        return True
    
    search = encode_problem(domains, constraints)

    def decoder(final):
        new_board = sudoku.copy()
        for (row, col), value in final.items():
            new_board[row, col] = value
        return new_board

    return search, decoder

def get_tree_search_for_jobshop(jobshop):
    """
    Encodes a Job Shop Scheduling problem as a tree search.

    Args:
        jobshop (tuple): A tuple (m, d) where:
            - m (int): Number of machines.
            - d (list): List of job durations.

    Returns:
        tuple: (PathlessTreeSearch, decoder)
            - search: Search object for solving the job shop.
            - decoder: Function to decode final node into job-machine assignments.
    """
    m,d = jobshop

    domains = {
        i: list(range(m)) 
        for i in range(len(d)) 
    }

    def constraints(p_assignment):
        return True
    
    def better(a,b):
        def time(p_assingment):
            total_load = [0] * m
            for job, machine in p_assingment.items():
                total_load[machine] += d[job]
            return max(total_load)
        return time(a) < time(b)
    
    search = encode_problem(domains, constraints, better, order="dfs")

    def decoder(final):
        jobs = len(d)
        result = [0] * jobs
        for job, machine in final.items():
            result[job] = machine
        return result

        
    
    return search, decoder


def get_tree_search_for_connect_4(opponent):
    """
    Creates a tree search object to find a winning strategy for Connect-4.

    Args:
        opponent (Callable): Function mapping state to opponent's move.

    Returns:
        tuple: (PathlessTreeSearch, decoder)
            - search: Search object to solve the game.
            - decoder: Function to extract yellow player’s move sequence.
    """

    n0 = ConnectState()

    def succ(state):
        succs = []

        for col in range(7):
            if state.is_applicable(col):
                next = state.play(col, opponent)
                succs.append(next)
        return succs

    def goal(state):
        return state.winner == "yellow"
    
    search = PathlessTreeSearch(n0, succ, goal, better=None, order="bfs")
    
    def decoder(state):
        return state.yellow_sequence

    return search, decoder


def get_tree_search_for_tour_planning(distances, from_index, to_index):
    """
    Encodes a tour planning problem as a tree search.

    Args:
        distances (np.ndarray): Adjacency matrix of distances between cities.
        from_index (int): Starting city index.
        to_index (int): Target city index.

    Returns:
        tuple: (PathlessTreeSearch, decoder)
            - search: Search object to solve the tour planning problem.
            - decoder: Function that returns the full path of the tour.
    """
    n = len(distances)
    cities = list(range(n))

    domains = {
        0: [from_index],
        n - 1: [to_index]
    }

    for i in range(1, n - 1):
        domains[i] = [c for c in cities if c != from_index and c != to_index]

    def constraints(p_assignment):
        values = list(p_assignment.values())
        return len(values) == len(set(values))

    def better(a, b):
        def route(path):
            length = 0
            for i in range(1, len(path)):
                city1 = path[i - 1]
                city2 = path[i]
                length += distances[city1, city2]
            return length
        return route(a) < route(b)

    search = encode_problem(domains, constraints, better)

    def decoder(assignment):
        return [assignment[i] for i in range(len(assignment))]

    return search, decoder
