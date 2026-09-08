from flask import Flask, jsonify, render_template
from database import get_connection, init_db
from simulator import generate_reading

app = Flask(__name__)

production_count = 0


def save_reading(reading):
    with get_connection() as connection:
        connection.execute(
            """
            INSERT INTO readings
            (timestamp, temperature, rpm, voltage, current, machine_status, alarm, production_count)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                reading["timestamp"],
                reading["temperature"],
                reading["rpm"],
                reading["voltage"],
                reading["current"],
                reading["machine_status"],
                reading["alarm"],
                reading["production_count"],
            ),
        )
        connection.commit()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/reading")
def reading():
    global production_count
    data = generate_reading(production_count)
    production_count = data["production_count"]
    save_reading(data)
    return jsonify(data)


@app.route("/api/history")
def history():
    with get_connection() as connection:
        rows = connection.execute(
            "SELECT * FROM readings ORDER BY id DESC LIMIT 30"
        ).fetchall()
    return jsonify([dict(row) for row in reversed(rows)])


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
