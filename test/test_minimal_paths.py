import unittest

from simulation.model import CommunicationNetwork
from simulation.minimal_paths import single_source_dijkstra_vertices, single_source_dijkstra_hyperedges, DistanceType


class MinimalPath(unittest.TestCase):
    cn = CommunicationNetwork({'h1': ['v1', 'v2'], 'h2': ['v2', 'v3'], 'h3': ['v3', 'v4']}, {'h1': 1, 'h2': 2, 'h3': 3})

    def test_1(self):
        self.assertEqual(single_source_dijkstra_vertices(MinimalPath.cn, 'v1', DistanceType.SHORTEST, min_timing=0), {'v2': 1, 'v3': 2, 'v4': 3})

    def test_2(self):
        result_1 = single_source_dijkstra_vertices(MinimalPath.cn, 'v1', DistanceType.SHORTEST, min_timing=0)
        result_2 = single_source_dijkstra_hyperedges(MinimalPath.cn, 'v1', DistanceType.SHORTEST, min_timing=0)
        self.assertEqual(result_1, result_2, 'Single-source Dijkstra implementations are not equivalent')

    def test_3(self):
        result_1 = single_source_dijkstra_vertices(MinimalPath.cn, 'v1', DistanceType.FASTEST, min_timing=0)
        result_2 = single_source_dijkstra_hyperedges(MinimalPath.cn, 'v1', DistanceType.FASTEST, min_timing=0)
        self.assertEqual(result_1, result_2, 'Single-source Dijkstra implementations are not equivalent')

    def test_4(self):
        result_1 = single_source_dijkstra_vertices(MinimalPath.cn, 'v1', DistanceType.FOREMOST, min_timing=0)
        result_2 = single_source_dijkstra_hyperedges(MinimalPath.cn, 'v1', DistanceType.FOREMOST, min_timing=0)
        self.assertEqual(result_1, result_2, 'Single-source Dijkstra implementations are not equivalent')
        
    # Checks whether the function handles a non-existent source vertex correctly. 
    # It is expected to raise an Exception.
    def test_nonexistent_source_vertex(self):
        with self.assertRaises(Exception):
            single_source_dijkstra_vertices(MinimalPath.cn, 'v5', DistanceType.SHORTEST, min_timing=0)
    
    # Checks how the function handles a vertex with a self-loop.
    # It is expected that the self-loop should not affect the shortest path calculation.
    def test_vertex_with_self_loop(self):
        cn = CommunicationNetwork({'h1': ['v1', 'v2'], 'h2': ['v2', 'v3'], 'h3': ['v3', 'v3']}, {'h1': 1, 'h2': 2, 'h3': 3})
        result = single_source_dijkstra_vertices(cn, 'v1', DistanceType.SHORTEST, min_timing=0)
        self.assertEqual(result, {'v2': 1, 'v3': 2}, "A self-loop should not affect the shortest path")
