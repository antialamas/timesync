import unittest
import numpy as np
from src.simulation.quantum_channel import QuantumChannelSimulator

class TestQuantumChannel(unittest.TestCase):
    def setUp(self):
        """Initialize test environment before each test"""
        self.simulator = QuantumChannelSimulator()
        self.test_config = {
            'alice': {
                'mu1': 0.1,  # Signal state power
                'mu2': 0.05,  # Decoy state power
                'p1': 0.8,   # Probability of signal state
            },
            'bob': {
                'darkCount': 100,  # Dark counts per second
                'timeBin': 100e-12  # Time bin width in seconds
            },
            'channel': {
                'loss': 0.2,  # Channel loss in dB/km
                'length': 10,  # Channel length in km
                'syncError': 0.1  # Timing synchronization error
            },
            'processing': {
                'blockSize': 1000,  # Number of pulses per block
                'maxOffset': 50     # Maximum timing offset to check
            }
        }

    def test_config_validation(self):
        """Test configuration validation"""
        # Test valid configuration
        config = self.simulator.validate_config(self.test_config)
        self.assertAlmostEqual(config['alice']['mu1'], 0.1)
        self.assertAlmostEqual(config['alice']['mu2'], 0.05)
        
        # Test missing required parameter
        invalid_config = self.test_config.copy()
        del invalid_config['alice']['mu1']
        with self.assertRaises(ValueError):
            self.simulator.validate_config(invalid_config)
        
        # Test invalid parameter values
        invalid_config = self.test_config.copy()
        invalid_config['alice']['p1'] = 1.5  # Probability > 1
        with self.assertRaises(ValueError):
            self.simulator.validate_config(invalid_config)

    def test_state_generation(self):
        """Test quantum state generation"""
        config = self.simulator.validate_config(self.test_config)
        block_size = config['processing']['blockSize']
        
        # Generate states
        states = self.simulator.generate_states(config)
        
        # Check array dimensions
        self.assertEqual(len(states), block_size)
        
        # Check state values
        unique_states = np.unique(states)
        self.assertTrue(all(s in [config['alice']['mu1'], config['alice']['mu2']] 
                          for s in unique_states))
        
        # Check state distribution
        signal_count = np.sum(states == config['alice']['mu1'])
        signal_prob = signal_count / block_size
        self.assertAlmostEqual(signal_prob, config['alice']['p1'], delta=0.1)

    def test_channel_effects(self):
        """Test quantum channel effects"""
        config = self.simulator.validate_config(self.test_config)
        states = self.simulator.generate_states(config)
        
        # Apply channel effects
        transmitted = self.simulator.apply_channel_effects(states, config)
        
        # Check dimensions
        self.assertEqual(len(transmitted), len(states))
        
        # Check transmission is less than input (due to loss)
        self.assertTrue(np.mean(transmitted) < np.mean(states))
        
        # Check no negative values
        self.assertTrue(np.all(transmitted >= 0))

    def test_detection(self):
        """Test photon detection simulation"""
        config = self.simulator.validate_config(self.test_config)
        states = self.simulator.generate_states(config)
        transmitted = self.simulator.apply_channel_effects(states, config)
        
        # Simulate detection
        detected = self.simulator.simulate_detection(transmitted, config)
        
        # Check dimensions
        self.assertEqual(len(detected), len(transmitted))
        
        # Check binary output (0 or 1)
        self.assertTrue(np.all(np.logical_or(detected == 0, detected == 1)))
        
        # Check detection probability is reasonable
        detection_prob = np.mean(detected)
        self.assertTrue(0 <= detection_prob <= 1)

    def test_cross_correlation(self):
        """Test timing analysis using cross-correlation"""
        config = self.simulator.validate_config(self.test_config)
        states = self.simulator.generate_states(config)
        transmitted = self.simulator.apply_channel_effects(states, config)
        detected = self.simulator.simulate_detection(transmitted, config)
        
        # Calculate cross-correlation
        correlation = self.simulator.calculate_correlation(detected, config)
        
        # Check dimensions
        max_offset = config['processing']['maxOffset']
        expected_length = 2 * max_offset + 1
        self.assertEqual(len(correlation), expected_length)
        
        # Check correlation values are normalized
        self.assertTrue(np.all(correlation >= -1))
        self.assertTrue(np.all(correlation <= 1))
        
        # Check peak exists
        peak_idx = np.argmax(correlation)
        self.assertTrue(0 <= peak_idx < len(correlation))

    def test_statistics(self):
        """Test statistical analysis of results"""
        config = self.simulator.validate_config(self.test_config)
        states = self.simulator.generate_states(config)
        transmitted = self.simulator.apply_channel_effects(states, config)
        detected = self.simulator.simulate_detection(transmitted, config)
        
        # Calculate statistics
        stats = self.simulator.calculate_statistics(detected, states, config)
        
        # Check required statistics are present
        required_stats = ['total_counts', 'signal_counts', 'decoy_counts', 
                         'signal_rate', 'decoy_rate', 'qber_estimate']
        for stat in required_stats:
            self.assertIn(stat, stats)
        
        # Check value ranges
        self.assertTrue(stats['total_counts'] >= 0)
        self.assertTrue(0 <= stats['qber_estimate'] <= 1)
        self.assertTrue(stats['signal_counts'] <= stats['total_counts'])

if __name__ == '__main__':
    unittest.main()