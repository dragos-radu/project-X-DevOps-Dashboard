import os

import requests
from PySide6.QtCore import QObject, Property, Signal, Slot, QTimer


DEFAULT_BACKEND_URL = os.getenv("DEVOPS_DASHBOARD_BACKEND_URL", "http://localhost:8001")


class WeatherController(QObject):
    weatherChanged = Signal()

    def __init__(self, backend_url: str = DEFAULT_BACKEND_URL):
        super().__init__()

        self._backend_url = backend_url.rstrip("/")
        self._loading = True
        self._online = False
        self._status = "Loading"
        self._temperature = "--°"
        self._min_max = "--° / --°"
        self._location = "Colibași, Giurgiu"
        self._sunrise = "--:--"
        self._sunset = "--:--"
        self._weather_code = -1
        self._icon_path = "assets/weather/unknown.svg"

        self._timer = QTimer()
        self._timer.setInterval(10 * 60 * 1000)
        self._timer.timeout.connect(self.refresh)
        self._timer.start()

        QTimer.singleShot(100, self.refresh)

    def _format_temperature(self, value) -> str:
        try:
            return f"{round(float(value))}°"
        except (TypeError, ValueError):
            return "--°"

    def _format_time(self, value) -> str:
        if not value:
            return "--:--"

        text = str(value)
        if "T" in text:
            return text.split("T", 1)[1][:5]

        return text[:5]

    def _icon_path_for_code(self, code: int) -> str:
        if code in (0, 1):
            return "assets/weather/clear.svg"
        if code == 2:
            return "assets/weather/partly-cloudy.svg"
        if code == 3:
            return "assets/weather/cloudy.svg"
        if code in (45, 48):
            return "assets/weather/fog.svg"
        if code in (51, 53, 55):
            return "assets/weather/drizzle.svg"
        if code in (56, 57, 66, 67):
            return "assets/weather/freezing-rain.svg"
        if code in (61, 63, 65):
            return "assets/weather/rain.svg"
        if code in (71, 73, 75, 85, 86):
            return "assets/weather/snow.svg"
        if code == 77:
            return "assets/weather/snow-grains.svg"
        if code in (80, 81, 82):
            return "assets/weather/showers.svg"
        if code in (95, 96, 99):
            return "assets/weather/thunderstorm.svg"

        return "assets/weather/unknown.svg"

    @Slot()
    def refresh(self):
        self._loading = True
        self.weatherChanged.emit()

        try:
            response = requests.get(f"{self._backend_url}/weather/current", timeout=2)
            response.raise_for_status()
            payload = response.json()

            today = payload.get("today", {})
            location = payload.get("location", {})
            weather_code = int(payload.get("weather_code", -1))

            self._online = True
            self._status = payload.get("condition") or "Unknown"
            self._temperature = self._format_temperature(payload.get("temperature"))
            self._min_max = (
                f"{self._format_temperature(today.get('min_temperature'))} / "
                f"{self._format_temperature(today.get('max_temperature'))}"
            )
            self._location = location.get("name") or "Colibași, Giurgiu"
            self._sunrise = self._format_time(today.get("sunrise"))
            self._sunset = self._format_time(today.get("sunset"))
            self._weather_code = weather_code
            self._icon_path = self._icon_path_for_code(weather_code)

        except Exception as error:
            print(f"Weather refresh failed: {error}")

            self._online = False
            self._status = "Offline"
            self._temperature = "--°"
            self._min_max = "--° / --°"
            self._weather_code = -1
            self._icon_path = "assets/weather/unknown.svg"

        self._loading = False
        self.weatherChanged.emit()

    @Property(bool, notify=weatherChanged)
    def loading(self):
        return self._loading

    @Property(bool, notify=weatherChanged)
    def online(self):
        return self._online

    @Property(str, notify=weatherChanged)
    def status(self):
        return self._status

    @Property(str, notify=weatherChanged)
    def temperature(self):
        return self._temperature

    @Property(str, notify=weatherChanged)
    def minMax(self):
        return self._min_max

    @Property(str, notify=weatherChanged)
    def location(self):
        return self._location

    @Property(str, notify=weatherChanged)
    def sunrise(self):
        return self._sunrise

    @Property(str, notify=weatherChanged)
    def sunset(self):
        return self._sunset

    @Property(int, notify=weatherChanged)
    def weatherCode(self):
        return self._weather_code

    @Property(str, notify=weatherChanged)
    def iconPath(self):
        return self._icon_path
