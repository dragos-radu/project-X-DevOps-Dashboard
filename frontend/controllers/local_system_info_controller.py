import os
import platform
import socket
from pathlib import Path

from PySide6.QtCore import QObject, Property, Signal


class LocalSystemInfoController(QObject):
    systemInfoChanged = Signal()

    def __init__(self):
        super().__init__()

        self._hostname = self._get_hostname()
        self._os_name = self._get_os_name()
        self._local_ip = self._get_local_ip()

    def _get_hostname(self) -> str:
        return socket.gethostname()

    def _get_os_name(self) -> str:
        os_release_path = Path("/etc/os-release")

        if os_release_path.exists():
            try:
                for line in os_release_path.read_text().splitlines():
                    if line.startswith("PRETTY_NAME="):
                        return line.split("=", 1)[1].strip().strip('"')
            except OSError:
                pass

        return platform.system()

    def _get_local_ip(self) -> str:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
                sock.connect(("8.8.8.8", 80))
                return sock.getsockname()[0]
        except OSError:
            return "Unavailable"

    @Property(str, notify=systemInfoChanged)
    def hostname(self):
        return self._hostname

    @Property(str, notify=systemInfoChanged)
    def osName(self):
        return self._os_name

    @Property(str, notify=systemInfoChanged)
    def localIp(self):
        return self._local_ip