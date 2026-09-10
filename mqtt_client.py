import json
import os

try:
    import paho.mqtt.client as mqtt
except ImportError:  # pragma: no cover
    mqtt = None

MQTT_HOST = os.getenv("MQTT_HOST", "localhost")
MQTT_PORT = int(os.getenv("MQTT_PORT", "1883"))
MQTT_TOPIC = os.getenv("MQTT_TOPIC", "factory/conveyor-01/telemetry")


class MQTTGateway:
    """MQTT edge subscriber used by the monitoring dashboard."""

    def __init__(self, on_message=None):
        self.on_message = on_message
        self.client = None
        self.connected = False

    def start(self):
        if mqtt is None:
            return False
        try:
            self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id="industrial-dashboard")
            self.client.on_connect = self._on_connect
            self.client.on_message = self._on_message
            self.client.connect_async(MQTT_HOST, MQTT_PORT, keepalive=60)
            self.client.loop_start()
            return True
        except Exception:
            self.connected = False
            return False

    def _on_connect(self, client, userdata, flags, reason_code, properties=None):
        self.connected = reason_code == 0
        if self.connected:
            client.subscribe(MQTT_TOPIC, qos=1)

    def _on_message(self, client, userdata, message):
        try:
            payload = json.loads(message.payload.decode("utf-8"))
            if self.on_message:
                self.on_message(payload)
        except (json.JSONDecodeError, UnicodeDecodeError):
            return

    def publish(self, payload):
        if not self.connected or self.client is None:
            return False
        result = self.client.publish(MQTT_TOPIC, json.dumps(payload), qos=1)
        return result.rc == mqtt.MQTT_ERR_SUCCESS

    def stop(self):
        if self.client:
            self.client.loop_stop()
            self.client.disconnect()
            self.connected = False
