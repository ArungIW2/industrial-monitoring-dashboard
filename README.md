# Industrial Monitoring Dashboard 🏭

A portfolio project that simulates a manufacturing machine monitoring system. The dashboard displays machine condition, sensor values, alarms, and production information in real time.

## Features

- Machine status: RUNNING, STOPPED, FAULT
- Temperature monitoring
- RPM monitoring
- Voltage and current monitoring
- Automatic alarm detection from configurable thresholds
- Production counter
- Simulated sensor data
- SQLite data storage
- Responsive web dashboard

## Architecture

```text
Sensor Simulator
      │
      ▼
   Flask API ───────► SQLite
      │
      ▼
 Web Dashboard
```

## Tech Stack

- Python 3.11+
- Flask
- SQLite
- HTML5
- CSS3
- JavaScript

## Run Locally

```bash
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

Linux/macOS:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Start the application:

```bash
python app.py
```

Open `http://127.0.0.1:5000` in your browser.

## Portfolio Value

This project demonstrates practical skills in Python web development, data logging, monitoring, basic industrial instrumentation concepts, and Industry 4.0-style visualization.

## Future Development

- MQTT integration
- ESP32 sensor input
- User authentication
- Historical charts
- OEE calculation
- PLC integration
- Docker deployment

## Author

**Arung Ikhsani Wijaya**

Background: Teknik Komputer dan Jaringan | Manufacturing Operations | Industrial Automation Interest
