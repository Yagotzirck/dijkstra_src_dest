import json, io

from exceptions import InvalidArcError, DuplicateArcError
from arc_node import Arc, Node

class Graph:
    __slots__ = (
        # A list of Node tuples; each node is identified by its index
        # inside this list
        'nodes',  

        # The following two fields are sets of node indices, referencing 
        # Node tuples inside the "nodes" list defined above and representing,
        # respectively:
        #   - The set of permanent nodes (whose distance from the source node s
        #     is proven to be optimal);
        #   - The set of temporary nodes, whose distance's optimality has
        #     not been proven yet.
        #
        # Both fields are used for the FORWARD Dijkstra's implementation:
        # the algorithm starts with
        #   - The source node s in "perm_fwd";
        #   - All the other nodes in "temp_fwd".
        #
        'perm_fwd',
        'temp_fwd',

        # Everything that has already been said about "perm_fwd" and
        # "temp_fwd" still applies for the two fields below, except
        # for the following:
        #   - Both fields are used for the REVERSE Dijkstra's implementation;
        #   - The algorithm starts with the destination node t in "perm_rev", and all
        #     the other nodes in "temp_rev".
        'perm_rev',
        'temp_rev'
    )

    def __init__(self, file_json:io.TextIOWrapper):
        graph_dict = json.load(file_json)

        num_nodes = graph_dict['num_nodes']

        self.nodes = [Node() for _ in range(num_nodes)]

        # In order to check for duplicate arcs, we'll insert each (tail, head)
        # pair (without the cost, since two arcs with the same (tail, head)
        # values but different cost are still duplicates) inside a list of
        # sets (one list for each node).
        arc_sets = [set() for _ in range(num_nodes)]

        for curr_arc in graph_dict['arcs']:
            arc = Arc(*curr_arc)
            self.__validate_arc(arc, arc_sets)

            self.nodes[arc.tail].out_arcs.append(arc)
            self.nodes[arc.head].in_arcs.append(arc)

            arc_sets[arc.tail].add( (arc.tail, arc.head) )
    
    def reset_nodes(self):
        """
        Resets nodes' distance labels and predecessor/successor values,\n
        in order to reuse the graph for further executions.
        """
        for i in len(self.nodes):
            self.nodes[i].dist_s = float('+inf')
            self.nodes[i].dist_t = float('+inf')
            self.nodes[i].pred = None
            self.nodes[i].succ = None
    
    def __validate_arc(self, arc:Arc, arc_sets:list[set]):
        num_nodes = len(self.nodes)

        if  not(0 <= arc.tail < num_nodes):
            raise InvalidArcError(arc, f"Tail not in range [0, {num_nodes-1}]")

        if  not(0 <= arc.head < num_nodes):
            raise InvalidArcError(arc, f"Head not in range [0, {num_nodes-1}]")

        if arc.cost < 0:
            raise InvalidArcError(arc, "Negative cost")
        
        if arc.tail == arc.head:
            raise InvalidArcError(arc, "Loopback arc: tail is equal to head")

        arc_without_cost = (arc.tail, arc.head)
        if arc_without_cost in arc_sets[arc.tail]:
            raise DuplicateArcError(arc_without_cost)