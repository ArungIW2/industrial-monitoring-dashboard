# Industrial Monitoring Dashboard 🏭

A portfolio-grade **Industry 4.0 machine monitoring platform** built around an edge telemetry pipeline. It supports simulated machine data today and is structured so a PLC/industrial gateway can publish the same telemetry through MQTT later.

## Architecture

```text
┌──────────────────┐
│ Machine / PLC    │
│ Sensors + Logic  │
└────────┬─────────┘
         │
         │ MQTT
         ▼
┌──────────────────┐
│ Edge MQTT Broker │
│ Eclipse Mosquitto│
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Python Gateway   │
│ MQTT Subscriber  │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ SQLite Telemetry │
│ + Alarm History  │
└────────┬─────────┘
         │
         ├──────────────► OEE / Health Analytics
         │
         ▼
┌──────────────────────────────────┐
│ Flask Industry 4.0 Dashboard     │
│ Live telemetry • alarms • OEE    │
│ machine health • production      │
└──────────────────────────────────┘
```

## Features

- Realtime machine telemetry
- MQTT ingestion with automatic fallback to simulator mode
- Temperature, RPM, voltage and current monitoring
- Machine status: RUNNING, STOPPED, FAULT
- Alarm history with severity
- Machine health score
- OEE overview: Availability, Performance, Quality and OEE
- Production count
- Telemetry source indicator: MQTT / SIMULATOR
- Historical telemetry table
- Docker Compose stack with Mosquitto + dashboard + machine simulator
- Database migration support for the original project database

## Project Structure

```text
industrial-monitoring-dashboard/
├── app.py                 # Flask API + dashboard server
├── analytics.py           # OEE and machine health calculations
├── database.py            # Telemetry, alarms and production storage
├── simulator.py           # Machine telemetry generator
├── mqtt_client.py         # MQTT edge subscriber
├── mqtt_publisher.py      # Machine/PLC telemetry simulator publisher
├── Dockerfile
├── docker-compose.yml
├── mosquitto.conf
├── requirements.txt
├── templates/index.html
└── static/
    ├── app.js
    └── style.css
```

## Run locally — simulator mode

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

Start:

```bash
python app.py
```

Open `http://127.0.0.1:5000`.

If no MQTT broker is available, the dashboard automatically generates demo telemetry.

## Run the full with Docker

Install Docker Desktop, then:

```bash
docker compose up --build
```

Open `http://127.0.0.1:5000`.

The stack starts:

1. **Mosquitto** — MQTT broker
2. **machine-simulator** — publishes machine telemetry every 3 seconds
3. **dashboard** — subscribes to MQTT and stores telemetry in SQLite

Stop the stack:

```bash
docker compose down
```

## MQTT contract

Default topic:

```text
factory/machine-01/telemetry
```

Example payload:

```json
{
  "timestamp": "2026-09-10T08:00:00",
  "temperature": 68.4,
  "rpm": 1452,
  "voltage": 220.1,
  "current": 8.4,
  "machine_status": "RUNNING",
  "alarm": "NORMAL",
  "production_count": 125
}
```

For a real deployment, replace `mqtt_publisher.py` with a PLC/edge adapter that reads actual sensor or PLC values and publishes this contract. Do **not** connect the software directly to safety-critical machine controls without appropriate industrial engineering, network segmentation, testing and fail-safe design.

## API

- `GET /` — dashboard
- `GET /api/reading` — current/latest telemetry
- `GET /api/history?limit=30` — telemetry history
- `GET /api/alarms` — alarm history
- `GET /api/analytics` — OEE and machine health analytics
- `GET /api/system` — MQTT connection and data source status

## Portfolio Value

This version demonstrates a broader Industry 4.0 skill set:

- Industrial telemetry architecture
- MQTT publish/subscribe
- Edge gateway concepts
- REST API development
- Persistent machine data logging
- Alarm management
- OEE fundamentals
- Condition/health monitoring
- Dockerized deployment
- Separation between machine data acquisition and visualization

## Next realistic upgrade

The next step toward an actual factory installation is **PLC integration**: read tags/registers from a Siemens, Mitsubishi, Omron or other supported PLC using an appropriate industrial protocol such as OPC UA or Modbus TCP, then map those tags into the MQTT telemetry contract.

## Author

**Arung Ikhsani Wijaya**

Background: Teknik Komputer dan Jaringan | Manufacturing Operations | Industrial Automation Interest
