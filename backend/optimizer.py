"""
JalUrja AI - Solar Time-of-Day (ToD) Pump Scheduling Optimizer
"""

from typing import List, Dict, Any

class PumpOptimizer:
    """
    Optimizes municipal booster and raw water intake pumping operations
    aligned with state electricity DISCOM Time-of-Day (ToD) solar tariffs.
    """
    def __init__(self):
        # Time-of-Day Tariffs (₹ per kWh)
        # Solar Hours (10:00 - 16:00): Highly subsidized solar green power
        # Peak Hours (06:00 - 09:00, 18:00 - 22:00): Highest cost peak grid power
        self.tariffs = {
            "SOLAR_OFFPEAK": 4.20,
            "NIGHT_OFFPEAK": 4.80,
            "NORMAL": 6.50,
            "PEAK_GRID": 8.90
        }

    def get_tariff_for_hour(self, hour: int) -> Dict[str, Any]:
        if 10 <= hour < 16:
            return {"rate_inr": self.tariffs["SOLAR_OFFPEAK"], "zone": "Solar Green Hours (Off-Peak)", "badge": "SOLAR"}
        elif 18 <= hour < 22 or 6 <= hour < 9:
            return {"rate_inr": self.tariffs["PEAK_GRID"], "zone": "Evening/Morning Peak Grid", "badge": "PEAK"}
        elif 23 <= hour or hour < 5:
            return {"rate_inr": self.tariffs["NIGHT_OFFPEAK"], "zone": "Night Off-Peak", "badge": "NIGHT"}
        else:
            return {"rate_inr": self.tariffs["NORMAL"], "zone": "Standard Grid Tariff", "badge": "NORMAL"}

    def generate_optimal_schedule(self, pump_kw: float = 120.0, capacity_lps: float = 350.0) -> Dict[str, Any]:
        """
        Computes 24-hour pump schedule:
        Unoptimized baseline vs JalUrja AI Solar-Optimized schedule.
        """
        hourly_schedule = []
        baseline_cost_total = 0.0
        optimized_cost_total = 0.0
        total_kwh_optimized = 0.0

        for hour in range(24):
            tariff_info = self.get_tariff_for_hour(hour)
            rate = tariff_info["rate_inr"]

            # Baseline unoptimized behavior: pumps simply run reactive to consumer demand
            # (running heavily during 6-9 AM and 6-10 PM peak hours!)
            if hour in [6, 7, 8, 18, 19, 20, 21]:
                baseline_status = "RUNNING_100%"
                baseline_kwh = pump_kw * 1.0
            elif 10 <= hour < 16:
                baseline_status = "STANDBY"
                baseline_kwh = 0.0
            else:
                baseline_status = "PARTIAL_50%"
                baseline_kwh = pump_kw * 0.5
            
            baseline_cost = baseline_kwh * rate
            baseline_cost_total += baseline_cost

            # JalUrja AI Optimized strategy:
            # Pre-pump into reservoirs during 10:00 - 16:00 solar hours!
            # Minimize pumping during 18:00 - 22:00 peak hours!
            if 10 <= hour < 16:
                opt_status = "RUNNING_100%_SOLAR"
                opt_kwh = pump_kw * 1.0
                reason = "Maximize low-cost solar electricity (₹4.20/kWh) to pre-fill MBR reservoirs."
            elif 23 <= hour or hour < 4:
                opt_status = "RUNNING_70%_NIGHT"
                opt_kwh = pump_kw * 0.70
                reason = "Night off-peak reservoir replenishment."
            elif hour in [6, 7, 8]:
                opt_status = "MODERATE_40%"
                opt_kwh = pump_kw * 0.40
                reason = "Supply morning peak leveraging pre-filled head storage."
            elif hour in [18, 19, 20, 21]:
                opt_status = "MINIMAL_STANDBY_15%"
                opt_kwh = pump_kw * 0.15
                reason = "Avoid high peak grid charges (₹8.90/kWh); utilize stored solar energy water head."
            else:
                opt_status = "BALANCED_40%"
                opt_kwh = pump_kw * 0.40
                reason = "Maintain continuous minimum residual pressure."

            opt_cost = opt_kwh * rate
            optimized_cost_total += opt_cost
            total_kwh_optimized += opt_kwh

            hourly_schedule.append({
                "hour": hour,
                "hour_label": f"{hour:02d}:00",
                "tariff_rate_inr": rate,
                "tariff_zone": tariff_info["zone"],
                "badge": tariff_info["badge"],
                "baseline_status": baseline_status,
                "baseline_kwh": round(baseline_kwh, 1),
                "baseline_cost_inr": round(baseline_cost, 2),
                "optimized_status": opt_status,
                "optimized_kwh": round(opt_kwh, 1),
                "optimized_cost_inr": round(opt_cost, 2),
                "hourly_savings_inr": round(baseline_cost - opt_cost, 2),
                "dispatch_rationale": reason
            })

        daily_savings = round(baseline_cost_total - optimized_cost_total, 2)
        pct_savings = round((daily_savings / baseline_cost_total) * 100, 1) if baseline_cost_total > 0 else 0.0

        return {
            "summary": {
                "pump_rated_kw": pump_kw,
                "baseline_daily_cost_inr": round(baseline_cost_total, 2),
                "optimized_daily_cost_inr": round(optimized_cost_total, 2),
                "daily_cost_savings_inr": daily_savings,
                "percentage_savings": pct_savings,
                "total_kwh_consumed": round(total_kwh_optimized, 1),
                "solar_hours_utilization_pct": 100.0,
                "co2_emissions_averted_kg_daily": round(daily_savings * 0.82, 1) # ~0.82 kg CO2 per avoided peak kWh
            },
            "hourly_schedule": hourly_schedule
        }

pump_optimizer = PumpOptimizer()
