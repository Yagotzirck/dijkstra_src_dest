import unittest
from io import StringIO

from graph import Graph
from arc_node import Arc
from exceptions import InvalidArcError, DuplicateArcError


graph_negCostArc = """
{
    "num_nodes": 5,
    "arcs": [
        [0, 1, 2],
        [0, 2, 4],

        [1, 2, 1],
        [1, 3, -100],
        [1, 4, 2]
    ]
}
"""

graph_duplicateArc = """
{
    "num_nodes": 3,
    "arcs": [
        [0, 1, 2],
        [0, 2, 4],

        [1, 2, 1],

        [0, 2, 100]
    ]
}
"""

graph_illegalNodeInTailArc = """
{
    "num_nodes": 3,
    "arcs": [
        [0, 1, 2],
        [0, 2, 4],

        [1, 2, 1],

        [5, 2, 100]
    ]
}
"""
graph_illegalNodeInHeadArc = """
{
    "num_nodes": 3,
    "arcs": [
        [0, 1, 2],
        [0, 2, 4],

        [1, 2, 1],

        [2, -8, 100]
    ]
}
"""

graph_loopbackArc = """
{
    "num_nodes": 3,
    "arcs": [
        [0, 1, 2],
        [0, 2, 4],

        [1, 1, 100]
    ]
}
"""


class TestDijkstraGraphValidation(unittest.TestCase):
    def checkIfRaises(self, graph_json:str, exception):
        """Helper function for test methods, to reduce cluttering."""
        with StringIO(graph_json) as f:
            with self.assertRaises(exception) as context_manager:
                graph = Graph(f)
        
        return context_manager.exception

    def test_arc_negativeCost(self):
        exc = self.checkIfRaises(graph_negCostArc, InvalidArcError)
        self.assertEqual(exc.arc, Arc(1, 3, -100))
        self.assertEqual(exc.details, "Negative cost")

    def test_arc_duplicate(self):
        exc = self.checkIfRaises(graph_duplicateArc, DuplicateArcError)
        self.assertEqual(exc.arc_without_cost, (0, 2))

    def test_arc_illegalNodeInTail(self):
        exc = self.checkIfRaises(graph_illegalNodeInTailArc, InvalidArcError)
        self.assertEqual(exc.arc, Arc(5, 2, 100))
        self.assertEqual(exc.details, "Tail not in range [0, 2]")


    def test_arc_illegalNodeInHead(self):
        exc = self.checkIfRaises(graph_illegalNodeInHeadArc, InvalidArcError)
        self.assertEqual(exc.arc, Arc(2, -8, 100))
        self.assertEqual(exc.details, "Head not in range [0, 2]")

    def test_arc_loopback(self):
        exc = self.checkIfRaises(graph_loopbackArc, InvalidArcError)
        self.assertEqual(exc.arc, Arc(1, 1, 100))
        self.assertEqual(exc.details, "Loopback arc: tail is equal to head")


if __name__ == '__main__':
    unittest.main()