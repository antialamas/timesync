#!/usr/bin/env python3
import argparse
import logging
from simulation.quantum_channel import QuantumChannelSimulator
from generate_plots import PlotGenerator
import matplotlib.pyplot as plt

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def parse_args():
    parser = argparse.ArgumentParser(description='Quantum Channel Simulation')
    
    # Alice's parameters
    parser.add_argument('--mu1', type=float, default=0.1,
                      help='Signal state power (photons/pulse)')
    parser.add_argument('--mu2', type=float, default=0.05,
                      help='Decoy state power (photons/pulse)')
    parser.add_argument('--p1', type=float, default=0.8,
                      help='Probability of signal state')
    
    # Bob's parameters
    parser.add_argument('--dark-count', type=int, default=100,
                      help='Dark count rate (counts/second)')
    parser.add_argument('--time-bin', type=float, default=100e-12,
                      help='Time bin width (seconds)')
    
    # Channel parameters
    parser.add_argument('--loss', type=float, default=0.2,
                      help='Channel loss (dB/km)')
    parser.add_argument('--length', type=float, default=10,
                      help='Channel length (km)')
    parser.add_argument('--sync-error', type=float, default=0.1,
                      help='Timing synchronization error (ps)')
    
    # Processing parameters
    parser.add_argument('--block-size', type=int, default=1000,
                      help='Number of pulses per block')
    parser.add_argument('--max-offset', type=int, default=50,
                      help='Maximum timing offset to check')
    
    # Output parameters
    parser.add_argument('--show-plots', action='store_true',
                      help='Show plots instead of saving to files')
    
    return parser.parse_args()

def main():
    args = parse_args()
    
    # Create configuration dictionary
    config = {
        'alice': {
            'mu1': args.mu1,
            'mu2': args.mu2,
            'p1': args.p1
        },
        'bob': {
            'darkCount': args.dark_count,
            'timeBin': args.time_bin
        },
        'channel': {
            'loss': args.loss,
            'length': args.length,
            'syncError': args.sync_error * 1e-12  # Convert ps to seconds
        },
        'processing': {
            'blockSize': args.block_size,
            'maxOffset': args.max_offset
        }
    }
    
    # Initialize simulator and plot generator
    simulator = QuantumChannelSimulator()
    plot_generator = PlotGenerator()
    
    try:
        # Run simulation
        logger.info("Generating quantum states...")
        states = simulator.generate_states(config)
        
        logger.info("Applying channel effects...")
        transmitted = simulator.apply_channel_effects(states, config)
        
        logger.info("Simulating detection...")
        detected = simulator.simulate_detection(transmitted, config)
        
        logger.info("Calculating correlation...")
        correlation = simulator.calculate_correlation(detected, config)
        
        logger.info("Calculating statistics...")
        stats = simulator.calculate_statistics(detected, states, config)
        
        # Generate or display plots
        if args.show_plots:
            # Show plots interactively
            plt.figure(1)
            plot_generator.plot_correlation(correlation, config)
            plt.title("Cross-correlation Analysis")
            
            plt.figure(2)
            plot_generator.plot_counts(detected, config)
            plt.title("Photon Count Distribution")
            
            plt.show()
        else:
            # Save plots to files
            plot_generator.plot_correlation(correlation, config, 'correlation.png')
            plot_generator.plot_counts(detected, config, 'counts.png')
            logger.info("Plots saved as correlation.png and counts.png")
        
        # Display statistics
        logger.info("\nSimulation Results:")
        logger.info(f"Total counts: {stats['total_counts']}")
        logger.info(f"Signal counts: {stats['signal_counts']}")
        logger.info(f"Decoy counts: {stats['decoy_counts']}")
        logger.info(f"Signal rate: {stats['signal_rate']:.2f} counts/s")
        logger.info(f"Decoy rate: {stats['decoy_rate']:.2f} counts/s")
        logger.info(f"QBER estimate: {stats['qber_estimate']:.4f}")
        
    except Exception as e:
        logger.error(f"Simulation failed: {str(e)}")
        return 1
    
    return 0

if __name__ == '__main__':
    exit(main())