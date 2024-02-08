from collections import deque

from graph import Graph
from exceptions import NoDirectedPathError

def dijkstra_fwd(graph:Graph, src:int, dest:int) -> deque:
    """Forward Dijkstra algorithm's implementation."""
    graph.init_state(src, dest)

    while graph.temp_fwd:
        # Get the temporary node with the minimum distance from src
        i = min(
            graph.temp_fwd,
            key = lambda nodeID: graph.nodes[nodeID].dist_s
        )

        graph.make_node_perm_fwd(i)

        if i == dest:
            # We found the optimal path from the source to the destination node
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
                # (nothing happens), and it can't possibly be in the set
                # of permanent nodes since we just found a path from the
                # source node "src" which is shorter than the previous one.
                graph.temp_fwd.add(j)
        
    # If the destination node doesn't have a predecessor,
    # there is no directed path from src to dest
    if graph.nodes[dest].pred is None:
        raise NoDirectedPathError(src, dest)
    
    # Return the path from the source to the destination,
    # by tracing back the destination node's predecessors.
    src_dest_path = deque([dest])
    curr_node = graph.nodes[dest]

    while (curr_pred := curr_node.pred) is not None:
        src_dest_path.appendleft(curr_pred)
        curr_node = graph.nodes[curr_pred]

    return src_dest_path


def dijkstra_rev(graph:Graph, src:int, dest:int) -> deque:
    """Reverse Dijkstra algorithm's implementation."""
    graph.init_state(src, dest)

    while graph.temp_rev:
        # Get the temporary node with the minimum distance from dest
        j = min(
            graph.temp_rev,
            key = lambda nodeID: graph.nodes[nodeID].dist_t
        )

        graph.make_node_perm_rev(j)

        if j == src:
            # We found the optimal path from the source to the destination node
            break

        j_dist_t = graph.nodes[j].dist_t

        for arc in graph.nodes[j].in_arcs:
            i = arc.tail
            if graph.nodes[i].dist_t > j_dist_t + arc.cost:
                # Distance update
                graph.nodes[i].dist_t = j_dist_t + arc.cost
                graph.nodes[i].succ = j

                # Add the tail i to the set of temporary nodes.
                # NOTE: it doesn't matter if it's already there
                # (nothing happens), and it can't possibly be in the set
                # of permanent nodes since we just found a path from the
                # destination node "dest" which is shorter than the previous one.
                graph.temp_rev.add(i)
        
    # If the source node doesn't have a successor,
    # there is no directed path from src to dest
    if graph.nodes[src].succ is None:
        raise NoDirectedPathError(src, dest)
    
    # Return the path from the source to the destination,
    # by tracing forward the source node's successors.
    src_dest_path = deque([src])
    curr_node = graph.nodes[src]

    while (curr_succ := curr_node.succ) is not None:
        src_dest_path.append(curr_succ)
        curr_node = graph.nodes[curr_succ]

    return src_dest_path