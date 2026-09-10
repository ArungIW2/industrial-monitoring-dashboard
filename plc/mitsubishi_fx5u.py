"""Mitsubishi FX5U SLMP/MC protocol reader for the conveyor machine.

Default device map is intentionally configurable because the real PLC program
may use different D/M addresses. This module is READ-ONLY: it never writes to
PLC devices.
"""

import os
from datetime import datetime

try:
    import pymcprotocol
except ImportError:  # pragma: no cover
    pymcprotocol = None


class MitsubishiFX5UReader:
    """Read telemetry tags from a Mitsubishi FX5U over Ethernet (SLMP/MC)."""

    def __init__(self):
        self.ip = os.getenv("PLC_IP", "192.168.1.10")
        self.port = int(os.getenv("PLC_PORT", "5007"))
        self.timeout = float(os.getenv("PLC_TIMEOUT", "2.0"))

        self.temp_device = os.getenv("PLC_TEMP_DEVICE", "D100")
        self.rpm_device = os.getenv("PLC_RPM_DEVICE", "D101")
        self.voltage_device = os.getenv("PLC_VOLTAGE_DEVICE", "D102")
        self.current_device = os.getenv("PLC_CURRENT_DEVICE", "D103")
        self.production_device = os.getenv("PLC_PRODUCTION_DEVICE", "D104")
        self.running_device = os.getenv("PLC_RUNNING_DEVICE", "M100")
        self.fault_device = os.getenv("PLC_FAULT_DEVICE", "M101")

        self.client = None
        self.connected = False

    def connect(self):
        if pymcprotocol is None:
            raise RuntimeError("pymcprotocol is not installed")

        self.client = pymcprotocol.Type3E()
        self.client.connect(self.ip, self.port)
        self.connected = True

    def close(self):
        if self.client:
            try:
                self.client.close()
            except Exception:
                pass
        self.connected = False

    def _read_word(self, device):
        values = self.client.batchread_wordunits(headdevice=device, readsize=1)
        return values[0]

    def _read_bit(self, device):
        values = self.client.batchread_bitunits(headdevice=device, readsize=1)
        return bool(values[0])

    def read_machine(self):
        if not self.connected:
            self.connect()

        temperature = self._read_word(self.temp_device) / 10.0
        rpm = self._read_word(self.rpm_device)
        voltage = self._read_word(self.voltage_device) / 10.0
        current = self._read_word(self.current_device) / 100.0
        production_count = self._read_word(self.production_device)
        running = self._read_bit(self.running_device)
        fault = self._read_bit(self.fault_device)

        alarms = []
        if fault:
            alarms.append("PLC FAULT")
        if temperature >= 80:
            alarms.append("HIGH TEMPERATURE")
        if rpm >= 1650:
            alarms.append("HIGH RPM")
        if voltage < 210 or voltage > 230:
            alarms.append("VOLTAGE OUT OF RANGE")
        if current >= 11:
            alarms.append("HIGH CURRENT")

        status = "FAULT" if fault else ("RUNNING" if running else "STOPPED")

        return {
            "timestamp": datetime.now().isoformat(timespec="seconds"),
            "temperature": round(temperature, 1),
            "rpm": int(rpm),
            "voltage": round(voltage, 1),
            "current": round(current, 2),
            "machine_status": status,
            "alarm": ", ".join(alarms) if alarms else "NORMAL",
            "production_count": int(production_count),
        }
