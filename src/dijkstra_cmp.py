from sys import argv
from collections import deque
from time import time

from graph import Graph
from algorithms import dijkstra_fwd, dijkstra_rev, dijkstra_bidir

def validate_args(argv) -> tuple:
    usage_msg = (
        "\nUsage:\n"
        "python dijkstra_cmp.py <input_graph_json> <src_node> <dest_node>\n"
    )
    if len(argv) != 4:
        print(usage_msg)
        quit()
    
    input_graph_json = argv[1]
    
    if not input_graph_json.endswith('.json'):
        print("Parameter 'input_graph_json' must have .json extension")
        quit()
    
    try:
        src_node = int(argv[2])
    except ValueError:
        print("Parameter 'src_node' must be integer")
        quit()
    
    try:
        dest_node = int(argv[3])
    except ValueError:
        print("Parameter 'dest_node' must be integer")
        quit()
    
    return (input_graph_json, src_node, dest_node)


def print_results(
    path:deque,
    perf_times:list,
    perm_nodes:list,
    num_total_nodes:int) -> None:

    print(40 * '=')
    print('RESULTS\n')

    print('Optimal path:')
    for i, node in enumerate(path, start=1):
        print(f'{i:>10}: {node:>10}')
    
    print()
    print(40 * '-')

    print(f'Number of nodes in graph: {num_total_nodes}\n')

    print("{0:->12}{1:->16}{2:->16}{3:->20}".format("", "Forward", "Reverse", "Bidirectional"))
    print("{0:<12}{1:>14.3f}{2:>16.3f}{3:>20.3f}".format("Execution time", *perf_times))
    print("{0:<12}{1:>13}{2:>16}{3:>20}".format("Permanent nodes", *perm_nodes))

    print(64 * '-')
    print()


if __name__ == '__main__':
    input_graph_json, src_node, dest_node = validate_args(argv)

    print("Building the graph...", end=' ', flush=True)
    with open(input_graph_json, 'r') as f:
        graph = Graph(f)
    print('done\n')
    
    alg_funcs = [dijkstra_fwd, dijkstra_rev, dijkstra_bidir]
    alg_perf_times = list()
    alg_perm_nodes = list() 
    
    for alg_func in alg_funcs:
        print(f'Executing {alg_func.__name__}()...', end=' ', flush=True)

        start = time()
        path = alg_func(graph, src_node, dest_node)
        perf_time = time() - start

        print('done')

        alg_perf_times.append(perf_time)

        num_perm_nodes = len( graph.perm_fwd.union(graph.perm_rev) )
        alg_perm_nodes.append(num_perm_nodes)
    
    num_total_nodes = len(graph.nodes)

    print_results(path, alg_perf_times, alg_perm_nodes, num_total_nodes)




    







