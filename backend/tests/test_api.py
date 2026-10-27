"""
Unit & Integration Tests for JalUrja AI Backend APIs
"""

import pytest
from fastapi.testclient import TestClient
from backend.main import app
from backend.database import db

@pytest.fixture
def client():
    return TestClient(app)

def test_dashboard_endpoint(client):
    """Verify that root URL serves the interactive HTML dashboard."""
    response = client.get("/")
    assert response.status_code == 200
    assert "JalUrja AI" in response.text
    assert "grid-map" in response.text

def test_api_overview(client):
    """Verify system overview and KPI metrics."""
    response = client.get("/api/overview")
    assert response.status_code == 200
    data = response.json()
    assert "kpi_metrics" in data
    assert data["grid_status"] == "OPERATIONAL"
    assert "current_nrw_loss_pct" in data["kpi_metrics"]
    assert data["kpi_metrics"]["daily_power_savings_inr"] > 0

def test_api_nodes(client):
    """Verify network topology returns nodes and pipelines."""
    response = client.get("/api/nodes")
    assert response.status_code == 200
    data = response.json()
    assert "nodes" in data
    assert len(data["nodes"]) >= 5
    # Check that at least one pump and reservoir exist
    node_types = [n["type"] for n in data["nodes"]]
    assert "reservoir" in node_types
    assert "pump_station" in node_types
    assert "sensor_junction" in node_types

def test_api_alerts_and_resolve(client):
    """Verify retrieving and resolving leak alerts."""
    # Fetch alerts
    response = client.get("/api/alerts")
    assert response.status_code == 200
    alerts = response.json().get("alerts", [])
    assert len(alerts) > 0
    
    first_alert = alerts[0]
    alert_id = first_alert["id"]

    # Resolve alert
    resolve_resp = client.post(f"/api/alerts/{alert_id}/resolve")
    assert resolve_resp.status_code == 200
    assert resolve_resp.json()["status"] == "SUCCESS"

    # Confirm resolved state
    alerts_after = client.get("/api/alerts").json().get("alerts", [])
    matching = [a for a in alerts_after if a["id"] == alert_id]
    assert matching[0]["status"] == "RESOLVED"

def test_telemetry_ingest(client):
    """Verify IoT sensor ingestion and dynamic anomaly scoring."""
    payload = {
        "node_id": "NODE-101",
        "pressure_bar": 1.5, # low pressure drop
        "flow_rate_lps": 195.0,
        "acoustic_noise_db": 62.0, # elevated acoustic
        "vibration_mms": 1.5
    }
    response = client.post("/api/telemetry", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "RECORDED"
    assert data["leak_probability"] > 0.50
    assert data["severity"] in ["WARNING", "CRITICAL"]

def test_demand_forecast(client):
    """Verify 24-hour demand forecasting endpoint."""
    response = client.get("/api/demand/forecast")
    assert response.status_code == 200
    data = response.json()
    forecast = data.get("forecast", [])
    assert len(forecast) == 24
    # Morning peak hour 7 should be higher than night hour 2
    assert forecast[7]["predicted_demand_mld"] > forecast[2]["predicted_demand_mld"]

def test_pump_optimizer_schedule(client):
    """Verify solar Time-of-Day pump schedule optimizer."""
    response = client.get("/api/optimizer/pumps/schedule?pump_kw=120.0")
    assert response.status_code == 200
    data = response.json()
    summary = data.get("summary", {})
    assert summary["daily_cost_savings_inr"] > 0
    assert summary["percentage_savings"] > 15.0 # At least 15% savings
    assert len(data.get("hourly_schedule", [])) == 24
