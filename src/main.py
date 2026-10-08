"""Main entry point for the V2V off-highway proof-of-concept."""

import argparse
import json
import time
import socket

from src.communication import V2VCommunicationNode
from src.metrics import MetricsLogger
from src.risk_engine import RiskEngine
from src.vehicle import Vehicle
from src.simulator import VehicleSimulator
from src.dashboard import Dashboard


def build_vehicle(vehicle_id: str, port: int, peer_ip: str, peer_port: int) -> Vehicle:
    return Vehicle(
        vehicle_id=vehicle_id,
        x=-60.0 if vehicle_id == "truck_01" else 0.0,
        y=0.0 if vehicle_id == "truck_01" else -60.0,
        heading_deg=0.0 if vehicle_id == "truck_01" else 90.0,
        speed_mps=5.0 if vehicle_id == "truck_01" else 4.2,
        route="crossing_east" if vehicle_id == "truck_01" else "crossing_north",
        zone="haul_road",
        port=port,
        peer_ip=peer_ip,
        peer_port=peer_port,
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Two-vehicle off-highway V2V demo")
    parser.add_argument("--vehicle", default="truck_01", choices=["truck_01", "truck_02"])
    parser.add_argument("--port", type=int, default=5001)
    parser.add_argument("--peer-port", type=int, default=5002)
    parser.add_argument("--peer-ip", default="127.0.0.1")
    args = parser.parse_args()

    vehicle = build_vehicle(args.vehicle, args.port, args.peer_ip, args.peer_port)
    node = V2VCommunicationNode(vehicle.vehicle_id, vehicle.port, vehicle.peer_ip, vehicle.peer_port)
    risk_engine = RiskEngine()
    metrics = MetricsLogger()
    dashboard = Dashboard()

    print(f"[{vehicle.vehicle_id}] V2V node started on port {args.port}")

    last_send = 0.0
    while True:
        now = time.time()
        if now - last_send >= 0.5:
            state = vehicle.get_state()
            node.send_state(state)
            metrics.record_sent()
            last_send = now

        for neighbor_id, neighbor in node.get_neighbors().items():
            data = neighbor["data"]
            if "position" not in data:
                continue
            delay = time.time() - neighbor["timestamp"]
            metrics.record_received(delay)

            level, message, distance = risk_engine.evaluate(state, data)
            if level != "safe":
                metrics.add_alert(vehicle.vehicle_id, level, message, distance)
                dashboard.show_alert(vehicle.vehicle_id, level, message, distance)
            else:
                dashboard.show_status(vehicle.vehicle_id, state)

        time.sleep(0.2)


if __name__ == "__main__":
    main()
