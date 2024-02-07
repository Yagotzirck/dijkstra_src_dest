import unittest
from io import StringIO
from collections import deque

from graph import Graph
from algorithms import dijkstra_fwd
from exceptions import NoDirectedPathError


graph_valid = """
{
    "num_nodes": 6,
    "arcs": [
        [0, 1, 2],
        [0, 2, 4],

        [1, 2, 1],
        [1, 3, 4],
        [1, 4, 2],

        [2, 4, 3],

        [3, 5, 2],

        [4, 3, 3],
        [4, 5, 2]
    ]
}
"""

class TestDijkstraBase:
    """
    Base class to be inherited from test classes related to each of
    the three Dijkstra's variants.
    Each derived class must do the following in setUp():
        - Call super().base_setUp(), to create the test graph;
        - define a class method "dijkstra_func", assigning to it the
          Dijkstra's variant to be tested.
    """
    def base_setUp(self):
        with StringIO(graph_valid) as f:
            self.graph = Graph(f)

    def test_optimal_paths(self):
        path_0_5 = self.dijkstra_func(self.graph, 0, 5)
        self.assertEqual(path_0_5, deque([0, 1, 4, 5]))

        path_0_2 = self.dijkstra_func(self.graph, 0, 2)
        self.assertEqual(path_0_2, deque([0, 1, 2]))

        path_2_3 = self.dijkstra_func(self.graph, 2, 3)
        self.assertEqual(path_2_3, deque([2, 4, 3]))
    
    def test_invalid_src_node_error(self):
        with self.assertRaises(KeyError):
            path = self.dijkstra_func(self.graph, 100, 1)

    def test_invalid_dest_node_error(self):
        with self.assertRaises(KeyError):
            path = self.dijkstra_func(self.graph, 1, 100)

    def test_src_equal_to_dest_error(self):
        with self.assertRaises(ValueError):
            path = self.dijkstra_func(self.graph, 1, 1)

    def checkIfRaisesNoDirectedPath(self, src:int, dest:int):
        """Helper function for test_unreachable_dest, to reduce cluttering."""
        with self.assertRaises(NoDirectedPathError) as context_manager:
            path_src_dest = self.dijkstra_func(self.graph, src, dest)
        
        exc = context_manager.exception
        self.assertEqual(exc.src, src)
        self.assertEqual(exc.dest, dest)

    def test_unreachable_dest(self):
        self.checkIfRaisesNoDirectedPath(5, 0)
        self.checkIfRaisesNoDirectedPath(3, 2)
        self.checkIfRaisesNoDirectedPath(4, 1)


class TestDijkstraFwd(unittest.TestCase, TestDijkstraBase):
    def setUp(self):
        super().base_setUp()
        self.dijkstra_func = dijkstra_fwd
        

if __name__ == '__main__':
    unittest.main() 