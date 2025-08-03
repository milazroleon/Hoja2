from typing import Any, Callable, List, Optional

class PathlessTreeSearch:

    def __init__(self, n0, succ, goal, better=None, order="bfs"):

        self.n0: Any = n0
        self.succ: Callable = succ
        self.goal: Callable = goal
        self.better: Optional[Callable] = better
        self.order: str = order

        self._open: List[Any] = [n0]
        self._best: Optional[Any] = None


    def reset(self):
        
        self._open = [self.n0]
        self._best = None

    def step(self):

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
        if len(self._open) > 0:
            return True
        else:
            return False
    

    @property
    def best(self):
        return self._best

def encode_problem(domains, constraints, better=None):

    n0 = {}

    def succ(p_assignment):
        unassign_value = [ n for n in domains if n not in p_assignment]
        if not unassign_value: 
            return []
        
        var = unassign_value[0]
        succs = []

        for values in domains[var]:
            new_a = p_assignment.copy()
            new_a[var] = values
            if constraints(new_a):
                succs.append(new_a)
        return succs
    
    def goal(p_assignment):
        if len(p_assignment) == len(domains):
            return True
        else: 
            return False
        
    return PathlessTreeSearch(n0, succ, goal, better, order="bfs")
