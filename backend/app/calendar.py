"""
iCloud Calendar Integration using CalDAV
"""

import os
from datetime import date, datetime, time, timedelta
from zoneinfo import ZoneInfo
import caldav
from icalendar import Calendar

# Credentials from environment
ICLOUD_USERNAME = os.getenv("ICLOUD_USERNAME", "")
ICLOUD_APP_PASSWORD = os.getenv("ICLOUD_APP_PASSWORD", "")


def _as_utc_datetime(value, tz):
    if isinstance(value, datetime):
        if value.tzinfo is None:
            return value.replace(tzinfo=tz)
        return value.astimezone(tz)
    if isinstance(value, date):
        return datetime.combine(value, time.min, tzinfo=tz)
    return None


class iCloudCalendarManager:
    """Manager for iCloud calendar operations"""
    
    def __init__(self):
        self.client = None
        self.principal = None
        self.connect()
    
    def connect(self):
        """Connect to iCloud CalDAV server"""
        try:
            self.client = caldav.DAVClient(
                url="https://caldav.icloud.com",
                username=ICLOUD_USERNAME,
                password=ICLOUD_APP_PASSWORD,
            )
            self.principal = self.client.principal()
            return True
        except Exception as e:
            print(f"❌ iCloud connection error: {e}")
            return False
    
    def get_calendars(self):
        """Get list of available calendars"""
        try:
            calendars = list(self.principal.calendars())
            return [
                {
                    "id": cal.name,
                    "name": cal.get_display_name(),
                }
                for cal in calendars
            ]
        except Exception as e:
            print(f"❌ Calendar retrieval error: {e}")
            return []
    
    def get_events(self, days: int = 30):
        """Get events from the upcoming days"""
        try:
            tz = ZoneInfo("UTC")
            now = datetime.now(tz=tz)
            start_date = now
            end_date = now + timedelta(days=days)
            
            events_result = []
            calendars = list(self.principal.calendars())
            
            for cal in calendars:
                cal_name = cal.get_display_name()
                cal_events = []
                
                try:
                    all_events = cal.date_search(
                        start=start_date,
                        end=end_date,
                        expand=True,
                    )
                    
                    for event in all_events:
                        try:
                            ical = Calendar.from_ical(event.data)
                            for component in ical.walk():
                                if component.name == "VEVENT":
                                    dtstart = component.get("DTSTART")
                                    if not dtstart:
                                        continue

                                    event_dt = _as_utc_datetime(dtstart.dt, tz)
                                    if event_dt is None or not start_date <= event_dt <= end_date:
                                        continue

                                    summary = component.get("SUMMARY", "No title")
                                    location = component.get("LOCATION", "")
                                    dtend = component.get("DTEND")

                                    cal_events.append({
                                        "title": str(summary),
                                        "location": str(location) if location else None,
                                        "start": str(dtstart.dt),
                                        "end": str(dtend.dt) if dtend else None,
                                    })
                        except Exception as e:
                            print(f"Calendar event parse error: {e}")
                except Exception as e:
                    print(f"Calendar date search error for {cal_name}: {e}")
                
                if cal_events:
                    events_result.append({
                        "calendar": cal_name,
                        "events": cal_events,
                    })
            
            return events_result
        except Exception as e:
            print(f"❌ Events retrieval error: {e}")
            return []


# Singleton instance
_calendar_manager = None


def get_calendar_manager():
    """Get calendar manager instance (singleton)"""
    global _calendar_manager
    if _calendar_manager is None:
        _calendar_manager = iCloudCalendarManager()
    return _calendar_manager
