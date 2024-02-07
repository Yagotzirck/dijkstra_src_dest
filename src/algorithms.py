from collections import deque

from graph import Graph
from exceptions import NoDirectedPathError

def dijkstra_fwd(graph:Graph, src:int, dest:int) -> deque:
    graph.init_state(src, dest)

    while graph.temp_fwd:
        # Get the temporary node with the minimum distance label
        i = min(
            graph.temp_fwd,
            key = lambda nodeID: graph.nodes[nodeID].dist_s
        )

        graph.make_node_perm_fwd(i)

        # We found the optimal path from the source to the destination node
        if i == dest:
            break

        i_dist_s = graph.nodes[i].dist_s

        for arc in graph.nodes[i].out_arcs:
            j = arc.head
            if graph.nodes[j].dist_s > i_dist_s + arc.cost:
                # Distance update
                graph.nodes[j].dist_s = i_dist_s + arc.cost
                graph.nodes[j].pred = i

                # Add the head j to the set of temporary nodes.
                # NOTE: it doesn't matter if it's already there
                # (nothing happens), and it can't possibly be permanent
                # since we just found a path from the source node "src" which
                # is shorter than the previous one.
                graph.temp_fwd.add(j)
        
    # If the destination node doesn't have a predecessor,
    # there is no directed path from the src to dest
    if graph.nodes[dest].pred == None:
        raise NoDirectedPathError(src, dest)
    
    # Return the path from the source to the destination,
    # by tracing the destination node's predecessors.
    src_dest_path = deque()
    curr_node = graph.nodes[dest]
    src_dest_path.appendleft(dest)

    while (curr_pred := curr_node.pred) != None:
        src_dest_path.appendleft(curr_pred)
        curr_node = graph.nodes[curr_pred]

    return src_dest_path