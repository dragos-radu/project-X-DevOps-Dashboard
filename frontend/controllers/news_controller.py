import os
import re
from datetime import datetime, timezone

import requests
from PySide6.QtCore import QObject, Property, Signal, Slot, QTimer


DEFAULT_BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:30080")


class NewsController(QObject):
    newsChanged = Signal()

    def __init__(self, backend_url: str = DEFAULT_BACKEND_URL):
        super().__init__()

        self._backend_url = backend_url.rstrip("/")
        self._loading = True
        self._online = False
        self._empty = True
        self._items = []
        self._last_fetch_minute_key = None

        self._timer = QTimer()
        self._timer.setInterval(30 * 1000)
        self._timer.timeout.connect(self._refresh_on_schedule)
        self._timer.start()

        QTimer.singleShot(100, self.refresh)

    def _clean_summary(self, value) -> str:
        if not value:
            return ""

        text = re.sub(r"<[^>]+>", "", str(value))
        text = re.sub(r"\s+", " ", text).strip()

        if len(text) > 180:
            return f"{text[:177].rstrip()}..."

        return text

    def _format_time(self, value) -> str:
        if not value:
            return ""

        text = str(value)

        try:
            if text.endswith("Z"):
                text = f"{text[:-1]}+00:00"

            parsed = datetime.fromisoformat(text)
            if parsed.tzinfo is not None:
                parsed = parsed.astimezone(timezone.utc).replace(tzinfo=None)

            return parsed.strftime("%d %b %H:%M")
        except ValueError:
            return text[:16]

    def _normalize_item(self, item) -> dict:
        timestamp = (
            item.get("published_at")
            or item.get("created_at")
            or item.get("updated_at")
            or ""
        )

        return {
            "id": item.get("id", ""),
            "title": item.get("title") or "Untitled news",
            "summary": self._clean_summary(item.get("summary")),
            "url": item.get("url") or "",
            "source": item.get("source") or "DevOps News",
            "publishedAt": self._format_time(timestamp),
        }

    def _current_minute_key(self) -> str:
        return datetime.now().strftime("%Y-%m-%d %H:%M")

    @Slot()
    def _refresh_on_schedule(self):
        now = datetime.now()

        if now.minute not in (10, 40):
            return

        minute_key = self._current_minute_key()
        if minute_key == self._last_fetch_minute_key:
            return

        self.refresh()

    @Slot()
    def refresh(self):
        self._last_fetch_minute_key = self._current_minute_key()
        self._loading = True
        self.newsChanged.emit()

        try:
            response = requests.get(f"{self._backend_url}/news", timeout=4)
            response.raise_for_status()
            payload = response.json()

            if not isinstance(payload, list):
                payload = []

            self._items = [self._normalize_item(item) for item in payload]
            self._online = True
            self._empty = len(self._items) == 0

        except Exception as error:
            print(f"News refresh failed: {error}")

            self._online = False
            self._empty = True
            self._items = []

        self._loading = False
        self.newsChanged.emit()

    @Property(bool, notify=newsChanged)
    def loading(self):
        return self._loading

    @Property(bool, notify=newsChanged)
    def online(self):
        return self._online

    @Property(bool, notify=newsChanged)
    def empty(self):
        return self._empty

    @Property("QVariantList", notify=newsChanged)
    def items(self):
        return self._items
