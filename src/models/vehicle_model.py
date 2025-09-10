"""
Electric Vehicle model class.

This module defines the ElectricVehicle class for modeling EV characteristics.
"""

from dataclasses import dataclass
from typing import Optional, Dict, Any
import numpy as np


@dataclass
class VehicleSpecs:
    """Vehicle specifications data class."""
    make: str
    model: str
    year: int
    battery_capacity: float  # kWh
    max_charging_power: float  # kW
    efficiency: float  # kWh/100km or miles/kWh
    weight: float  # kg
    drag_coefficient: float
    frontal_area: float  # m²


class ElectricVehicle:
    """
    Electric Vehicle model for optimization studies.
    
    This class represents an electric vehicle with its key characteristics
    and provides methods for calculating energy consumption, range, etc.
    """
    
    def __init__(self, specs: VehicleSpecs):
        """
        Initialize an Electric Vehicle.
        
        Args:
            specs: VehicleSpecs object containing vehicle specifications
        """
        self.specs = specs
        self.current_soc = 1.0  # Start fully charged
        self.location = (0.0, 0.0)  # (latitude, longitude)
        self.total_distance = 0.0
        
    def calculate_energy_consumption(self, 
                                   distance: float,
                                   speed: float,
                                   elevation_change: float = 0.0,
                                   temperature: float = 20.0) -> float:
        """
        Calculate energy consumption for a given trip.
        
        Args:
            distance: Distance in km
            speed: Average speed in km/h
            elevation_change: Net elevation change in meters
            temperature: Ambient temperature in Celsius
            
        Returns:
            Energy consumption in kWh
        """
        # Base consumption from efficiency rating
        base_consumption = distance * self.specs.efficiency / 100
        
        # Speed factor (consumption increases with speed due to air resistance)
        speed_factor = 1.0 + (speed - 50) * 0.01  # 1% increase per km/h over 50
        speed_factor = max(0.5, speed_factor)  # Minimum 50% of base
        
        # Elevation factor
        elevation_factor = 1.0 + elevation_change * 0.0001  # Rough approximation
        
        # Temperature factor (efficiency decreases in extreme temperatures)
        temp_factor = 1.0 + abs(temperature - 20) * 0.005
        
        total_consumption = base_consumption * speed_factor * elevation_factor * temp_factor
        
        return max(0, total_consumption)
    
    def calculate_range(self, conditions: Dict[str, Any] = None) -> float:
        """
        Calculate remaining range based on current state of charge.
        
        Args:
            conditions: Dictionary of driving conditions
                       (speed, temperature, elevation_change)
            
        Returns:
            Remaining range in km
        """
        if conditions is None:
            conditions = {'speed': 50, 'temperature': 20, 'elevation_change': 0}
        
        # Available energy
        available_energy = self.current_soc * self.specs.battery_capacity
        
        # Calculate consumption per km under given conditions
        consumption_per_km = self.calculate_energy_consumption(
            distance=1.0,
            speed=conditions.get('speed', 50),
            elevation_change=conditions.get('elevation_change', 0),
            temperature=conditions.get('temperature', 20)
        )
        
        return available_energy / consumption_per_km if consumption_per_km > 0 else 0
    
    def update_state_after_trip(self, 
                              distance: float,
                              energy_consumed: float,
                              new_location: tuple = None):
        """
        Update vehicle state after completing a trip.
        
        Args:
            distance: Distance traveled in km
            energy_consumed: Energy consumed in kWh
            new_location: New (latitude, longitude) position
        """
        # Update state of charge
        energy_depleted = energy_consumed / self.specs.battery_capacity
        self.current_soc = max(0, self.current_soc - energy_depleted)
        
        # Update location
        if new_location:
            self.location = new_location
            
        # Update total distance
        self.total_distance += distance
    
    def charge(self, energy_added: float) -> float:
        """
        Charge the vehicle battery.
        
        Args:
            energy_added: Energy to add in kWh
            
        Returns:
            Actual energy added (may be less if battery was nearly full)
        """
        max_energy = (1.0 - self.current_soc) * self.specs.battery_capacity
        actual_energy = min(energy_added, max_energy)
        
        soc_increase = actual_energy / self.specs.battery_capacity
        self.current_soc = min(1.0, self.current_soc + soc_increase)
        
        return actual_energy
    
    def get_status(self) -> Dict[str, Any]:
        """Get current vehicle status."""
        return {
            'make_model': f"{self.specs.make} {self.specs.model}",
            'soc': self.current_soc,
            'remaining_energy': self.current_soc * self.specs.battery_capacity,
            'location': self.location,
            'total_distance': self.total_distance,
            'estimated_range': self.calculate_range()
        }


# Example usage and testing
if __name__ == "__main__":
    # Create a sample vehicle
    tesla_specs = VehicleSpecs(
        make="Tesla",
        model="Model 3",
        year=2023,
        battery_capacity=75.0,  # kWh
        max_charging_power=250.0,  # kW
        efficiency=15.0,  # kWh/100km
        weight=1847,  # kg
        drag_coefficient=0.23,
        frontal_area=2.22  # m²
    )
    
    vehicle = ElectricVehicle(tesla_specs)
    
    # Test energy consumption calculation
    consumption = vehicle.calculate_energy_consumption(
        distance=100,  # 100 km
        speed=80,      # 80 km/h
        temperature=10  # 10°C
    )
    
    print(f"Vehicle: {vehicle.specs.make} {vehicle.specs.model}")
    print(f"Energy consumption for 100km at 80km/h: {consumption:.2f} kWh")
    print(f"Current range: {vehicle.calculate_range():.1f} km")
    print(f"Status: {vehicle.get_status()}")