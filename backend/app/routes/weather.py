"""
Weather API routes.
"""

from fastapi import APIRouter, HTTPException

from app.weather import fetch_current_weather


router = APIRouter(prefix="/weather", tags=["Weather"])


@router.get("")
def get_weather():
    try:
        return fetch_current_weather()
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Weather provider error: {e}")


@router.get("/current")
def get_current_weather():
    return get_weather()
