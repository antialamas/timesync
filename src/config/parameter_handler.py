import yaml
from pathlib import Path
from typing import Dict, Any
import uuid
from datetime import datetime

class ConfigManager:
    """Handles parameter validation and configuration file operations"""
    
    # Parameter constraints and defaults
    PARAMETER_SPECS = {
        'alice': {
            'power': {'type': float, 'min': -100, 'max': 0, 'default': -10},
            'rate': {'type': float, 'min': 0, 'max': 1000, 'default': 100}
        },
        'bob': {
            'efficiency': {'type': float, 'min': 0, 'max': 100, 'default': 50},
            'dark_count': {'type': float, 'min': 0, 'max': 1e6, 'default': 1000}
        },
        'channel': {
            'loss': {'type': float, 'min': 0, 'max': 100, 'default': 10},
            'noise': {'type': float, 'min': 0, 'max': 1e6, 'default': 1000}
        },
        'processing': {
            'window': {'type': float, 'min': 0.1, 'max': 1000, 'default': 1},
            'threshold': {'type': float, 'min': 0, 'max': 1, 'default': 0.5}
        }
    }

    def validate_parameters(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate and normalize simulation parameters
        
        Args:
            params: Dictionary of parameters grouped by category
            
        Returns:
            Validated and normalized parameters with defaults filled in
        
        Raises:
            ValueError: If parameters are invalid
        """
        validated = {}
        
        # Add metadata
        validated['metadata'] = {
            'id': str(uuid.uuid4()),
            'timestamp': datetime.utcnow().isoformat(),
            'version': '1.0'
        }

        # Validate each parameter group
        for group, specs in self.PARAMETER_SPECS.items():
            validated[group] = {}
            group_params = params.get(group, {})
            
            for param_name, constraints in specs.items():
                value = group_params.get(param_name, constraints['default'])
                
                # Type checking
                try:
                    value = constraints['type'](value)
                except (TypeError, ValueError):
                    raise ValueError(
                        f"Invalid type for {group}.{param_name}. "
                        f"Expected {constraints['type'].__name__}"
                    )
                
                # Range checking
                if value < constraints['min'] or value > constraints['max']:
                    raise ValueError(
                        f"Parameter {group}.{param_name} must be between "
                        f"{constraints['min']} and {constraints['max']}"
                    )
                
                validated[group][param_name] = value
        
        return validated

    def load_config(self, file_path: str) -> Dict[str, Any]:
        """
        Load parameters from a YAML configuration file
        
        Args:
            file_path: Path to the configuration file
            
        Returns:
            Dictionary of parameters
            
        Raises:
            FileNotFoundError: If config file doesn't exist
            yaml.YAMLError: If config file is invalid
        """
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"Configuration file not found: {file_path}")
            
        with path.open('r') as f:
            config = yaml.safe_load(f)
            
        # Validate loaded parameters
        return self.validate_parameters(config)

    def save_config(self, config: Dict[str, Any], file_path: str) -> None:
        """
        Save parameters to a YAML configuration file
        
        Args:
            config: Dictionary of parameters to save
            file_path: Path where to save the configuration
        """
        path = Path(file_path)
        path.parent.mkdir(parents=True, exist_ok=True)
            
        with path.open('w') as f:
            yaml.safe_dump(config, f, default_flow_style=False)