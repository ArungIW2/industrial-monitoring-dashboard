# Conveyor 01 Control Sequence

## State machine

```text
IDLE
  |
  | START + safety OK + no fault
  v
RUNNING
  |
  +--> PART DETECTED --> production_count + 1
  |
  +--> MOTOR FAULT ----> FAULT
  |
  +--> STOP -----------> IDLE
  |
  +--> safety lost ----> FAULT

FAULT
  |
  | fault cleared + operator reset
  v
IDLE
```

## Interlock concept

Conveyor output `Y0` is permitted only when:

- Start request is active or the machine is in automatic run mode.
- Stop input is healthy.
- Safety chain status is healthy.
- Motor/inverter fault is clear.

The monitoring software does not bypass these interlocks and does not command `Y0`.

## Production counting

Use a rising-edge detection on the part sensor `X2` so one physical part increments the counter only once.

Conceptually:

```text
X2 rising edge
    -> validate part
    -> D104 = D104 + 1
    -> M103 = cycle complete
```

For a high-speed production line, use an appropriate high-speed counter/input rather than relying on a normal scan-cycle counter.

## Alarm examples

| Alarm | Trigger | Severity |
|---|---|---|
| MOTOR FAULT | X3 active | HIGH |
| SAFETY CHAIN | X4 not healthy | CRITICAL |
| HIGH TEMPERATURE | D100 >= 800 | HIGH |
| HIGH RPM | D101 >= 1650 | MEDIUM |
| HIGH CURRENT | D103 >= 1100 | HIGH |

Temperature/current thresholds are engineering examples, not universal limits. Actual limits must come from the motor, inverter, process and risk assessment.
