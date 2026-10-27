# JalUrja AI: User Experience, Wireframes & Design Documentation

## 1. Design Philosophy
JalUrja AI is designed for municipal water engineers, control room operators, and civic decision-makers in Indian cities. The user interface prioritizes:
1. **Urgency-Driven Hierarchy:** Critical pipeline bursts and dangerous pressure surges are elevated to the top of the operator’s visual field with high-contrast color indicators (Crimson Red for bursts, Amber for warnings, Emerald Green for nominal).
2. **Actionable Spatial Intelligence:** Direct integration of interactive GIS maps with node-level sensor telemetry.
3. **One-Click Dispatch:** Instant conversion of an algorithmic alert into a maintenance work order sent to field repair vans.

---

## 2. Key User Personas & Journeys

### Persona A: Municipal Water Distribution Engineer (Ward Level)
* **Goal:** Monitor ward pipeline integrity, respond immediately to bursts, minimize Non-Revenue Water (NRW).
* **Journey:**
  1. Opens JalUrja AI Dashboard on control room tablet or monitor.
  2. Scans KPI summary cards: Current Grid Flow (L/s), Average Network Pressure (Bar), Water Loss Index (NRW %).
  3. Receives live alert popup: *Node-102 (Koramangala 80ft Rd) pressure drop detected*.
  4. Inspects time-series pressure vs acoustic curve; confirms acoustic signature is indicative of cast-iron joint shearing.
  5. Clicks *"Acknowledge & Dispatch Field Crew"*.

### Persona B: Municipal Energy Manager & Pumping Station Superintendent
* **Goal:** Curtail heavy grid power bills and leverage state solar Time-of-Day (ToD) subsidies.
* **Journey:**
  1. Navigates to *Pump Scheduling & Energy Optimizer*.
  2. Reviews projected 24-hour ward water demand curve vs DISCOM power tariff schedule.
  3. Inspects automated dispatch recommendations: Shift PUMP-01 to maximum flow during 10:00 AM - 4:00 PM solar window.
  4. Toggles *"Auto-Schedule Activation"*.

---

## 3. High-Fidelity UI Layout Wireframe

```
+-----------------------------------------------------------------------------------------+
| [JalUrja AI Logo]  JalUrja AI - Municipal Water & Energy Command Center    [Live Status] |
| City: Bengaluru (South Zone) | Active Nodes: 8 | Pumping Stations: 2 | Alerts: 1 Critical|
+-----------------------------------------------------------------------------------------+
|  [Daily NRW Loss]       [Total Pumping Power]    [Active Leak Alerts]   [Est. Daily Savings]|
|      18.4% (-34%)          1,480 kWh (-22%)           1 Critical             ₹18,450 / day  |
+----------------------------------------------------+------------------------------------+
|  INTERACTIVE WARD PIPELINE MAP (GIS/LEAFLET)       |  ACTIVE LEAK & ANOMALY ALERTS      |
|                                                    |                                    |
|   [MBR Reservoir]                                  |  [CRITICAL BURST]                  |
|          |                                         |  Node-102: Koramangala 80ft Rd     |
|     (PUMP-01: 312 L/s)                             |  Pressure: 1.72 Bar (Drop 51%)     |
|          |                                         |  Acoustic: 68.7 dB (Elevated)      |
|    [Node-101]                                      |  Leak Probability: 93%             |
|          \                                         |  Action: [Dispatch Van] [Isolate]  |
|      [Node-102] <-- [CRITICAL RED BLINK]           +------------------------------------+
|          /                                         |  PUMP SCHEDULING (ENERGY OPTIMIZER)|
|    [Node-105]                                      |                                    |
|                                                    |  PUMP-01 (120 kW):                 |
|                                                    |  Current: 10:00 - 16:00 (Solar)    |
|                                                    |  Status: RUNNING @ 312 L/s         |
|                                                    |  Tariff: ₹4.20 / kWh (Savings: ₹4K)|
+----------------------------------------------------+------------------------------------+
|  REAL-TIME TELEMETRY STREAM & DEMAND FORECAST                                           |
|  [24-Hour Demand Forecast vs Actual Consumption Graph]                                  |
|  [Multi-Sensor Pressure & Flow Rate Time-Series Chart]                                  |
+-----------------------------------------------------------------------------------------+
```

---

## 4. UI Color Palette & Accessibility Standards
- **Primary Brand / Water Tone:** `#0284c7` (Sky-600) & `#0369a1` (Sky-700)
- **Energy / Solar Accent:** `#f59e0b` (Amber-500) & `#d97706` (Amber-600)
- **Critical Burst Alert:** `#ef4444` (Red-500) with subtle pulse animation
- **Nominal Status:** `#10b981` (Emerald-500)
- **Typography:** Inter / sans-serif with accessible contrast ratio > 4.5:1 compliant with WCAG 2.1 AA standards.
