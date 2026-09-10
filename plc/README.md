# Mitsubishi FX5U Conveyor 01 PLC

This project models a small industrial conveyor monitored by a Mitsubishi FX5U PLC.

## Machine scenario

**Conveyor 01** transports parts from an infeed station to an inspection station.
The PLC monitors motor operation, production count, temperature and electrical load.

The software side is READ-ONLY: it acquires PLC data and sends telemetry to the dashboard.
It does not write commands to the PLC.

## Suggested I/O list

| Address | Type | Signal | Description |
|---|---|---|---|
| X0 | DI | Start PB | Start conveyor |
| X1 | DI | Stop PB | Stop conveyor |
| X2 | DI | Part Sensor | Detect finished part |
| X3 | DI | Motor Fault | Inverter/motor fault input |
| X4 | DI | Emergency Stop OK | Safety-chain status input |
| Y0 | DO | Conveyor Run | Motor/inverter run command |
| Y1 | DO | Fault Lamp | Machine fault indication |
| Y2 | DO | Run Lamp | Machine running indication |

> Safety circuits must be implemented according to the actual machine risk assessment. Do not use this example as a safety-rated design.

## Suggested PLC data map

| Device | Meaning | Unit / encoding |
|---|---|---|
| D100 | Motor temperature | 0.1 °C |
| D101 | Conveyor motor speed | RPM |
| D102 | Motor voltage | 0.1 V |
| D103 | Motor current | 0.01 A |
| D104 | Production counter | parts |
| M100 | Conveyor running | 0/1 |
| M101 | Machine fault | 0/1 |
| M102 | Inspection station active | 0/1 |
| M103 | Cycle complete pulse | 0/1 |

These addresses are a portfolio example. Map them to the actual GX Works3 program before connecting to a real PLC.

## Operating sequence

1. Operator presses START (`X0`).
2. PLC verifies that STOP is healthy, the safety chain is OK and no motor fault is active.
3. PLC energizes `Y0` and sets `M100`.
4. Parts are detected by `X2`.
5. Each valid part increments `D104` and produces a cycle-complete event (`M103`).
6. Temperature/current/RPM values are updated in `D100-D103`.
7. A fault stops normal operation and sets `M101`.
8. The Python gateway reads these devices and publishes telemetry to MQTT.

## GX Works3 implementation notes

Create the PLC program around separate sections:

- `MAIN`: machine sequence/state logic
- `IO`: physical input/output mapping
- `COUNTER`: production and cycle counting
- `ALARM`: fault conditions
- `DATA`: engineering-unit values for the gateway

For a real FX5U, configure the Ethernet/SLMP communication parameters in GX Works3 and confirm the exact port/device addressing for the CPU and network module in use.

## Gateway mapping

The Python gateway reads:

```text
D100 -> temperature
D101 -> rpm
D102 -> voltage
D103 -> current
D104 -> production_count
M100 -> machine_status RUNNING/STOPPED
M101 -> machine_status FAULT
```

The resulting JSON is published to:

```text
factory/conveyor-01/telemetry
```

## Test before connecting to production equipment

Use a spare PLC, simulator or isolated test network first. Confirm scaling, byte/word representation, device addresses and update rates. Keep the monitoring application read-only until the complete system has been validated.
