import unittest

from simulation.model import CommunicationNetwork
from simulation.model import EntityNotFound


class ModelTest(unittest.TestCase):

    cn = CommunicationNetwork({'h1': ['v1', 'v2'], 'h2': ['v2', 'v3'], 'h3': ['v3', 'v4']}, {'h1': 1, 'h2': 2, 'h3': 3})

    def test_vertices(self):
        self.assertEqual(len(ModelTest.cn.vertices()), 4)
        self.assertEqual(ModelTest.cn.vertices('h1'), {'v1', 'v2'})

    def test_hyperedges(self):
        self.assertEqual(len(ModelTest.cn.hyperedges()), 3)
        self.assertEqual(ModelTest.cn.hyperedges('v1'), {'h1'})

    def test_timings(self):
        # Testing the timings associated with each hyperedge (h1, h2, and h3) in the communication network
        self.assertEqual(ModelTest.cn.timings('h1'), 1)
        self.assertEqual(ModelTest.cn.timings('h2'), 2)
        self.assertEqual(ModelTest.cn.timings('h3'), 3)
    
    def test_channels(self):
        # Testing the channels (hyperedges) associated with each vertex (v1, v2, and v3) in the communication network
        self.assertEqual(ModelTest.cn.channels('v1'), {'h1'})
        self.assertEqual(ModelTest.cn.channels('v2'), {'h1', 'h2'})
        self.assertEqual(ModelTest.cn.channels('v3'), {'h2', 'h3'})
    
    def test_participants(self):
        # Testing the participants (vertices) associated with each hyperedge (h1, h2, and h3) in the communication network
        self.assertEqual(ModelTest.cn.participants('h1'), {'v1', 'v2'})
        self.assertEqual(ModelTest.cn.participants('h2'), {'v2', 'v3'})
        self.assertEqual(ModelTest.cn.participants('h3'), {'v3', 'v4'})
    
    def test_invalid_vertex(self):
        # Begin a context where we expect an EntityNotFound exception to be raised
        with self.assertRaises(EntityNotFound):
            ModelTest.cn.hyperedges('v5')
    
    def test_invalid_hyperedge(self):
        # Begin a context where we expect an EntityNotFound exception to be raised
        with self.assertRaises(EntityNotFound):
            ModelTest.cn.vertices('h4')
    
    # This test is checking that the appropriate exception is thrown when trying to access an entity that doesn't exist    
    def test_entity_not_found(self):
        with self.assertRaises(EntityNotFound):
            self.cn.vertices('h4')
        with self.assertRaises(EntityNotFound):
            self.cn.hyperedges('v5')
            
class ModelDataTest(unittest.TestCase):
    def test_model_with_data(self):
        communciation_network = CommunicationNetwork.from_json('./data/networks/microsoft.json.bz2')
        self.assertEqual(len(communciation_network.participants()), 37103)
        self.assertEqual(len(communciation_network.channels()), 309740)

        self.assertEqual(len(communciation_network.vertices()), 37103)
        self.assertEqual(len(communciation_network.hyperedges()), 309740)
    
    def test_data_integrity(self):
        # Load the communication network from a JSON file
        communciation_network = CommunicationNetwork.from_json('./data/networks/microsoft.json.bz2')

        # Ensure all channels have at least one participant
        for channel in communciation_network.channels():
            participants = communciation_network.participants(channel)
            self.assertGreater(len(participants), 0, f"Channel {channel} has no participants")

        # Ensure all participants are in at least one channel
        for participant in communciation_network.participants():
            channels = communciation_network.channels(participant)
            self.assertGreater(len(channels), 0, f"Participant {participant} is in no channel")
            