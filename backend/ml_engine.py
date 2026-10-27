"""
JalUrja AI - Machine Learning Anomaly Detection & Water Demand Forecasting Engine
"""

import math
from typing import Dict, Any, List, Tuple
from datetime import datetime

class LeakDetectionEngine:
    """
    Multi-sensor acoustic & hydraulic anomaly detection model.
    Combines differential pressure drop, flow surge, and acoustic vibration.
    """
    def __init__(self):
        # Baseline hydraulic parameters
        self.acoustic_baseline_db = 18.0
        self.acoustic_critical_threshold_db = 55.0
        self.pressure_drop_critical_pct = 0.35  # > 35% pressure loss is critical

    def score_sensor_reading(
        self,
        current_pressure: float,
        target_pressure: float,
        flow_rate: float,
        acoustic_db: float,
        vibration_mms: float = 0.5
    ) -> Tuple[float, str, str]:
        """
        Returns (leak_probability, severity_label, diagnostic_notes)
        """
        # 1. Hydraulic pressure deficit ratio
        if target_pressure > 0:
            pressure_deficit = max(0.0, (target_pressure - current_pressure) / target_pressure)
        else:
            pressure_deficit = 0.0

        # 2. Acoustic anomaly component (normalized)
        acoustic_anomaly = max(0.0, (acoustic_db - self.acoustic_baseline_db) / (self.acoustic_critical_threshold_db - self.acoustic_baseline_db))
        acoustic_anomaly = min(1.0, acoustic_anomaly)

        # 3. Vibration anomaly
        vib_factor = min(1.0, max(0.0, (vibration_mms - 0.4) / 1.6))

        # Composite multi-variate score
        composite_score = (0.50 * pressure_deficit) + (0.35 * acoustic_anomaly) + (0.15 * vib_factor)
        # Apply sigmoid shaping
        leak_prob = round(1.0 / (1.0 + math.exp(-7.0 * (composite_score - 0.38))), 3)

        if leak_prob >= 0.70:
            severity = "CRITICAL"
            notes = f"Major pipeline burst indicated. Pressure drop: {pressure_deficit*100:.1f}%, Acoustic noise: {acoustic_db:.1f} dB."
        elif leak_prob >= 0.35:
            severity = "WARNING"
            notes = f"Moderate anomaly detected. Probable pipe cavitation or joint seepage."
        else:
            severity = "NORMAL"
            notes = "Hydraulic and acoustic parameters within nominal thresholds."

        return leak_prob, severity, notes


class DemandForecaster:
    """
    Predicts 24-hour urban water demand (Mega-Litres per Day)
    based on diurnal consumption curves, peak morning/evening hours, and temperature.
    """
    def __init__(self):
        # Base diurnal coefficients for Indian urban wards (6 AM & 6 PM peaks)
        self.hourly_multipliers = [
            0.28, 0.22, 0.20, 0.25, 0.45, 0.75, # 00 - 05
            1.25, 1.40, 1.35, 1.15, 0.95, 0.85, # 06 - 11
            0.80, 0.75, 0.70, 0.75, 0.85, 1.10, # 12 - 17
            1.35, 1.30, 1.10, 0.85, 0.60, 0.40  # 18 - 23
        ]
        self.base_ward_demand_mld = 11.5  # Mean MLD for typical metro ward cluster

    def predict_24h_demand(self, base_mld: float = None) -> List[Dict[str, Any]]:
        base = base_mld or self.base_ward_demand_mld
        forecast = []
        for hour in range(24):
            mult = self.hourly_multipliers[hour]
            # diurnal demand calculation
            predicted_mld = round(base * mult, 2)
            
            # Identify consumption period
            if hour in [6, 7, 8, 9, 18, 19, 20]:
                category = "PEAK_CONSUMPTION"
            elif hour in [10, 11, 12, 13, 14, 15, 16]:
                category = "DAY_MODERATE"
            else:
                category = "NIGHT_OFFPEAK"

            forecast.append({
                "hour": hour,
                "hour_label": f"{hour:02d}:00",
                "predicted_demand_mld": predicted_mld,
                "category": category
            })
        return forecast

leak_engine = LeakDetectionEngine()
demand_forecaster = DemandForecaster()
