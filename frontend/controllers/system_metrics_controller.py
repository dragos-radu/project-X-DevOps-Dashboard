import os
from typing import List

import requests
from PySide6.QtCore import QObject, Property, Signal, Slot, QTimer


BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:30080")


class SystemMetricsController(QObject):
    metricsChanged = Signal()

    def __init__(self):
        super().__init__()

        self._online = False

        self._cpu = "--%"
        self._ram = "--%"
        self._disk = "--%"
        self._temperature = "--°"
        self._uptime = "offline"

        self._cpu_value = 0.0
        self._ram_value = 0.0
        self._disk_value = 0.0
        self._temperature_value = 0.0

        self._cpu_history = [0.0] * 10
        self._ram_history = [0.0] * 10

        self._timer = QTimer()
        self._timer.setInterval(2000)
        self._timer.timeout.connect(self.refresh)
        self._timer.start()

        self.refresh()

    def _format_uptime(self, seconds: int) -> str:
        days = seconds // 86400
        hours = (seconds % 86400) // 3600
        minutes = (seconds % 3600) // 60

        if days > 0:
            return f"{days}d, {hours}h"

        return f"{hours}h, {minutes}m"

    def _push_history_value(self, history: List[float], value: float) -> List[float]:
        updated = history + [value]
        return updated[-10:]

    @Slot()
    def refresh(self):
        try:
            response = requests.get(f"{BACKEND_URL}/metrics/system", timeout=2)
            response.raise_for_status()
            data = response.json()

            cpu_value = float(data.get("cpu_percent", 0))
            ram_value = float(data.get("ram_percent", 0))
            disk_value = float(data.get("disk_percent", 0))
            temp_value = data.get("temperature_c")
            uptime_seconds = int(data.get("uptime_seconds", 0))

            self._online = True

            self._cpu_value = cpu_value
            self._ram_value = ram_value
            self._disk_value = disk_value
            self._temperature_value = float(temp_value) if temp_value is not None else 0.0

            self._cpu = f"{cpu_value:.0f}%"
            self._ram = f"{ram_value:.0f}%"
            self._disk = f"{disk_value:.0f}%"
            self._temperature = (
                f"{self._temperature_value:.0f}°"
                if temp_value is not None
                else "N/A"
            )
            self._uptime = self._format_uptime(uptime_seconds)

            self._cpu_history = self._push_history_value(self._cpu_history, cpu_value)
            self._ram_history = self._push_history_value(self._ram_history, ram_value)

        except Exception as error:
            print(f"System metrics refresh failed: {error}")

            self._online = False

            self._cpu = "--%"
            self._ram = "--%"
            self._disk = "--%"
            self._temperature = "--°"
            self._uptime = "offline"

            self._cpu_value = 0.0
            self._ram_value = 0.0
            self._disk_value = 0.0
            self._temperature_value = 0.0

            self._cpu_history = self._push_history_value(self._cpu_history, 0.0)
            self._ram_history = self._push_history_value(self._ram_history, 0.0)

        self.metricsChanged.emit()

    @Property(bool, notify=metricsChanged)
    def online(self):
        return self._online

    @Property(str, notify=metricsChanged)
    def cpu(self):
        return self._cpu

    @Property(str, notify=metricsChanged)
    def ram(self):
        return self._ram

    @Property(str, notify=metricsChanged)
    def disk(self):
        return self._disk

    @Property(str, notify=metricsChanged)
    def temperature(self):
        return self._temperature

    @Property(str, notify=metricsChanged)
    def uptime(self):
        return self._uptime

    @Property(float, notify=metricsChanged)
    def cpuValue(self):
        return self._cpu_value

    @Property(float, notify=metricsChanged)
    def ramValue(self):
        return self._ram_value

    @Property(float, notify=metricsChanged)
    def diskValue(self):
        return self._disk_value

    @Property(float, notify=metricsChanged)
    def temperatureValue(self):
        return self._temperature_value

    @Property("QVariantList", notify=metricsChanged)
    def cpuHistory(self):
        return self._cpu_history

    @Property("QVariantList", notify=metricsChanged)
    def ramHistory(self):
        return self._ram_history
