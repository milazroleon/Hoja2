class PathlessTreeSearch:
    """
    Implements a pathless tree search that supports BFS and DFS exploration.

    Attributes:
        order (str): Search order strategy ("bfs" or "dfs").
        best (Any): Best known solution found during the search.
        active (bool): True if the search can continue, False otherwise.
    """

    def __init__(self, n0, succ, goal, better=None, order="bfs"):
        """
        Initializes the search instance.

        Args:
            n0 (Any): Initial node in the search.
            succ (Callable): Function that returns successors of a node.
            goal (Callable): Function that returns True if a node is a goal.
            better (Callable, optional): Comparator that returns True if first arg is better.
            order (str): Exploration strategy ("bfs" or "dfs").
        """
        self.n0 = n0
        self.succ = succ
        self.goal = goal
        self.better = better
        self.order = order

        self.reset()

    def reset(self):
        """
        Resets the search to its initial configuration.
        Useful for re-running the search from scratch.
        """
        self._open = [self.n0]
        self._best = None
        self._active = True

    def step(self):
        """
        Executes a single step in the tree search.

        Returns:
            bool: True if a new best solution is found; False otherwise.
        """
        if not self._open:
            self._active = False
            return False
        
        if self.order == "bfs":
            node = self._open.pop(0)
        else: 
            node = self._open.pop()

        for succ_node in self.succ(node):
            if self.goal(succ_node):
                if self.better is None:
                    self._best = succ_node
                    self._open = []
                    self._active = Fals
                    return True
                elif self._best is None or self.better(succ_node, self._best):
                    self._best = succ_node
                    return True
            if self.order == "bfs":
                self._open.append(succ_node)
            else:
                self._open.insert(0, succ_node)

        if not self._open:
            self._active = False
        return False

    @property
    def active(self):

        """
        Indicates whether the search is still ongoing.

        Returns:
            bool: True if there are nodes left to explore.
        """

        if len(self._open) > 0:
            return True
        else:
            return False


    @property
    def best(self):

        """
        Returns the current best solution.

        Returns:
            Any: The best node found so far.
        """

        return self._best


def encode_problem(domains, constraints, better=None, order="bfs"):

    """
    Encodes a fixed-variable search problem as a tree search.

    Args:
        domains (dict): Mapping of variable names to domain lists.
        constraints (Callable): Function that returns True if partial assignment is valid.
        better (Callable, optional): Function that compares two full assignments.

    Returns:
        PathlessTreeSearch: Configured search object.
    """

    variables = list(domains.keys())
    n0 = {}

    def succ(assignment):
        if len(assignment) == len(variables):
            return []

        var = variables[len(assignment)]
        children = []

        for value in domains[var]:
            new_assignment = assignment.copy()
            new_assignment[var] = value
            if constraints(new_assignment):
                children.append(new_assignment)

        return children

    def goal(assignment):
        return len(assignment) == len(variables)

    return PathlessTreeSearch(n0=n0, succ=succ, goal=goal, better=better, order=order)
