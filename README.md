# dijkstra_src_dest
A Python implementation and comparison of three Dijkstra's algorithm variants (Forward, Reverse, Bidirectional) to find the shortest path between a source node and a destination node.

## Usage
### dijkstra_cmp.py
Open a command prompt and type:

    python dijkstra_cmp.py <json_graph> <src_node> <dest_node>
where <src_node> and <dest_node> are integer node IDs representing the path's beginning and end inside the graph, respectively.

As for <json_graph>, it is the input json file having the following structure:

      {

        "num_nodes": <number of nodes in the graph>,
  
        "arcs": [
          [<tail1>, <head1>, <cost1>],
          [<tail2>, <head2>, <cost2>],
          ...
          [<tailN>, <headN>, <costN>]
        ]
      }

Note that:
- The **tail** and **head** values must be inside the inclusive range [0, num_nodes - 1];
- The **cost** values must be nonnegative;
- **Duplicate arcs** *(that is, arcs sharing the same tail and head values)* and **loopback arcs** *(arcs where the tail is equal to the head, i.e. returning to the same node)* are not allowed.

Once the execution of the three Dijkstra's variants terminates, the following results are shown:
- The optimal path;
- For each algorithm, the execution time and the number of nodes it marked as permanent *(less is better)*.

### grid_graph_gen.py
Open a command prompt and type:

    python grid_graph_gen.py <num_side_nodes> <max_cost> <output_json_filename>
to generate a .json undirected grid graph, usable as input for **dijkstra_cmp.py**.

For instance, the following command generates a **3x3** grid graph with randomized arc costs between 0 and **20**, and saves it as **grid.json**:

    python grid_graph_gen.py 3 20 grid.json
