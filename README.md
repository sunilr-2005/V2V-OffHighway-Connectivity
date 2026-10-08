# V2V Off-Highway Connectivity Proof of Concept

This project demonstrates a practical vehicle-to-vehicle (V2V) safety concept for off-highway vehicles operating in constrained environments such as mines, construction sites, quarries, and agricultural fields.

The proof-of-concept focuses on a blind crossing scenario, where two vehicles exchange state information and the system warns drivers or recommends action before a collision can occur.

## Project Goal

Provide a working simulation of two off-highway vehicles that:

- broadcast their current state to each other
- receive and parse neighbor data
- detect a crossing or route-conflict risk
- issue a warning or recommended action
- log communication and alert performance metrics

## Why this is a strong solution

This is a realistic and effective V2V design because it:

- uses vehicle telemetry instead of a single sensor
- handles spatial awareness with position and heading
- supports blind-zone safety conditions
- works with low-cost local communication for a proof-of-concept
- is easy to extend to GPS, RTK, 5G, or DSRC in a real deployment

## Scenario

Two vehicles approach a blind crossing from perpendicular directions:

- Vehicle A moves eastward along a haul road
- Vehicle B moves northward along a connector road
- Both send their state to each other every 200–500 ms
- The risk engine detects collision probability based on distance, heading, and time-to-collision
- A warning is displayed when the risk exceeds a threshold

## Communication Strategy

For the proof-of-concept, the easiest working method is a local UDP broadcast or point-to-point Wi‑Fi communication between vehicles.

Each vehicle sends a JSON message like:

```json
{
  "vehicle_id": "truck_01",
  "timestamp": 1715000000.123,
  "position": {"x": 15.5, "y": 28.2},
  "heading_deg": 90.0,
  "speed_mps": 5.2,
  "brake": false,
  "status": "moving",
  "route": "crossing_east",
  "zone": "haul_road"
}
```

## File Layout

```text
V2V-OffHighway-Connectivity/
├── README.md
├── requirements.txt
├── src/
│   ├── __init__.py
│   ├── communication.py
│   ├── vehicle.py
│   ├── risk_engine.py
│   ├── metrics.py
│   ├── simulator.py
│   ├── dashboard.py
│   └── main.py
├── tests/
│   └── test_risk_engine.py
├── docs/
│   └── architecture.md
└── data/
    └── sample_logs/
```

## Installation

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Run Two Vehicles

Open two terminals and run:

```bash
python src/main.py --vehicle truck_01 --port 5001 --peer-port 5002
```

```bash
python src/main.py --vehicle truck_02 --port 5002 --peer-port 5001
```

This creates two vehicles that share state information over a local network.

## How it connects another vehicle

To connect another vehicle in a real environment:

- assign each vehicle a unique `vehicle_id`
- configure each node with its own port
- set the peer IP/port of the other vehicle
- ensure both are on the same local network or are reachable through the chosen communication network
- enable UDP broadcast or direct socket communication

For example, in a lab or field setup:

```python
peer_ip = "192.168.1.104"
peer_port = 5002
```

Then the sender broadcasts to that peer.

## Warning Logic

The risk engine evaluates:

- vehicle distance
- relative speed
- heading crossing angle
- time-to-collision
- route conflict zone

Example rule:

```python
if distance < 35 and time_to_collision < 5 and angle_diff > 30:
    alert = "Blind crossing risk detected"
```

## Metrics Collected

The POC logs:

- communication range
- packet delay
- message delivery success rate
- position accuracy
- warning accuracy
- response time
- risk alert details

## Output Example

```text
[truck_01] Received message from truck_02 at distance=24.3m, TTC=3.8s, risk=high
[truck_01] Warning: Blind crossing risk detected. Slow down and yield.
```

## Advanced Extension

This can be extended to:

- GPS/RTK localization
- DSRC/802.11p or LTE communication
- restricted-zone geofencing
- queue detection and speed recommendation
- automatic braking advisory logic
- real machine integration on Raspberry Pi or embedded controller

## Summary

This project is a practical V2V off-highway proof-of-concept that demonstrates how two vehicles can cooperate using shared position and movement data to improve safety around blind crossings and route conflicts.

It is low-cost, modular, and suitable for simulation or hardware-based extension.

