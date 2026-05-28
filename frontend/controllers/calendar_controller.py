import os
from datetime import date, datetime, timedelta, timezone

import requests
from PySide6.QtCore import QObject, Property, Signal, Slot, QTimer


BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:30080")


class CalendarController(QObject):
    calendarChanged = Signal()

    def __init__(self, backend_url: str = BACKEND_URL):
        super().__init__()

        self._backend_url = backend_url.rstrip("/")
        self._loading = True
        self._online = False
        self._first_event_name = "No upcoming events"
        self._first_event_datetime = ""
        self._second_event_name = ""
        self._second_event_datetime = ""

        self._timer = QTimer()
        self._timer.setInterval(5 * 60 * 1000)
        self._timer.timeout.connect(self.refresh)
        self._timer.start()

        QTimer.singleShot(150, self.refresh)

    def _parse_datetime(self, value):
        if not value:
            return None

        text = str(value)

        try:
            if text.endswith("Z"):
                text = f"{text[:-1]}+00:00"
            return datetime.fromisoformat(text)
        except ValueError:
            pass

        try:
            return datetime.combine(date.fromisoformat(text[:10]), datetime.min.time())
        except ValueError:
            return None

    def _format_event_datetime(self, value) -> str:
        event_time = self._parse_datetime(value)
        if event_time is None:
            return "Time unavailable"

        now = datetime.now(event_time.tzinfo or timezone.utc)
        event_date = event_time.date()

        if event_date == now.date():
            label = "Today"
        elif event_date == now.date() + timedelta(days=1):
            label = "Tomorrow"
        else:
            label = event_time.strftime("%d %b")

        if event_time.time() == datetime.min.time():
            return label

        return f"{label} {event_time.strftime('%H:%M')}"

    def _normalize_events(self, payload):
        if "upcoming" in payload:
            return payload.get("upcoming") or []

        events = []
        for calendar in payload.get("calendars", []) or []:
            calendar_name = calendar.get("calendar")
            for event in calendar.get("events", []) or []:
                events.append({
                    "calendar": calendar_name,
                    **event,
                })

        return events

    def _event_sort_key(self, event):
        event_time = self._parse_datetime(event.get("start"))
        if event_time is None:
            return float("inf")

        return event_time.timestamp()

    @Slot()
    def refresh(self):
        self._loading = True
        self.calendarChanged.emit()

        try:
            try:
                response = requests.get(
                    f"{self._backend_url}/calendar/events/upcoming",
                    timeout=3,
                )
                response.raise_for_status()
                payload = response.json()
            except requests.RequestException:
                response = requests.get(
                    f"{self._backend_url}/calendar/events",
                    timeout=3,
                )
                response.raise_for_status()
                payload = response.json()

            events = self._normalize_events(payload)
            events.sort(key=self._event_sort_key)

            self._online = True

            if not events:
                self._first_event_name = "No upcoming events"
                self._first_event_datetime = ""
                self._second_event_name = ""
                self._second_event_datetime = ""
            else:
                first_event = events[0]
                second_event = events[1] if len(events) > 1 else None

                self._first_event_name = first_event.get("title") or "Untitled event"
                self._first_event_datetime = self._format_event_datetime(first_event.get("start"))

                if second_event is None:
                    self._second_event_name = ""
                    self._second_event_datetime = ""
                else:
                    self._second_event_name = second_event.get("title") or "Untitled event"
                    self._second_event_datetime = self._format_event_datetime(second_event.get("start"))

        except Exception as error:
            print(f"Calendar refresh failed: {error}")

            self._online = False
            self._first_event_name = "Calendar offline"
            self._first_event_datetime = ""
            self._second_event_name = ""
            self._second_event_datetime = ""

        self._loading = False
        self.calendarChanged.emit()

    @Property(bool, notify=calendarChanged)
    def loading(self):
        return self._loading

    @Property(bool, notify=calendarChanged)
    def online(self):
        return self._online

    @Property(str, notify=calendarChanged)
    def firstEventName(self):
        return self._first_event_name

    @Property(str, notify=calendarChanged)
    def firstEventDateTime(self):
        return self._first_event_datetime

    @Property(str, notify=calendarChanged)
    def secondEventName(self):
        return self._second_event_name

    @Property(str, notify=calendarChanged)
    def secondEventDateTime(self):
        return self._second_event_datetime
