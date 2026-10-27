"""
Unit tests for Machine Learning algorithms and Tariff Optimization Logic
"""

import pytest
from backend.ml_engine import LeakDetectionEngine, DemandForecaster
from backend.optimizer import PumpOptimizer

def test_leak_engine_nominal_conditions():
    engine = LeakDetectionEngine()
    prob, severity, notes = engine.score_sensor_reading(
        current_pressure=3.20,
        target_pressure=3.20,
        flow_rate=110.0,
        acoustic_db=17.5,
        vibration_mms=0.4
    )
    assert prob < 0.20
    assert severity == "NORMAL"

def test_leak_engine_critical_burst():
    engine = LeakDetectionEngine()
    # 50% pressure drop with acoustic roar
    prob, severity, notes = engine.score_sensor_reading(
        current_pressure=1.60,
        target_pressure=3.20,
        flow_rate=210.0,
        acoustic_db=68.5,
        vibration_mms=2.2
    )
    assert prob >= 0.70
    assert severity == "CRITICAL"
    assert "burst" in notes.lower()

def test_demand_forecaster_24h_cycle():
    forecaster = DemandForecaster()
    forecast = forecaster.predict_24h_demand(base_mld=10.0)
    assert len(forecast) == 24
    
    # Hour 7 (07:00 AM) and Hour 19 (07:00 PM) must be peak consumption
    assert forecast[7]["category"] == "PEAK_CONSUMPTION"
    assert forecast[19]["category"] == "PEAK_CONSUMPTION"
    
    # Hour 2 (02:00 AM) must be night off-peak
    assert forecast[2]["category"] == "NIGHT_OFFPEAK"
    assert forecast[7]["predicted_demand_mld"] > forecast[2]["predicted_demand_mld"]

def test_pump_optimizer_solar_tariff():
    optimizer = PumpOptimizer()
    # Hour 12 (12 PM) should be SOLAR
    solar_tariff = optimizer.get_tariff_for_hour(12)
    assert solar_tariff["badge"] == "SOLAR"
    assert solar_tariff["rate_inr"] == 4.20

    # Hour 20 (8 PM) should be PEAK
    peak_tariff = optimizer.get_tariff_for_hour(20)
    assert peak_tariff["badge"] == "PEAK"
    assert peak_tariff["rate_inr"] == 8.90

    # Schedule should deliver positive monetary savings
    result = optimizer.generate_optimal_schedule(pump_kw=100.0)
    assert result["summary"]["daily_cost_savings_inr"] > 0
    assert result["summary"]["optimized_daily_cost_inr"] < result["summary"]["baseline_daily_cost_inr"]
