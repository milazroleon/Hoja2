from pathless_tree_search import PathlessTreeSearch
from connect4.connect_state import ConnectState
import numpy as np

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
    domains = {}

    for row in range(9):
        for col in range(9):
            if sudoku[row, col] == 0:
                used = set(sudoku[row, :]) | set(sudoku[:, col])
                block = sudoku[(row // 3) * 3: (row // 3) * 3 + 3,
                               (col // 3) * 3: (col // 3) * 3 + 3]
                used |= set(block.flatten())
                domains[(row, col)] = [v for v in range(1, 10) if v not in used]

    def constraints(assignment):
        board = sudoku.copy()
        for (r, c), val in assignment.items():
            board[r, c] = val

        for (r, c), val in assignment.items():
            if list(board[r, :]).count(val) > 1:
                return False
            if list(board[:, c]).count(val) > 1:
                return False
            br, bc = 3 * (r // 3), 3 * (c // 3)
            block = board[br:br+3, bc:bc+3].flatten()
            if list(block).count(val) > 1:
                return False
        return True

    def decoder(solution):
        filled = sudoku.copy()
        if solution is None:
            return filled
        for (r, c), v in solution.items():
            filled[r, c] = v
        return filled

    search = encode_problem(domains, constraints, order="bfs")
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

    def decoder(final):
        jobs = len(d)
        result = [0] * jobs
        for job, machine in final.items():
            result[job] = machine
        return result
    
    search = encode_problem(domains, constraints, better, order="dfs")   
    
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

    initial_state = ConnectState()
    red_first_move = opponent(initial_state)
    state_after_red = initial_state.transition(red_first_move)

    n0 = (state_after_red, [])

    def goal(state):
        board, _ = state
        return board.get_winner() == 1

    def succ(state):
        board, yellow_moves = state
        if board.is_final():
            return []

        successors = []
        for yellow_col in board.get_free_cols():
            yellow_board = board.transition(yellow_col)
            new_moves = yellow_moves + [yellow_col]

            if yellow_board.get_winner() == 1:
                successors.append((yellow_board, new_moves))
            else:
                red_col = opponent(yellow_board)
                red_board = yellow_board.transition(red_col)
                successors.append((red_board, new_moves))

        return successors

    def decoder(state):
        if state is None:
            return []
        return state[1]

    search = PathlessTreeSearch(n0=n0, succ=succ, goal=goal, order="bfs")
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
        # Solo permitimos rutas sin repetir ciudades
        values = list(p_assignment.values())
        return len(values) == len(set(values))

    def better(a, b):
        def route(path):
            length = 0
            for i in range(1, len(path)):
                city1 = path[i - 1]
                city2 = path[i]
                d = distances[city1, city2]
                if d == 0: 
                    return float("inf")
                length += d
            return length
        return route(a) < route(b)

    search = encode_problem(domains, constraints, better)

    def decoder(assignment):
        return [assignment[i] for i in range(len(assignment))]

    return search, decoder
