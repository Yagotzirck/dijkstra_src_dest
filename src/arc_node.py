import collections

Arc = collections.namedtuple('Arc', ['tail', 'head', 'cost'])

class Node:
    __slots__ = (
    'dist_s',   # The distance label from the source node s
    'dist_t',   # The distance label from the destination node t

    # The predecessor node in the optimal path from the source node s
    # (used for Forward Dijkstra)
    'pred',     

    # The successor node in the optimal path towards the destination node t
    # (used for Reverse Dijkstra)
    'succ',     

    'in_arcs',  # A list of Arc tuples, representing the outgoing arcs
    'out_arcs'  # A list of Arc tuples, representing the incoming arcs
    )

    def __init__(self):
        self.dist_s = float('+inf')
        self.dist_t = float('+inf')
        self.pred = None
        self.succ = None
        self.in_arcs = list()
        self.out_arcs = list()