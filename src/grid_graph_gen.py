import random, sys, json


def grid_graph_gen(num_side_nodes:int, max_cost:int) -> dict:
    """Generates a 4-neighbors grid graph made up of
    (num_side_nodes) * (num_side_nodes) nodes, with
    randomized arc costs inside the range [0, max_cost].
    """
    num_nodes = num_side_nodes * num_side_nodes

    graph_dict = {
        'num_nodes': num_nodes,
        'arcs': list()
    }

    random.seed()

    for i in range(num_side_nodes):
        row_node = i * num_side_nodes
        for j in range(num_side_nodes):
            # NOTE: for each direction, we check that
            # the head index is not out of bounds.
            # There are more efficient ways to deal with this, but this is
            # a one-off generator to save JSON files and therefore I prefer
            # code simplicity over efficiency.

            nodeId = row_node + j

            # East
            if j != num_side_nodes - 1: 
                arc = ( nodeId, nodeId+1, random.randint(0, max_cost) )
                graph_dict['arcs'].append(arc)
            
            # South
            if i != 0:
                arc = ( nodeId, nodeId - num_side_nodes, random.randint(0, max_cost) )
                graph_dict['arcs'].append(arc)
            
            # West
            if j != 0:
                arc = ( nodeId, nodeId - 1, random.randint(0, max_cost) )
                graph_dict['arcs'].append(arc)
            
            # North
            if i != num_side_nodes - 1:
                arc = ( nodeId, nodeId + num_side_nodes, random.randint(0, max_cost) )
                graph_dict['arcs'].append(arc)
    
    return graph_dict


if __name__ == '__main__':

    usage_msg = (
        "\nUsage:\n"
        "python grid_graph_gen.py <num_side_nodes> <max_cost> <output_json_filename>\n"
    )
    if len(sys.argv) != 4:
        print(usage_msg)
        quit()

    try:
        num_side_nodes = int(sys.argv[1])
    except ValueError:
        raise ValueError("Parameter 'num_side_nodes' must be integer")

    try:
        max_cost = int(sys.argv[2])
    except ValueError:
        raise ValueError("Parameter 'max_cost' must be integer")
    
    output_json_filename = sys.argv[3]
    if not output_json_filename.endswith('.json'):
        raise UserWarning("Parameter 'output_json_filename' must have .json extension")
    
    graph_dict = grid_graph_gen(num_side_nodes, max_cost)

    with open(output_json_filename, 'w') as f:
        json.dump(graph_dict, f)
    
    print("The grid graph has been saved.")