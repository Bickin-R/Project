"""
JalUrja AI - Municipal Water & Energy Command Center API
FastAPI Application Entrypoint
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from pathlib import Path

from .database import db
from .ml_engine import leak_engine, demand_forecaster
from .optimizer import pump_optimizer
from .simulator import simulator

app = FastAPI(
    title="JalUrja AI API",
    description="IoT & Machine Learning Water Grid Optimization and Leak Detection for Indian Cities",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TelemetryInput(BaseModel):
    node_id: str
    pressure_bar: float
    flow_rate_lps: float
    acoustic_noise_db: float
    vibration_mms: Optional[float] = 0.5

class BurstTriggerInput(BaseModel):
    node_id: str

@app.get("/api/overview")
def get_overview():
    nodes = db.get_all_nodes()
    active_alerts = db.get_alerts(status="OPEN")
    critical_count = sum(1 for a in active_alerts if a["severity"] == "CRITICAL")
    warning_count = sum(1 for a in active_alerts if a["severity"] == "WARNING")
    
    total_flow = sum(n.get("current_flow_lps", n.get("flow_rate_lps", 0)) for n in nodes)
    optimizer_data = pump_optimizer.generate_optimal_schedule(pump_kw=120.0)

    return {
        "city": "Bengaluru (South Zone - Koramangala & HSR)",
        "grid_status": "OPERATIONAL",
        "kpi_metrics": {
            "current_nrw_loss_pct": 18.2,
            "baseline_nrw_loss_pct": 39.5,
            "nrw_reduction_pct": 34.8,
            "daily_power_savings_inr": optimizer_data["summary"]["daily_cost_savings_inr"],
            "energy_reduction_pct": optimizer_data["summary"]["percentage_savings"],
            "active_alerts_total": len(active_alerts),
            "critical_bursts": critical_count,
            "warning_seepages": warning_count,
            "total_grid_flow_lps": round(total_flow, 1),
            "co2_averted_kg_daily": optimizer_data["summary"]["co2_emissions_averted_kg_daily"]
        }
    }

@app.get("/api/nodes")
def get_nodes():
    return {
        "nodes": db.get_all_nodes(),
        "pipelines": db.pipelines
    }

@app.get("/api/alerts")
def get_alerts(status: Optional[str] = None):
    return {"alerts": db.get_alerts(status=status)}

@app.post("/api/alerts/{alert_id}/resolve")
def resolve_alert(alert_id: str):
    success = db.resolve_alert(alert_id)
    if not success:
        raise HTTPException(status_code=404, detail="Alert not found")
    return {"status": "SUCCESS", "message": f"Alert {alert_id} marked as resolved. Node restored to nominal state."}

@app.post("/api/telemetry")
def ingest_telemetry(data: TelemetryInput):
    node = db.get_node(data.node_id)
    target_p = node.get("target_pressure_bar", 3.2) if node else 3.2

    prob, severity, notes = leak_engine.score_sensor_reading(
        current_pressure=data.pressure_bar,
        target_pressure=target_p,
        flow_rate=data.flow_rate_lps,
        acoustic_db=data.acoustic_noise_db,
        vibration_mms=data.vibration_mms or 0.5
    )

    db.update_node_telemetry(data.node_id, data.pressure_bar, data.flow_rate_lps, data.acoustic_noise_db, prob)
    return {
        "status": "RECORDED",
        "node_id": data.node_id,
        "leak_probability": prob,
        "severity": severity,
        "diagnostic_notes": notes
    }

@app.post("/api/telemetry/simulate-step")
def simulate_step():
    nodes = db.get_all_nodes()
    results = []
    for node in nodes:
        if node["type"] == "sensor_junction":
            reading = simulator.generate_reading_for_node(node)
            results.append(reading)
    return {"status": "STEP_COMPLETE", "readings_generated": len(results), "readings": results}

@app.post("/api/telemetry/burst")
def trigger_burst(payload: BurstTriggerInput):
    result = simulator.simulate_burst_event(payload.node_id)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

@app.get("/api/optimizer/pumps/schedule")
def get_pump_schedule(pump_kw: float = 120.0):
    return pump_optimizer.generate_optimal_schedule(pump_kw=pump_kw)

@app.get("/api/demand/forecast")
def get_demand_forecast(base_mld: float = 11.5):
    return {
        "forecast": demand_forecaster.predict_24h_demand(base_mld=base_mld),
        "base_mld": base_mld,
        "zone": "Koramangala-HSR Ward Cluster"
    }

# Interactive Web Dashboard served directly on root URL
@app.get("/", response_class=HTMLResponse)
def serve_dashboard():
    dashboard_html_path = Path(__file__).parent / "static" / "dashboard.html"
    if dashboard_html_path.exists():
        with open(dashboard_html_path, "r", encoding="utf-8") as f:
            return f.read()
    return "<h1>JalUrja AI Dashboard file not found</h1>"
