"""Metrics logger for evaluating communication and alert performance."""

from dataclasses import dataclass, field
from typing import List, Dict, Any
import time


@dataclass
class MetricsLogger:
    sent_count: int = 0
    received_count: int = 0
    alerts: List[Dict[str, Any]] = field(default_factory=list)
    delays: List[float] = field(default_factory=list)

    def record_sent(self) -> None:
        self.sent_count += 1

    def record_received(self, delay: float) -> None:
        self.received_count += 1
        self.delays.append(delay)

    def add_alert(self, vehicle_id: str, level: str, message: str, distance: float) -> None:
        self.alerts.append({
            "vehicle_id": vehicle_id,
            "level": level,
            "message": message,
            "distance": distance,
            "timestamp": time.time(),
        })

    def summary(self) -> Dict[str, Any]:
        avg_delay = sum(self.delays) / len(self.delays) if self.delays else 0.0
        return {
            "sent_count": self.sent_count,
            "received_count": self.received_count,
            "avg_delay_sec": round(avg_delay, 4),
            "alert_count": len(self.alerts),
            "alerts": self.alerts,
        }
