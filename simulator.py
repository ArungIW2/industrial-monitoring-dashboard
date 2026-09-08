import random
from datetime import datetime


def generate_reading(production_count=0):
    temperature = round(random.gauss(68, 5), 1)
    rpm = max(0, int(random.gauss(1450, 90)))
    voltage = round(random.gauss(220, 3), 1)
    current = round(random.gauss(8.5, 0.8), 2)

    alarms = []
    if temperature >= 80:
        alarms.append("HIGH TEMPERATURE")
    if rpm >= 1650:
        alarms.append("HIGH RPM")
    if voltage < 210 or voltage > 230:
        alarms.append("VOLTAGE OUT OF RANGE")
    if current >= 11:
        alarms.append("HIGH CURRENT")

    machine_status = "FAULT" if alarms else random.choices(
        ["RUNNING", "STOPPED"], weights=[92, 8], k=1
    )[0]

    if machine_status == "RUNNING":
        production_count += random.choice([0, 0, 1, 1, 2])

    return {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "temperature": temperature,
        "rpm": rpm,
        "voltage": voltage,
        "current": current,
        "machine_status": machine_status,
        "alarm": ", ".join(alarms) if alarms else "NORMAL",
        "production_count": production_count,
    }
