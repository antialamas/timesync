import matplotlib.pyplot as plt
import numpy as np
from simulation.quantum_channel import QuantumChannelSimulator

def generate_example_plots():
    """Generate example plots showing quantum channel simulation results"""
    
    # Initialize simulator with default parameters
    simulator = QuantumChannelSimulator()
    
    # Example configuration
    config = {
        'alice': {
            'mu1': 0.1,
            'mu2': 0.05,
            'p1': 0.8
        },
        'bob': {
            'darkCount': 100,
            'timeBin': 100
        },
        'channel': {
            'loss': 0.2,
            'syncError': 0.1
        },
        'processing': {
            'blockSize': 1000,
            'maxOffset': 50
        }
    }
    
    # Run simulation
    results = simulator.run(config)
    
    # Plot cross-correlation
    plt.figure(figsize=(10, 6))
    plt.plot(results['time_points'], results['cross_correlation'], 'b-')
    plt.title('Cross-correlation vs Time Offset')
    plt.xlabel('Time Offset (bins)')
    plt.ylabel('Correlation')
    plt.grid(True)
    plt.savefig('static/correlation.png')
    plt.close()
    
    # Plot photon counts
    plt.figure(figsize=(10, 6))
    counts = np.array(results['counts'])
    time_bins = np.arange(len(counts)) * config['bob']['timeBin']
    plt.plot(time_bins, counts, 'b-', label='Detection Events')
    plt.title('Photon Detection Events')
    plt.xlabel('Time (ps)')
    plt.ylabel('Counts')
    plt.legend()
    plt.grid(True)
    plt.savefig('static/counts.png')
    plt.close()
    
    # Print statistics
    print("\nSimulation Statistics:")
    print(f"Total Counts: {results['statistics']['total_counts']}")
    print(f"Mean Count Rate: {results['statistics']['mean_count_rate']:.2f} cps")
    print(f"QBER: {results['statistics']['qber']:.2%}")
    print(f"Synchronization Success: {results['statistics']['sync_success']}")

if __name__ == '__main__':
    generate_example_plots()