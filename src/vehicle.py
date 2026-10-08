"""Vehicle model and state representation."""

from dataclasses import dataclass, field
from typing import Dict, List, Optional
import math
import time


@dataclass
class Vehicle:
    """Represents one vehicle state and motion information."""

    vehicle_id: str
    x: float = 0.0
    y: float = 0.0
    heading_deg: float = 0.0
    speed_mps: float = 0.0
    brake: bool = False
    status: str = "moving"
    route: str = "straight"
    zone: str = "haul_road"
    port: int = 5001
    peer_ip: str = "127.0.0.1"
    peer_port: int = 5002
    last_update: float = field(default_factory=time.time)
    history: List[Dict[str, float]] = field(default_factory=list)

    def get_state(self) -> Dict[str, object]:
        return {
            "vehicle_id": self.vehicle_id,
            "timestamp": time.time(),
            "position": {"x": self.x, "y": self.y},
            "heading_deg": self.heading_deg,
            "speed_mps": self.speed_mps,
            "brake": self.brake,
            "status": self.status,
            "route": self.route,
            "zone": self.zone,
            "port": self.port,
        }

    def update_position(self, dt: float) -> None:
        rad = math.radians(self.heading_deg)
        dx = math.cos(rad) * self.speed_mps * dt
        dy = math.sin(rad) * self.speed_mps * dt
        self.x += dx
        self.y += dy
        self.last_update = time.time()
        self.history.append({"time": self.last_update, "x": self.x, "y": self.y})

    def distance_to(self, other: "Vehicle") -> float:
        return math.hypot(self.x - other.x, self.y - other.y)

    def relative_heading_to(self, other: "Vehicle") -> float:
        angle = abs(self.heading_deg - other.heading_deg) % 360
        return min(angle, 360 - angle)

    def set_route(self, route: str) -> None:
        self.route = route

    def set_zone(self, zone: str) -> None:
        self.zone = zone
