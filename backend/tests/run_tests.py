"""
Standalone test runner using Python standard library (unittest)
Ensures zero-dependency test verification.
"""

import unittest
from backend.ml_engine import LeakDetectionEngine, DemandForecaster
from backend.optimizer import PumpOptimizer
from backend.database import db

class TestJalUrjaAlgorithms(unittest.TestCase):
    def setUp(self):
        self.leak_engine = LeakDetectionEngine()
        self.forecaster = DemandForecaster()
        self.optimizer = PumpOptimizer()

    def test_nominal_leak_score(self):
        prob, severity, _ = self.leak_engine.score_sensor_reading(3.2, 3.2, 100.0, 16.0, 0.4)
        self.assertLess(prob, 0.25)
        self.assertEqual(severity, "NORMAL")

    def test_critical_burst_detection(self):
        prob, severity, notes = self.leak_engine.score_sensor_reading(1.5, 3.2, 220.0, 72.0, 2.3)
        self.assertGreaterEqual(prob, 0.70)
        self.assertEqual(severity, "CRITICAL")
        self.assertIn("burst", notes.lower())

    def test_demand_forecasting_peaks(self):
        forecast = self.forecaster.predict_24h_demand(11.5)
        self.assertEqual(len(forecast), 24)
        # 7 AM morning peak vs 2 AM night dip
        self.assertGreater(forecast[7]["predicted_demand_mld"], forecast[2]["predicted_demand_mld"])
        self.assertEqual(forecast[7]["category"], "PEAK_CONSUMPTION")

    def test_solar_tariff_savings(self):
        res = self.optimizer.generate_optimal_schedule(pump_kw=120.0)
        summary = res["summary"]
        self.assertGreater(summary["daily_cost_savings_inr"], 0)
        self.assertGreater(summary["percentage_savings"], 15.0)

    def test_database_and_alerts(self):
        alerts = db.get_alerts()
        self.assertGreater(len(alerts), 0)
        open_alerts = [a for a in alerts if a["status"] == "OPEN"]
        if open_alerts:
            aid = open_alerts[0]["id"]
            ok = db.resolve_alert(aid, "Field van dispatched")
            self.assertTrue(ok)

if __name__ == "__main__":
    unittest.main()
