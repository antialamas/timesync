import numpy as np
from scipy.signal import correlate
from typing import Dict, Any, Tuple, Optional
from dataclasses import dataclass

@dataclass
class SimulationConfig:
    """Configuration parameters for quantum channel simulation"""
    # Alice parameters
    signal_power: float  # mu1: mean photon number per signal pulse
    decoy_power: float  # mu2: mean photon number per decoy pulse
    signal_prob: float  # Probability of sending signal state
    
    # Bob parameters
    dark_count_rate: float  # Dark count rate in cps
    time_bin: float  # Time bin width in picoseconds
    
    # Channel parameters
    channel_loss_db: float  # Channel loss in dB
    sync_error_ppm: float  # Clock synchronization error in parts per million
    
    # Processing parameters
    block_size: int  # Number of time bins to accumulate
    max_offset: int  # Maximum expected clock offset in bins

@dataclass
class SimulationResults:
    """Results from quantum channel simulation"""
    time_points: np.ndarray
    cross_correlation: np.ndarray
    counts: np.ndarray
    peak_position: int
    total_counts: int
    mean_count_rate: float
    qber: float
    sync_success: bool

class QuantumChannelSimulator:
    """Simulates quantum channel communication between Alice and Bob"""
    
    def __init__(self):
        """Initialize simulator"""
        self.sampling_rate = 10e9  # 10 GHz sampling rate
        
    def validate_config(self, config: Dict[str, Any]) -> SimulationConfig:
        """
        Validate and convert configuration dictionary to SimulationConfig
        
        Args:
            config: Dictionary of simulation parameters
            
        Returns:
            Validated SimulationConfig object
            
        Raises:
            ValueError: If parameters are invalid
        """
        try:
            return SimulationConfig(
                signal_power=float(config['alice']['mu1']),
                decoy_power=float(config['alice']['mu2']),
                signal_prob=float(config['alice']['p1']),
                dark_count_rate=float(config['bob']['darkCount']),
                time_bin=float(config['bob']['timeBin']),
                channel_loss_db=float(config['channel']['loss']),
                sync_error_ppm=float(config['channel']['syncError']),
                block_size=int(config['processing']['blockSize']),
                max_offset=int(config['processing']['maxOffset'])
            )
        except (KeyError, ValueError) as e:
            raise ValueError(f"Invalid configuration: {str(e)}")

    def generate_states(self, config: SimulationConfig) -> Tuple[np.ndarray, np.ndarray]:
        """
        Generate Alice's quantum states and intensity array
        
        Args:
            config: Simulation parameters
            
        Returns:
            Tuple of (states array, intensity array)
        """
        # Generate random states based on probabilities
        states = np.random.choice(
            [config.signal_power, config.decoy_power],
            p=[config.signal_prob, 1 - config.signal_prob],
            size=int(config.block_size)
        )
        
        # Create intensity array for cross-correlation
        intensity = (states == config.signal_power).astype(int)
        
        return states, intensity

    def apply_channel_effects(self, 
                            states: np.ndarray,
                            config: SimulationConfig,
                            delay: Optional[int] = None) -> np.ndarray:
        """
        Apply channel loss and add delay
        
        Args:
            states: Input quantum states
            config: Simulation parameters
            delay: Optional fixed delay (for testing)
            
        Returns:
            Modified states after channel effects
        """
        # Convert dB loss to linear
        attenuation = 10 ** (config.channel_loss_db/10)
        
        # Calculate dark count probability per bin
        P_dark = 1 - np.exp(-config.dark_count_rate * config.time_bin * 1E-12)
        
        # Apply loss and add delay
        if delay is None:
            delay = config.max_offset + np.random.randint(0, 1001)
            
        # Add padding for delay
        front_pad = np.random.choice(
            [config.signal_power, config.decoy_power],
            p=[config.signal_prob, 1 - config.signal_prob],
            size=delay
        )
        end_pad = np.random.choice(
            [config.signal_power, config.decoy_power],
            p=[config.signal_prob, 1 - config.signal_prob],
            size=delay
        )
        extended_states = np.concatenate((front_pad, states, end_pad))
        
        # Apply loss and detection probability
        detection_prob = 1 - np.exp(-extended_states * attenuation)
        detection_prob += P_dark  # Add dark counts
        
        # Generate detection events
        detections = np.random.rand(len(detection_prob)) < detection_prob
        
        return detections, delay

    def find_delay(self,
                  intensity: np.ndarray,
                  detections: np.ndarray,
                  config: SimulationConfig,
                  actual_delay: int) -> Tuple[np.ndarray, np.ndarray, int, bool]:
        """
        Find delay using cross-correlation
        
        Args:
            intensity: Alice's intensity array
            detections: Bob's detection events
            config: Simulation parameters
            actual_delay: The actual delay added
            
        Returns:
            Tuple of (time points, cross correlation, found delay, success flag)
        """
        # Calculate cross-correlation
        cross_corr = correlate(intensity, detections, mode='valid', method='fft')
        
        # Find optimal lag
        optimal_lag = np.argmax(cross_corr)
        
        # Generate time points centered around optimal lag
        time_points = np.arange(len(cross_corr)) - len(cross_corr)//2
        
        # Check if found delay matches actual delay within tolerance
        sync_success = abs(optimal_lag - actual_delay) <= abs(config.sync_error_ppm * 1e-6 * config.block_size)
        
        return time_points, cross_corr, optimal_lag, sync_success

    def calculate_statistics(self,
                           detections: np.ndarray,
                           config: SimulationConfig) -> Tuple[int, float, float]:
        """
        Calculate detection statistics
        
        Args:
            detections: Detection events array
            config: Simulation parameters
            
        Returns:
            Tuple of (total counts, mean rate, QBER)
        """
        # Calculate total counts and rate
        total_counts = np.sum(detections)
        duration = len(detections) * config.time_bin * 1E-12  # seconds
        mean_rate = total_counts / duration
        
        # Estimate QBER from dark count contribution
        signal_window = config.time_bin * 1E-12  # seconds
        dark_contribution = config.dark_count_rate * signal_window
        qber = dark_contribution / (total_counts / len(detections))
        
        return total_counts, mean_rate, qber

    def run(self, config_dict: Dict[str, Any]) -> Dict[str, Any]:
        """
        Run complete channel simulation
        
        Args:
            config_dict: Dictionary of simulation parameters
            
        Returns:
            Dictionary containing simulation results
        """
        # Validate configuration
        config = self.validate_config(config_dict)
        
        # Generate Alice's states
        states, intensity = self.generate_states(config)
        
        # Apply channel effects
        detections, actual_delay = self.apply_channel_effects(states, config)
        
        # Find delay using cross-correlation
        time_points, cross_corr, found_delay, sync_success = self.find_delay(
            intensity, detections, config, actual_delay
        )
        
        # Calculate statistics
        total_counts, mean_rate, qber = self.calculate_statistics(detections, config)
        
        # Package results
        results = SimulationResults(
            time_points=time_points,
            cross_correlation=cross_corr,
            counts=detections,
            peak_position=found_delay,
            total_counts=total_counts,
            mean_count_rate=mean_rate,
            qber=qber,
            sync_success=sync_success
        )
        
        # Convert to dictionary for JSON serialization
        return {
            'time_points': results.time_points.tolist(),
            'cross_correlation': results.cross_correlation.tolist(),
            'counts': results.counts.tolist(),
            'peak_position': int(results.peak_position),
            'statistics': {
                'total_counts': results.total_counts,
                'mean_count_rate': results.mean_count_rate,
                'qber': results.qber,
                'sync_success': results.sync_success
            }
        }