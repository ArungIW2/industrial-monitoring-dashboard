"""Edge gateway: Mitsubishi FX5U -> MQTT.

Run this on an industrial PC or laptop that can reach the PLC Ethernet network.
The gateway is intentionally READ-ONLY toward the PLC.
"""

import json
import os
import time

import paho.mqtt.client as mqtt

from plc.mitsubishi_fx5u import MitsubishiFX5UReader

MQTT_HOST = os.getenv("MQTT_HOST", "localhost")
MQTT_PORT = int(os.getenv("MQTT_PORT", "1883"))
MQTT_TOPIC = os.getenv("MQTT_TOPIC", "factory/conveyor-01/telemetry")
POLL_INTERVAL = float(os.getenv("PLC_POLL_INTERVAL", "1.0"))


def main():
    plc = MitsubishiFX5UReader()
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id="mitsubishi-fx5u-gateway")
    client.connect(MQTT_HOST, MQTT_PORT, keepalive=60)
    client.loop_start()

    try:
        while True:
            try:
                reading = plc.read_machine()
                reading["machine_id"] = "CONVEYOR-01"
                reading["machine_type"] = "MOTOR_DRIVEN_CONVEYOR"
                reading["plc"] = "MITSUBISHI_FX5U"
                result = client.publish(MQTT_TOPIC, json.dumps(reading), qos=1)
                if result.rc != mqtt.MQTT_ERR_SUCCESS:
                    print("MQTT publish failed", flush=True)
            except Exception as exc:
                plc.close()
                print(f"PLC connection/read error: {exc}", flush=True)
            time.sleep(POLL_INTERVAL)
    except KeyboardInterrupt:
        pass
    finally:
        plc.close()
        client.loop_stop()
        client.disconnect()


if __name__ == "__main__":
    main()
