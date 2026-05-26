import os
import time
from pathlib import Path

import psutil

BOOT_TIME = psutil.boot_time()


def get_cpu_percent():
    return psutil.cpu_percent(interval=0.2)

def get_ram_percent():
    return psutil.virtual_memory().percent

def get_disk_percent():
    return psutil.disk_usage('/').percent

def get_uptime_seconds():
    return int(time.time() - BOOT_TIME)

def get_temperature_c() -> float | None:
    thermal_path = Path("/sys/class/thermal/thermal_zone0/temp")

    if thermal_path.exists():
        try:
            raw_value = thermal_path.read_text().strip()
            return round(int(raw_value) / 1000, 1)
        except (ValueError, OSError):
            return None

    return None


def get_system_metrics() -> dict:
    return {
        "cpu_percent": get_cpu_percent(),
        "ram_percent": get_ram_percent(),
        "disk_percent": get_disk_percent(),
        "temperature_c": get_temperature_c(),
        "uptime_seconds": get_uptime_seconds(),
        "hostname": os.uname().nodename,
    }
    
