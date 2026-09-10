from flask import Flask, jsonify, render_template, request
from analytics import calculate_health, calculate_oee, trend_summary
from database import ensure_schema, get_connection, init_db
from mqtt_client import MQTTGateway, MQTT_TOPIC
from simulator import generate_reading

app = Flask(__name__)
init_db()
ensure_schema()

production_count = 0
mqtt_gateway = MQTTGateway()


def save_reading(reading, source="SIMULATOR"):
    with get_connection() as connection:
        connection.execute(
            """
            INSERT INTO readings
            (timestamp, temperature, rpm, voltage, current, machine_status, alarm, production_count, source)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                reading["timestamp"], reading["temperature"], reading["rpm"],
                reading["voltage"], reading["current"], reading["machine_status"],
                reading["alarm"], reading["production_count"], source,
            ),
        )
        if reading["alarm"] != "NORMAL":
            connection.execute(
                "INSERT INTO alarms (timestamp, alarm, severity) VALUES (?, ?, ?)",
                (reading["timestamp"], reading["alarm"], "HIGH"),
            )
        connection.commit()


def ingest_mqtt(payload):
    required = ["timestamp", "temperature", "rpm", "voltage", "current", "machine_status", "alarm", "production_count"]
    if all(key in payload for key in required):
        save_reading(payload, source="MQTT")


mqtt_gateway.on_message = ingest_mqtt
mqtt_gateway.start()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/reading")
def reading():
    global production_count
    if not mqtt_gateway.connected:
        data = generate_reading(production_count)
        production_count = data["production_count"]
        save_reading(data)
        return jsonify({**data, "source": "SIMULATOR", "health_score": calculate_health(data)})
    with get_connection() as connection:
        row = connection.execute("SELECT * FROM readings ORDER BY id DESC LIMIT 1").fetchone()
    if row:
        data = dict(row)
        data["health_score"] = calculate_health(data)
        return jsonify(data)
    return jsonify({"source": "MQTT", "message": "Waiting for machine telemetry"})


@app.route("/api/history")
def history():
    limit = min(max(request.args.get("limit", default=30, type=int), 1), 200)
    with get_connection() as connection:
        rows = connection.execute("SELECT * FROM readings ORDER BY id DESC LIMIT ?", (limit,)).fetchall()
    return jsonify([dict(row) for row in reversed(rows)])


@app.route("/api/alarms")
def alarms():
    with get_connection() as connection:
        rows = connection.execute("SELECT * FROM alarms ORDER BY id DESC LIMIT 20").fetchall()
    return jsonify([dict(row) for row in rows])


@app.route("/api/analytics")
def analytics():
    return jsonify({"oee": calculate_oee(), "trend": trend_summary()})


@app.route("/api/system")
def system():
    return jsonify({
        "data_source": "MQTT" if mqtt_gateway.connected else "SIMULATOR",
        "mqtt_connected": mqtt_gateway.connected,
        "topic": MQTT_TOPIC,
    })


if __name__ == "__main__":
    app.run(debug=True)
