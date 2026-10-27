# JalUrja AI: 3-5 Minute Video Demonstration Script & Storyboard

This script is structured for recording the **3–5 minute pitch/demonstration video** (Resolution: 720p or 1080p, MP4/MOV format, Size: < 50MB) required by the MY Bharat portal.

---

## Video Overview & Target Breakdown
- **Target Duration:** 3 minutes 45 seconds (within the 3-5 minute limit)
- **Presenter Role:** Project Lead / Technical Architect
- **Visual Style:** Split screen / screencast with camera overlay and live prototype interaction.

---

## Detailed Minute-by-Minute Script

### Act 1: The Problem & Local Context (0:00 – 0:50)
* **Visual on Screen:**
  - News headlines / statistics regarding water shortages in major Indian cities (Bengaluru, Delhi, Chennai).
  - Graph displaying 40% Non-Revenue Water (NRW) loss and escalating municipal power tariffs.
* **Narration (Voiceover):**
  > *"Every single day, over 40% of treated, potable water in Indian cities vanishes before it ever reaches citizens' taps. Subsurface pipe bursts go undetected for days, leaking millions of liters underground while residents in downstream wards face bone-dry taps and depend on expensive private water tankers.*
  > *At the same time, municipal water boards spend up to 35% of their total operational budget just paying electricity bills for pumping water—often running heavy motors during peak evening hours when tariffs are highest.*
  > *To solve this critical dual challenge, we built **JalUrja AI**—an IoT and Machine Learning platform that stops water leakage in real time and optimizes pumping schedules using clean solar energy."*

---

### Act 2: Solution Overview & Architecture (0:50 – 1:40)
* **Visual on Screen:**
  - High-resolution system architecture diagram from `docs/ARCHITECTURE.md`.
  - Animation showing IoT acoustic sensors, pressure transducers, and the cloud AI engine.
* **Narration (Voiceover):**
  > *"JalUrja AI creates a digital twin of the city's water network. Non-invasive acoustic vibration sensors and pressure transducers are installed at key pipeline junctions, streaming real-time telemetry over LoRaWAN to our FastAPI analytics backend.*
  > *Here, two intelligent algorithms operate continuously:*
  > *First, an **Isolation Forest ML Anomaly Detector** that instantly spots pipeline fractures and leakages by correlating sudden pressure drops with high-frequency acoustic noise.*
  > *Second, a **Time-of-Day Pumping Optimizer** that forecasts 24-hour ward water demand and shifts heavy pump loads into cheap, green solar hours."*

---

### Act 3: Live Working Prototype Demonstration (1:40 – 2:50)
* **Visual on Screen:**
  - Screencast of the running JalUrja AI Web Dashboard (`http://localhost:8000`).
  - Navigating through the interactive Ward Grid Map.
  - Clicking on the active leak alert at *Node-102 (Koramangala 80ft Road)*.
  - Demonstrating the Pump Optimizer and Solar Tariff Dispatch chart.
* **Narration (Voiceover):**
  > *"Let's look at our working prototype in action.*
  > *On our live dashboard, municipal engineers see a real-time GIS map of all ward reservoirs, booster pumps, and monitoring junctions. Each node displays live pressure in bar, flow rate in liters per second, and acoustic vibration.*
  > *Notice Node-102 on Koramangala 80ft Road—the AI has flagged a **Critical Leak** with a 93% probability. The acoustic noise jumped to 68.7 decibels while downstream pressure collapsed from 3.5 to 1.7 bar. With one click, the system highlights the exact pipeline segment, shows GPS coordinates, and dispatches an automated maintenance ticket to the nearest field van.*
  > *Next, looking at our Pump Scheduling tab: our optimizer has automatically re-scheduled Koramangala Booster Pump 1 to run at full capacity between 10:00 AM and 4:00 PM to take advantage of solar off-peak electricity at ₹4.20/kWh, reducing reliance on expensive evening peak grid power."*

---

### Act 4: Impact, Feasibility & SDGs (2:50 – 3:30)
* **Visual on Screen:**
  - Summary KPI cards: 35% NRW Reduction, 22% Energy Bill Cut, 8-Month ROI.
  - Badges for UN SDG 6 (Clean Water), SDG 7 (Clean Energy), and SDG 11 (Sustainable Cities).
* **Narration (Voiceover):**
  > *"The impact is immediate and quantifiable. A standard municipal zone deploying JalUrja AI saves approximately 12 million liters of water every single day, lowers municipal pumping electricity bills by 22%, and recovers capital investment within just 8 to 11 months.*
  > *This directly drives UN Sustainable Development Goals 6, 7, and 11, supporting the Government of India's Jal Jeevan Mission (Urban) and Smart Cities Mission."*

---

### Act 5: Conclusion & Call to Action (3:30 – 3:45)
* **Visual on Screen:**
  - Project Title slide, Team credentials, and GitHub open-source repository link.
* **Narration (Voiceover):**
  > *"JalUrja AI bridges the gap between deep tech and essential public infrastructure to ensure that every drop counts and every kilowatt is optimized. Our complete codebase, technical architecture, and test cases are fully open-sourced on GitHub. Thank you!"*
