"""Risk engine for conflict and blind-crossing detection."""

import math
from typing import Dict, Any, List, Tuple


class RiskEngine:
    """Calculates risk using distance, speed, heading, and route information."""

    def __init__(self, collision_distance: float = 35.0, ttc_threshold: float = 5.0):
        self.collision_distance = collision_distance
        self.ttc_threshold = ttc_threshold

    def _heading_difference(self, heading_a: float, heading_b: float) -> float:
        angle = abs(heading_a - heading_b) % 360
        return min(angle, 360 - angle)

    def _time_to_collision(self, pos_a: Dict[str, float], pos_b: Dict[str, float], speed_a: float, speed_b: float) -> float:
        dx = pos_b["x"] - pos_a["x"]
        dy = pos_b["y"] - pos_a["y"]
        distance = math.hypot(dx, dy)
        if distance <= 0:
            return 0.0
        relative_speed = abs(speed_a - speed_b)
        if relative_speed <= 0:
            return float("inf")
        return distance / relative_speed

    def evaluate(self, local_state: Dict[str, Any], neighbor_state: Dict[str, Any]) -> Tuple[str, str, float]:
        pos_a = local_state["position"]
        pos_b = neighbor_state["position"]

        dx = pos_b["x"] - pos_a["x"]
        dy = pos_b["y"] - pos_a["y"]
        distance = math.hypot(dx, dy)

        heading_diff = self._heading_difference(
            float(local_state.get("heading_deg", 0.0)),
            float(neighbor_state.get("heading_deg", 0.0)),
        )

        local_speed = float(local_state.get("speed_mps", 0.0))
        neighbor_speed = float(neighbor_state.get("speed_mps", 0.0))
        ttc = self._time_to_collision(pos_a, pos_b, local_speed, neighbor_speed)

        if distance < self.collision_distance and ttc < self.ttc_threshold and heading_diff > 30:
            return "high", "Blind crossing risk detected. Slow down and yield.", distance

        if distance < self.collision_distance * 1.5 and heading_diff > 20:
            return "medium", "Vehicle approaching at crossing angle. Maintain caution.", distance

        if distance < self.collision_distance * 2.0 and local_speed > 2.0:
            return "low", "Potential route conflict detected.", distance

        return "safe", "No immediate risk.", distance

    def evaluate_zone(self, local_state: Dict[str, Any], neighbor_state: Dict[str, Any]) -> bool:
        if local_state.get("zone") == neighbor_state.get("zone"):
            return False
        return True
