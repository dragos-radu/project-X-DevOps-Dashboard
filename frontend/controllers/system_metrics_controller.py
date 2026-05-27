import os
import socket
import subprocess
import time
from pathlib import Path
from typing import List

import psutil
from PySide6.QtCore import QObject, Property, Signal, Slot, QTimer


BOOT_TIME = psutil.boot_time()


class SystemMetricsController(QObject):
    metricsChanged = Signal()

    def __init__(self):
        super().__init__()

        self._online = True

        self._cpu = "--%"
        self._ram = "--%"
        self._disk = "--%"
        self._temperature = "--°"
        self._uptime = "offline"
        self._hostname = socket.gethostname()
        self._wifi_signal_strength = None
        self._wifi_level = 0

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

    def _get_cpu_percent(self) -> float:
        return psutil.cpu_percent(interval=0.2)

    def _get_ram_percent(self) -> float:
        return psutil.virtual_memory().percent

    def _get_disk_percent(self) -> float:
        return psutil.disk_usage("/").percent

    def _get_uptime_seconds(self) -> int:
        return int(time.time() - BOOT_TIME)

    def _get_temperature_c(self) -> float | None:
        thermal_path = Path("/sys/class/thermal/thermal_zone0/temp")

        if thermal_path.exists():
            try:
                raw_value = thermal_path.read_text().strip()
                return round(int(raw_value) / 1000, 1)
            except (ValueError, OSError):
                return None

        return None

    def _get_wifi_signal_strength(self) -> int | None:
        try:
            result = subprocess.run(
                ["iwconfig", "wlan0"],
                capture_output=True,
                text=True,
                check=True,
            )

            for line in result.stdout.splitlines():
                if "Signal level" in line:
                    parts = line.split("Signal level=")

                    if len(parts) > 1:
                        signal_part = parts[1].split()[0]
                        return int(signal_part.replace("dBm", ""))

        except (subprocess.CalledProcessError, FileNotFoundError, ValueError):
            return None

        return None

    def _wifi_signal_to_level(self, signal_strength: int | None) -> int:
        if signal_strength is None:
            return 0

        # Typical dBm values:
        # -30 excellent, -50 good, -60 ok, -70 weak, below -80 bad
        if signal_strength >= -50:
            return 4
        if signal_strength >= -60:
            return 3
        if signal_strength >= -70:
            return 2
        if signal_strength >= -80:
            return 1

        return 0

    @Slot()
    def refresh(self):
        try:
            cpu_value = self._get_cpu_percent()
            ram_value = self._get_ram_percent()
            disk_value = self._get_disk_percent()
            temperature_value = self._get_temperature_c()
            uptime_seconds = self._get_uptime_seconds()
            wifi_signal_strength = self._get_wifi_signal_strength()

            self._online = True

            self._cpu_value = cpu_value
            self._ram_value = ram_value
            self._disk_value = disk_value
            self._temperature_value = (
                float(temperature_value)
                if temperature_value is not None
                else 0.0
            )

            self._cpu = f"{cpu_value:.0f}%"
            self._ram = f"{ram_value:.0f}%"
            self._disk = f"{disk_value:.0f}%"
            self._temperature = (
                f"{self._temperature_value:.0f}°"
                if temperature_value is not None
                else "N/A"
            )
            self._uptime = self._format_uptime(uptime_seconds)
            self._hostname = socket.gethostname()
            self._wifi_signal_strength = wifi_signal_strength
            self._wifi_level = self._wifi_signal_to_level(wifi_signal_strength)

            self._cpu_history = self._push_history_value(self._cpu_history, cpu_value)
            self._ram_history = self._push_history_value(self._ram_history, ram_value)

        except Exception as error:
            print(f"Local system metrics refresh failed: {error}")

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
            self._wifi_signal_strength = None
            self._wifi_level = 0

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

    @Property(str, notify=metricsChanged)
    def hostname(self):
        return self._hostname

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

    @Property(int, notify=metricsChanged)
    def wifiSignalStrength(self):
        return self._wifi_signal_strength if self._wifi_signal_strength is not None else 0

    @Property(int, notify=metricsChanged)
    def wifiLevel(self):
        return self._wifi_level