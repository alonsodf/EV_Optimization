"""
Test suite for EV optimization algorithms and models.

This module contains unit tests for the EV optimization project.
Run tests with: pytest tests/
"""

import pytest
import numpy as np
import sys
import os

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from algorithms.battery_optimization import BatteryOptimizer
from models.vehicle_model import ElectricVehicle, VehicleSpecs


class TestBatteryOptimizer:
    """Test cases for BatteryOptimizer class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.optimizer = BatteryOptimizer(battery_capacity=50.0, efficiency=0.95)
    
    def test_initialization(self):
        """Test BatteryOptimizer initialization."""
        assert self.optimizer.battery_capacity == 50.0
        assert self.optimizer.efficiency == 0.95
    
    def test_optimize_charging_schedule(self):
        """Test charging schedule optimization."""
        time_horizon = 24
        energy_demand = [5.0] * time_horizon
        electricity_prices = [0.1] * time_horizon
        
        result = self.optimizer.optimize_charging_schedule(
            time_horizon, energy_demand, electricity_prices
        )
        
        # Check result structure
        assert 'charging_schedule' in result
        assert 'total_cost' in result
        assert 'energy_delivered' in result
        
        # Check result validity
        assert len(result['charging_schedule']) == time_horizon
        assert result['total_cost'] >= 0
        assert result['energy_delivered'] >= 0
    
    def test_state_of_charge_optimization(self):
        """Test SOC optimization."""
        initial_soc = 0.2
        target_soc = 0.8
        time_steps = 10
        
        soc_trajectory = self.optimizer.state_of_charge_optimization(
            initial_soc, target_soc, time_steps
        )
        
        # Check trajectory properties
        assert len(soc_trajectory) == time_steps
        assert soc_trajectory[0] == initial_soc
        assert soc_trajectory[-1] == target_soc
        assert all(0 <= soc <= 1 for soc in soc_trajectory)


class TestElectricVehicle:
    """Test cases for ElectricVehicle class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.specs = VehicleSpecs(
            make="Tesla",
            model="Model 3", 
            year=2023,
            battery_capacity=75.0,
            max_charging_power=250.0,
            efficiency=15.0,
            weight=1847,
            drag_coefficient=0.23,
            frontal_area=2.22
        )
        self.vehicle = ElectricVehicle(self.specs)
    
    def test_initialization(self):
        """Test vehicle initialization."""
        assert self.vehicle.specs.make == "Tesla"
        assert self.vehicle.current_soc == 1.0  # Starts fully charged
        assert self.vehicle.location == (0.0, 0.0)
        assert self.vehicle.total_distance == 0.0
    
    def test_energy_consumption_calculation(self):
        """Test energy consumption calculation."""
        consumption = self.vehicle.calculate_energy_consumption(
            distance=100,  # km
            speed=80,      # km/h
            elevation_change=0,
            temperature=20
        )
        
        assert consumption > 0
        assert isinstance(consumption, float)
    
    def test_range_calculation(self):
        """Test range calculation."""
        range_km = self.vehicle.calculate_range()
        
        assert range_km > 0
        assert isinstance(range_km, float)
        
        # Range should decrease as SOC decreases
        self.vehicle.current_soc = 0.5
        reduced_range = self.vehicle.calculate_range()
        assert reduced_range < range_km
    
    def test_charging(self):
        """Test vehicle charging."""
        # Start with half charge
        self.vehicle.current_soc = 0.5
        initial_energy = self.vehicle.current_soc * self.vehicle.specs.battery_capacity
        
        # Add 20 kWh
        energy_to_add = 20.0
        actual_energy_added = self.vehicle.charge(energy_to_add)
        
        assert actual_energy_added <= energy_to_add
        assert self.vehicle.current_soc > 0.5
        assert self.vehicle.current_soc <= 1.0
    
    def test_trip_update(self):
        """Test state update after trip."""
        initial_soc = self.vehicle.current_soc
        
        # Simulate a trip
        distance = 50  # km
        energy_consumed = 10  # kWh
        new_location = (40.7128, -74.0060)
        
        self.vehicle.update_state_after_trip(distance, energy_consumed, new_location)
        
        # Check updates
        assert self.vehicle.current_soc < initial_soc
        assert self.vehicle.location == new_location
        assert self.vehicle.total_distance == distance
    
    def test_status_report(self):
        """Test vehicle status reporting."""
        status = self.vehicle.get_status()
        
        required_keys = ['make_model', 'soc', 'remaining_energy', 
                        'location', 'total_distance', 'estimated_range']
        
        for key in required_keys:
            assert key in status
        
        assert isinstance(status['soc'], float)
        assert 0 <= status['soc'] <= 1


if __name__ == "__main__":
    # Run tests if script is executed directly
    pytest.main([__file__])