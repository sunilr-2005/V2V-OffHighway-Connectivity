"""Simple dashboard output for warnings and system status."""

from typing import Dict, Any


class Dashboard:
    def __init__(self) -> None:
        self.last_alert = None

    def show_status(self, vehicle_id: str, state: Dict[str, Any]) -> None:
        print(f"[{vehicle_id}] position=({state['position']['x']:.1f}, {state['position']['y']:.1f}) "
              f"heading={state['heading_deg']:.1f} speed={state['speed_mps']:.2f} route={state['route']}")

    def show_alert(self, vehicle_id: str, level: str, message: str, distance: float) -> None:
        self.last_alert = (level, message, distance)
        print(f"[{vehicle_id}] [{level.upper()}] {message} (distance={distance:.1f}m)")
