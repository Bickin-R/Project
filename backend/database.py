"""
JalUrja AI - Database and Grid State Management
"""

import json
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, List, Any, Optional

DATA_DIR = Path(__file__).parent.parent / "data"

class GridDatabase:
    def __init__(self):
        self.nodes: Dict[str, Dict[str, Any]] = {}
        self.pipelines: List[Dict[str, Any]] = []
        self.telemetry_history: List[Dict[str, Any]] = []
        self.alerts: List[Dict[str, Any]] = []
        self._load_seed_data()

    def _load_seed_data(self):
        topology_file = DATA_DIR / "pipeline_network.json"
        if topology_file.exists():
            with open(topology_file, "r") as f:
                data = json.load(f)
                for node in data.get("nodes", []):
                    self.nodes[node["id"]] = node
                self.pipelines = data.get("pipelines", [])
        
        # Prepopulate initial active alert at NODE-102
        self.alerts.append({
            "id": "ALT-2026-001",
            "node_id": "NODE-102",
            "node_name": "Koramangala 80ft Road Junction B",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "severity": "CRITICAL",
            "leak_probability": 0.93,
            "pressure_bar": 1.72,
            "target_pressure_bar": 3.50,
            "acoustic_noise_db": 68.7,
            "status": "OPEN",
            "assigned_crew": "Field Repair Van #04 (South Zone)",
            "message": "Major pressure drop and elevated acoustic signature detected. Probable cast-iron joint burst."
        })

    def get_all_nodes(self) -> List[Dict[str, Any]]:
        return list(self.nodes.values())

    def get_node(self, node_id: str) -> Optional[Dict[str, Any]]:
        return self.nodes.get(node_id)

    def update_node_telemetry(self, node_id: str, pressure: float, flow: float, acoustic: float, leak_prob: float):
        if node_id in self.nodes:
            self.nodes[node_id]["current_pressure_bar"] = pressure
            self.nodes[node_id]["flow_rate_lps"] = flow
            self.nodes[node_id]["acoustic_noise_db"] = acoustic
            self.nodes[node_id]["leak_probability"] = leak_prob
            if leak_prob >= 0.70:
                self.nodes[node_id]["status"] = "CRITICAL_LEAK"
            elif leak_prob >= 0.40:
                self.nodes[node_id]["status"] = "WARNING"
            else:
                self.nodes[node_id]["status"] = "NORMAL"

    def record_telemetry(self, record: Dict[str, Any]):
        self.telemetry_history.append(record)
        # Keep recent 200 records in memory
        if len(self.telemetry_history) > 200:
            self.telemetry_history.pop(0)

    def get_recent_telemetry(self, limit: int = 50) -> List[Dict[str, Any]]:
        return self.telemetry_history[-limit:]

    def add_alert(self, alert: Dict[str, Any]):
        self.alerts.insert(0, alert)

    def get_alerts(self, status: Optional[str] = None) -> List[Dict[str, Any]]:
        if status:
            return [a for a in self.alerts if a["status"].upper() == status.upper()]
        return self.alerts

    def resolve_alert(self, alert_id: str, notes: str = "Resolved by field crew") -> bool:
        for a in self.alerts:
            if a["id"] == alert_id:
                a["status"] = "RESOLVED"
                a["resolution_notes"] = notes
                a["resolved_at"] = datetime.now(timezone.utc).isoformat()
                # reset node status
                node_id = a.get("node_id")
                if node_id and node_id in self.nodes:
                    self.nodes[node_id]["status"] = "NORMAL"
                    self.nodes[node_id]["leak_probability"] = 0.05
                    self.nodes[node_id]["current_pressure_bar"] = self.nodes[node_id].get("target_pressure_bar", 3.2)
                return True
        return False

# Singleton instance
db = GridDatabase()
