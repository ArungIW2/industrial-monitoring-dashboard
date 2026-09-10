from database import get_connection

IDEAL_CYCLE_SECONDS = 2.0
PLANNED_MINUTES = 480.0


def calculate_oee():
    with get_connection() as connection:
        rows = connection.execute(
            "SELECT machine_status, production_count FROM readings ORDER BY id"
        ).fetchall()

    if not rows:
        return {"availability": 0, "performance": 0, "quality": 100, "oee": 0}

    running = sum(1 for row in rows if row["machine_status"] == "RUNNING")
    availability = min(100.0, (running / len(rows)) * 100)
    first = rows[0]["production_count"]
    last = rows[-1]["production_count"]
    produced = max(0, last - first)
    running_seconds = max(1.0, running * 3.0)
    performance = min(100.0, (produced * IDEAL_CYCLE_SECONDS / running_seconds) * 100)
    quality = 100.0
    oee = availability * performance * quality / 10000
    return {
        "availability": round(availability, 1),
        "performance": round(performance, 1),
        "quality": round(quality, 1),
        "oee": round(oee, 1),
    }


def calculate_health(reading):
    score = 100
    if reading["temperature"] >= 80:
        score -= 30
    elif reading["temperature"] >= 75:
        score -= 15
    if reading["current"] >= 11:
        score -= 30
    elif reading["current"] >= 10:
        score -= 15
    if reading["rpm"] >= 1650:
        score -= 20
    if not 210 <= reading["voltage"] <= 230:
        score -= 20
    return max(0, score)


def trend_summary():
    with get_connection() as connection:
        row = connection.execute(
            """
            SELECT
                AVG(temperature) AS avg_temperature,
                MAX(temperature) AS max_temperature,
                AVG(current) AS avg_current,
                MAX(current) AS max_current,
                AVG(rpm) AS avg_rpm,
                MAX(production_count) AS production_count
            FROM readings
            """
        ).fetchone()
    return {
        "avg_temperature": round(row["avg_temperature"] or 0, 1),
        "max_temperature": round(row["max_temperature"] or 0, 1),
        "avg_current": round(row["avg_current"] or 0, 2),
        "max_current": round(row["max_current"] or 0, 2),
        "avg_rpm": round(row["avg_rpm"] or 0, 0),
        "production_count": row["production_count"] or 0,
    }
