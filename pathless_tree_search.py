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

    def step(self):
        """
        Executes a single step in the tree search.

        Returns:
            bool: True if a new best solution is found; False otherwise.
        """
        if not self._open:
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
                    return False
                elif self.better is not None and (self._best is None or self.better(succ_node, self._best)):
                    self._best = succ_node
                    return True

                
            elif self.order == "bfs":
                self._open.append(succ_node)
            else:
                self._open.insert(0,succ_node)
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

    n0 = {}

    def succ(p_assignment):
        unassign_value = [n for n in domains if n not in p_assignment]
        if not unassign_value: 
            return []
        
        var = unassign_value[0]
        succs = []

        for value in domains[var]:
            new_a = p_assignment.copy()
            new_a[var] = value
            if constraints(new_a):
                succs.append(new_a)
        return succs
    
    def goal(p_assignment):
        return len(p_assignment) == len(domains)
        
    return PathlessTreeSearch(n0, succ, goal, better, order)
