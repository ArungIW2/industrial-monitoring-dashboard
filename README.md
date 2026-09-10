# Industrial Monitoring Dashboard — Mitsubishi FX5U Conveyor 🏭

Portfolio-grade **Industry 4.0 machine monitoring system** focused on one concrete machine: a **motor-driven conveyor for material transfer / inspection**.

The production target is a **Mitsubishi MELSEC iQ-F FX5U PLC** connected over Ethernet using **SLMP/MC protocol**. The software reads PLC data in READ-ONLY mode, converts it into a standard telemetry model, publishes it over MQTT, stores it, and displays the machine condition in a Flask dashboard.

> **Important:** the device addresses below are an example tag map for this portfolio project. They are not universal Mitsubishi addresses. Before connecting to a real machine, match them to the actual PLC program and electrical documentation.

## Machine scope

**Machine:** Conveyor 01 — motor-driven material transfer / inspection conveyor.

Typical process:

```text
Photoelectric sensor → PLC counting logic → Conveyor motor → Material transfer
                              ↓
                     Production counter
                              ↓
                   Ethernet / SLMP telemetry
```

Monitored variables:

| PLC tag | Example device | Meaning | Scaling |
|---|---|---|---|
| Temperature | D100 | Motor/drive temperature | value / 10 |
| RPM | D101 | Conveyor motor speed | 1 rpm/unit |
| Voltage | D102 | Motor/drive voltage | value / 10 |
| Current | D103 | Motor current | value / 100 |
| Production count | D104 | Parts/material count | 1 count/unit |
| Running | M100 | Conveyor running state | ON/OFF |
| Fault | M101 | PLC/machine fault state | ON/OFF |

For a real plant, the temperature and electrical values would normally originate from suitable sensors, drives or analog modules, while the PLC handles machine logic and production counting.

## Architecture

```text
┌───────────────────────────────┐
│ Conveyor 01                   │
│ Motor + sensors + drive       │
└───────────────┬───────────────┘
                │
                ▼
┌───────────────────────────────┐
│ Mitsubishi FX5U PLC           │
│ Machine logic + counters      │
└───────────────┬───────────────┘
                │ Ethernet / SLMP
                ▼
┌───────────────────────────────┐
│ Industrial PC / Laptop        │
│ plc_gateway.py                │
│ READ ONLY                     │
└───────────────┬───────────────┘
                │ MQTT
                ▼
┌───────────────────────────────┐
│ Eclipse Mosquitto             │
└───────────────┬───────────────┘
                ▼
┌───────────────────────────────┐
│ Flask Dashboard               │
│ SQLite + alarms + OEE         │
└───────────────────────────────┘
```

## Mitsubishi integration

The PLC adapter is in:

```text
plc/mitsubishi_fx5u.py
plc_gateway.py
```

It uses the Python `pymcprotocol` library to communicate with Mitsubishi PLCs using the MC protocol / SLMP family over Ethernet.

The gateway **does not write coils/registers or control the machine**. It only reads telemetry. This is deliberate for a portfolio project and is safer as the first real-machine integration step.

### Network example

```text
Mitsubishi FX5U: 192.168.1.10
Industrial PC:   192.168.1.20
PLC port:        5007
MQTT broker:     Industrial PC / server
```

Both PLC and gateway PC must be configured for the actual factory network. Do not copy these IP addresses blindly.

## Configure the PLC map

Copy `.env.example` to `.env` and change the values to match the real PLC project.

```text
PLC_IP=192.168.1.10
PLC_PORT=5007
PLC_POLL_INTERVAL=1.0

PLC_TEMP_DEVICE=D100
PLC_RPM_DEVICE=D101
PLC_VOLTAGE_DEVICE=D102
PLC_CURRENT_DEVICE=D103
PLC_PRODUCTION_DEVICE=D104
PLC_RUNNING_DEVICE=M100
PLC_FAULT_DEVICE=M101
```

The device map must be agreed with the PLC programmer. For example, if the actual machine stores motor current in D220 instead of D103, set `PLC_CURRENT_DEVICE=D220`.

## Run without a PLC

The simulator remains available for development:

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

Install:

```bash
pip install -r requirements.txt
python app.py
```

Open:

```text
http://127.0.0.1:5000
```

## Run Mitsubishi + MQTT stack

1. Put the industrial PC on the same network/VLAN as the FX5U.
2. Configure the FX5U Ethernet/SLMP settings in GX Works according to the actual PLC project.
3. Confirm the PLC IP and MC protocol port.
4. Set the PLC device map in `.env`.
5. Install dependencies:

```bash
pip install -r requirements.txt
```

6. Start Mosquitto and the dashboard, then start the PLC gateway:

```bash
docker compose up --build mqtt dashboard
```

In another terminal on the industrial PC:

```bash
python plc_gateway.py
```

The gateway publishes to:

```text
factory/conveyor-01/telemetry
```

For a Docker-based gateway on a machine where the PLC network is reachable from the container, the included profile can be used:

```bash
docker compose --profile plc up --build
```

For an actual factory deployment, running the gateway directly on the industrial PC is often simpler because PLC routing, firewall rules and network interfaces can be managed explicitly.

## MQTT telemetry contract

Example payload:

```json
{
  "timestamp": "2026-09-11T08:00:00",
  "temperature": 67.8,
  "rpm": 1425,
  "voltage": 220.4,
  "current": 8.15,
  "machine_status": "RUNNING",
  "alarm": "NORMAL",
  "production_count": 1250,
  "machine_id": "CONVEYOR-01",
  "machine_type": "MOTOR_DRIVEN_CONVEYOR",
  "plc": "MITSUBISHI_FX5U"
}
```

## Project structure

```text
industrial-monitoring-dashboard/
├── app.py
├── analytics.py
├── database.py
├── simulator.py
├── mqtt_client.py
├── mqtt_publisher.py
├── plc_gateway.py
├── plc/
│   ├── __init__.py
│   └── mitsubishi_fx5u.py
├── Dockerfile
├── docker-compose.yml
├── mosquitto.conf
├── .env.example
├── requirements.txt
├── templates/
│   └── index.html
└── static/
    ├── app.js
    └── style.css
```

## API

- `GET /` — dashboard
- `GET /api/reading` — latest telemetry
- `GET /api/history?limit=30` — telemetry history
- `GET /api/alarms` — alarm history
- `GET /api/analytics` — OEE and health analytics
- `GET /api/system` — MQTT/data-source status

## Portfolio value

This version is intentionally more specific than a generic dashboard. It demonstrates:

- Mitsubishi FX5U PLC integration
- MC protocol / SLMP communication
- Industrial Ethernet concepts
- READ-ONLY PLC data acquisition
- Edge gateway design
- MQTT publish/subscribe
- Machine-specific telemetry mapping
- Production counting
- Alarm monitoring
- OEE and machine health analytics
- REST API + SQLite
- Docker deployment

## Real-machine safety boundary

This project is a monitoring/telemetry layer, not a safety PLC, SCADA safety system, or certified machine-control system. Do not use the dashboard or its network path for emergency-stop, interlock, guard, motion-safety or other safety-critical control. Validate the actual PLC program, electrical design, network configuration, cybersecurity controls and fail-safe behavior with qualified industrial personnel before connecting to production equipment.

## Author

**Arung Ikhsani Wijaya**

Background: Teknik Komputer dan Jaringan | Manufacturing Operations | Industrial Automation Interest
