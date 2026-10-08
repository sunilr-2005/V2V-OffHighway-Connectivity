# V2V Off-Highway Connectivity Architecture

## 1. Vehicle Layer

Each vehicle maintains its own state:

- vehicle ID
- GPS or simulated position
- speed and direction
- brake and route status
- operating zone or route restriction

## 2. Communication Layer

The communication layer uses UDP to exchange JSON messages between vehicles. This is ideal for a proof-of-concept because it is lightweight, low-cost, and easy to deploy on a local network.

## 3. Risk Layer

The risk engine fuses neighbor telemetry with local vehicle state and determines whether a conflict is likely. It uses:

- distance threshold
- time-to-collision estimate
- crossing angle
- route conflict conditions

## 4. Alert Layer

When risk is high, the vehicle shows an alert and recommended action, for example:

- slow down
- stop before intersection
- yield
- do not enter restricted zone

## 5. Logging and Evaluation

The system logs:

- transmitted messages
- received packets
- delay
- distance and risk values
- alert events

These metrics can be used to evaluate communication performance and safety response.

