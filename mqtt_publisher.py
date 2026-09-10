import json
import os
import time

import paho.mqtt.client as mqtt

from simulator import generate_reading

HOST = os.getenv("MQTT_HOST", "localhost")
PORT = int(os.getenv("MQTT_PORT", "1883"))
TOPIC = os.getenv("MQTT_TOPIC", "factory/machine-01/telemetry")

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id="machine-01-simulator")
client.connect(HOST, PORT, 60)
client.loop_start()

production_count = 0
print(f"Publishing simulated machine telemetry to {TOPIC}")

try:
    while True:
        data = generate_reading(production_count)
        production_count = data["production_count"]
        client.publish(TOPIC, json.dumps(data), qos=1)
        print(data)
        time.sleep(3)
except KeyboardInterrupt:
    pass
finally:
    client.loop_stop()
    client.disconnect()
