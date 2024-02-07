from arc_node import Arc

class InvalidArcError(Exception):
    """
    Raised whenever an invalid arc is read from the input JSON file passed as
    a parameter to Graph's constructor.
    NOTE: "Invalid" means that either of the following situations happened:

        - The arc has one or both "tail"/"head" fields referencing an invalid node
          (that is, a node ID outside the integer range [0, num_nodes-1]);

        - The arc has negative cost, which is not allowed in Dijkstra's algorithm
          since its proof of correctness wouldn't hold anymore.
        
        - The "tail"/"head" fields are identical (loopback arc leaving from
          a node and returning the same node)
    """
    def __init__(self, arc:Arc, details:str):
        super().__init__(arc, details)
        self.arc = arc
        self.details = details

class DuplicateArcError(Exception):
    """
    Raised whenever the Graph's constructor reads the same 
    arc from the input JSON file more than once.
    """
    def __init__(self, arc_without_cost:tuple):
        super().__init__(arc_without_cost)
        self.arc_without_cost = arc_without_cost