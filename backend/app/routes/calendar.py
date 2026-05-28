"""
Calendar API Routes
"""

from fastapi import APIRouter, Query
from app.calendar import get_calendar_manager

router = APIRouter(prefix="/calendar", tags=["Calendar"])


@router.get("/calendars")
def get_calendars():
    """Get list of available calendars"""
    manager = get_calendar_manager()
    calendars = manager.get_calendars()
    
    return {
        "status": "ok" if calendars else "no_calendars",
        "calendars": calendars,
    }


@router.get("/events")
def get_events(days: int = Query(default=30, ge=1, le=365)):
    """Get upcoming events (default 30 days)"""
    manager = get_calendar_manager()
    events = manager.get_events(days=days)
    
    # Calculate total events count
    total_events = sum(len(cal.get("events", [])) for cal in events)
    
    return {
        "status": "ok" if events else "no_events",
        "days": days,
        "total_events": total_events,
        "calendars": events,
    }


@router.get("/events/upcoming")
def get_upcoming_events():
    """Get next 5 events"""
    manager = get_calendar_manager()
    all_events = manager.get_events(days=30)
    
    upcoming = []
    for cal_data in all_events:
        for event in cal_data.get("events", [])[:2]:  # Max 2 per calendar
            upcoming.append({
                "calendar": cal_data.get("calendar"),
                **event
            })
    
    return {
        "status": "ok" if upcoming else "no_events",
        "upcoming": upcoming[:5],  # Top 5
    }
