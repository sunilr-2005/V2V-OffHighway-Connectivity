"""Network communication layer for V2V message exchange."""

import json
import socket
import threading
import time
from typing import Dict, Any


class V2VCommunicationNode:
    """Simple UDP-based V2V communication node for proof-of-concept testing."""

    def __init__(self, vehicle_id: str, port: int, peer_ip: str = "127.0.0.1", peer_port: int = 5002):
        self.vehicle_id = vehicle_id
        self.port = port
        self.peer_ip = peer_ip
        self.peer_port = peer_port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(("0.0.0.0", port))
        self.sock.settimeout(0.2)
        self.neighbors: Dict[str, Dict[str, Any]] = {}
        self.lock = threading.Lock()
        self.running = True
        self.listener_thread = threading.Thread(target=self._listener_loop, daemon=True)
        self.listener_thread.start()

    def send_state(self, message: Dict[str, Any]) -> None:
        payload = json.dumps(message).encode("utf-8")
        self.sock.sendto(payload, (self.peer_ip, self.peer_port))

    def _listener_loop(self) -> None:
        while self.running:
            try:
                data, addr = self.sock.recvfrom(65535)
                if not data:
                    continue
                packet = json.loads(data.decode("utf-8"))
                if packet.get("vehicle_id") == self.vehicle_id:
                    continue
                with self.lock:
                    self.neighbors[packet["vehicle_id"]] = {
                        "data": packet,
                        "addr": addr,
                        "timestamp": time.time(),
                    }
            except socket.timeout:
                continue
            except Exception:
                continue

    def get_neighbors(self) -> Dict[str, Dict[str, Any]]:
        with self.lock:
            return dict(self.neighbors)

    def stop(self) -> None:
        self.running = False
        self.sock.close()
