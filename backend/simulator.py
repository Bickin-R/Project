"""
JalUrja AI - IoT Telemetry Stream Simulator
"""

import random
from datetime import datetime, timezone
from typing import Dict, Any
from .database import db
from .ml_engine import leak_engine

class IoTSimulator:
    """
    Simulates real-world acoustic, pressure, and flow sensors
    deployed across urban water networks.
    """
    def __init__(self):
        self.running = False

    def generate_reading_for_node(self, node: Dict[str, Any]) -> Dict[str, Any]:
        node_id = node["id"]
        target_p = node.get("target_pressure_bar", 3.2)
        base_flow = node.get("flow_capacity_lps", 120.0)

        # If it's already a known burst node (like NODE-102)
        if node.get("status") == "CRITICAL_LEAK":
            p = round(target_p * random.uniform(0.45, 0.55), 2)
            f = round(base_flow * random.uniform(1.3, 1.6), 1)
            ac = round(random.uniform(64.0, 75.0), 1)
            vib = round(random.uniform(1.8, 2.6), 2)
        elif node.get("status") == "WARNING":
            p = round(target_p * random.uniform(0.70, 0.85), 2)
            f = round(base_flow * random.uniform(1.1, 1.25), 1)
            ac = round(random.uniform(38.0, 48.0), 1)
            vib = round(random.uniform(0.8, 1.3), 2)
        else:
            # Nominal variation
            p = round(target_p + random.uniform(-0.15, 0.15), 2)
            f = round(base_flow * random.uniform(0.85, 1.15), 1)
            ac = round(random.uniform(14.0, 22.0), 1)
            vib = round(random.uniform(0.3, 0.6), 2)

        prob, severity, notes = leak_engine.score_sensor_reading(
            current_pressure=p,
            target_pressure=target_p,
            flow_rate=f,
            acoustic_db=ac,
            vibration_mms=vib
        )

        record = {
            "node_id": node_id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "pressure_bar": p,
            "flow_rate_lps": f,
            "acoustic_noise_db": ac,
            "vibration_mms": vib,
            "leak_probability": prob,
            "severity": severity,
            "diagnostic_notes": notes
        }

        # Update node in database
        db.update_node_telemetry(node_id, p, f, ac, prob)
        db.record_telemetry(record)
        return record

    def simulate_burst_event(self, node_id: str) -> Dict[str, Any]:
        """
        Operator action to simulate a sudden water main rupture for live demonstration.
        """
        node = db.get_node(node_id)
        if not node:
            return {"error": f"Node {node_id} not found"}

        node["status"] = "CRITICAL_LEAK"
        reading = self.generate_reading_for_node(node)

        alert_id = f"ALT-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        alert = {
            "id": alert_id,
            "node_id": node_id,
            "node_name": node.get("name", node_id),
            "timestamp": reading["timestamp"],
            "severity": "CRITICAL",
            "leak_probability": reading["leak_probability"],
            "pressure_bar": reading["pressure_bar"],
            "target_pressure_bar": node.get("target_pressure_bar", 3.2),
            "acoustic_noise_db": reading["acoustic_noise_db"],
            "status": "OPEN",
            "assigned_crew": "Emergency Rapid Response Unit",
            "message": f"SIMULATED BURST: Sudden catastrophic drop to {reading['pressure_bar']} bar with {reading['acoustic_noise_db']} dB acoustic roar."
        }
        db.add_alert(alert)
        return {"status": "SUCCESS", "alert": alert, "reading": reading}

simulator = IoTSimulator()
