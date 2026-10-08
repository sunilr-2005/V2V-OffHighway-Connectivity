"""Simulation environment for two-vehicle off-highway дорожing scenario."""

import math
import time
from typing import Dict, Any

from src.vehicle import Vehicle


class VehicleSimulator:
    """Simple simulator for a blind crossing scenario."""

    def __init__(self, veh_a: Vehicle, veh_b: Vehicle):
        self.veh_a = veh_a
        self.veh_b = veh_b

    def step(self, dt: float = 0.25) -> Dict[str, Any]:
        self.veh_a.update_position(dt)
        self.veh_b.update_position(dt)
        return {
            "veh_a": self.veh_a.get_state(),
            "veh_b": self.veh_b.get_state(),
        }

    def generate_scenario(self) -> None:
        # Vehicle A moves eastward toward crossing
        self.veh_a.x = -60.0
        self.veh_a.y = 0.0
        self.veh_a.heading_deg = 0.0
        self.veh_a.speed_mps = 5.0
        self.veh_a.route = "crossing_east"

        # Vehicle B moves northward toward crossing
        self.veh_b.x = 0.0
        self.veh_b.y = -60.0
        self.veh_b.heading_deg = 90.0
        self.veh_b.speed_mps = 4.2
        self.veh_b.route = "crossing_north"

    def is_crossing_risk(self) -> bool:
        distance = self.veh_a.distance_to(self.veh_b)
        return distance < 45.0
