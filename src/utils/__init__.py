"""
Utility functions for EV optimization.

This module contains common utility functions used across the project.
"""

import numpy as np
import pandas as pd
from typing import List, Dict, Any, Tuple
import json
import yaml


def load_config(config_path: str) -> Dict[str, Any]:
    """
    Load configuration from YAML or JSON file.
    
    Args:
        config_path: Path to configuration file
        
    Returns:
        Configuration dictionary
    """
    with open(config_path, 'r') as f:
        if config_path.endswith('.yaml') or config_path.endswith('.yml'):
            return yaml.safe_load(f)
        elif config_path.endswith('.json'):
            return json.load(f)
        else:
            raise ValueError("Config file must be .yaml, .yml, or .json")


def save_results(results: Dict[str, Any], output_path: str):
    """
    Save results to file.
    
    Args:
        results: Results dictionary
        output_path: Path to save results
    """
    if output_path.endswith('.json'):
        with open(output_path, 'w') as f:
            json.dump(results, f, indent=2, default=str)
    elif output_path.endswith('.yaml') or output_path.endswith('.yml'):
        with open(output_path, 'w') as f:
            yaml.dump(results, f, default_flow_style=False)
    else:
        raise ValueError("Output file must be .json, .yaml, or .yml")


def calculate_distance(point1: Tuple[float, float], 
                      point2: Tuple[float, float]) -> float:
    """
    Calculate Haversine distance between two geographic points.
    
    Args:
        point1: (latitude, longitude) of first point
        point2: (latitude, longitude) of second point
        
    Returns:
        Distance in kilometers
    """
    lat1, lon1 = np.radians(point1[0]), np.radians(point1[1])
    lat2, lon2 = np.radians(point2[0]), np.radians(point2[1])
    
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    
    a = np.sin(dlat/2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2)**2
    c = 2 * np.arcsin(np.sqrt(a))
    
    # Earth's radius in kilometers
    r = 6371
    
    return r * c


def normalize_data(data: np.ndarray, method: str = 'minmax') -> np.ndarray:
    """
    Normalize data using specified method.
    
    Args:
        data: Input data array
        method: Normalization method ('minmax', 'zscore', 'robust')
        
    Returns:
        Normalized data
    """
    if method == 'minmax':
        return (data - np.min(data)) / (np.max(data) - np.min(data))
    elif method == 'zscore':
        return (data - np.mean(data)) / np.std(data)
    elif method == 'robust':
        median = np.median(data)
        mad = np.median(np.abs(data - median))
        return (data - median) / mad
    else:
        raise ValueError("Method must be 'minmax', 'zscore', or 'robust'")


def create_time_series(start_time: str, 
                      end_time: str, 
                      frequency: str = 'H') -> pd.DatetimeIndex:
    """
    Create a time series index.
    
    Args:
        start_time: Start time (e.g., '2023-01-01 00:00:00')
        end_time: End time (e.g., '2023-01-31 23:00:00')
        frequency: Frequency ('H' for hourly, 'D' for daily, etc.)
        
    Returns:
        DatetimeIndex
    """
    return pd.date_range(start=start_time, end=end_time, freq=frequency)


def validate_parameters(params: Dict[str, Any], 
                       required_keys: List[str],
                       numeric_keys: List[str] = None) -> bool:
    """
    Validate parameter dictionary.
    
    Args:
        params: Parameters to validate
        required_keys: List of required parameter names
        numeric_keys: List of parameters that must be numeric
        
    Returns:
        True if valid, raises ValueError if not
    """
    # Check required keys
    missing_keys = [key for key in required_keys if key not in params]
    if missing_keys:
        raise ValueError(f"Missing required parameters: {missing_keys}")
    
    # Check numeric keys
    if numeric_keys:
        for key in numeric_keys:
            if key in params and not isinstance(params[key], (int, float)):
                raise ValueError(f"Parameter '{key}' must be numeric")
    
    return True


def format_time_duration(seconds: float) -> str:
    """
    Format time duration in human-readable format.
    
    Args:
        seconds: Duration in seconds
        
    Returns:
        Formatted string (e.g., "2h 30m 15s")
    """
    if seconds < 60:
        return f"{seconds:.1f}s"
    elif seconds < 3600:
        minutes = seconds // 60
        remaining_seconds = seconds % 60
        return f"{int(minutes)}m {remaining_seconds:.0f}s"
    else:
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        remaining_seconds = seconds % 60
        return f"{int(hours)}h {int(minutes)}m {remaining_seconds:.0f}s"


class ProgressTracker:
    """Simple progress tracker for long-running optimizations."""
    
    def __init__(self, total_iterations: int):
        self.total_iterations = total_iterations
        self.current_iteration = 0
        self.start_time = None
        
    def start(self):
        """Start tracking progress."""
        import time
        self.start_time = time.time()
        
    def update(self, iteration: int = None):
        """Update progress."""
        if iteration is not None:
            self.current_iteration = iteration
        else:
            self.current_iteration += 1
            
    def get_progress(self) -> Dict[str, Any]:
        """Get current progress information."""
        import time
        if self.start_time is None:
            return {"error": "Progress tracking not started"}
            
        progress_ratio = self.current_iteration / self.total_iterations
        elapsed_time = time.time() - self.start_time
        
        if progress_ratio > 0:
            estimated_total_time = elapsed_time / progress_ratio
            remaining_time = estimated_total_time - elapsed_time
        else:
            estimated_total_time = 0
            remaining_time = 0
            
        return {
            "iteration": self.current_iteration,
            "total_iterations": self.total_iterations,
            "progress_percent": progress_ratio * 100,
            "elapsed_time": format_time_duration(elapsed_time),
            "estimated_remaining": format_time_duration(remaining_time)
        }


# Example usage
if __name__ == "__main__":
    # Test distance calculation
    point1 = (40.7128, -74.0060)  # New York
    point2 = (34.0522, -118.2437)  # Los Angeles
    distance = calculate_distance(point1, point2)
    print(f"Distance from NYC to LA: {distance:.2f} km")
    
    # Test normalization
    data = np.array([1, 5, 10, 15, 20])
    normalized = normalize_data(data, 'minmax')
    print(f"Original data: {data}")
    print(f"Normalized data: {normalized}")
    
    # Test progress tracker
    tracker = ProgressTracker(100)
    tracker.start()
    tracker.update(25)
    progress = tracker.get_progress()
    print(f"Progress: {progress}")