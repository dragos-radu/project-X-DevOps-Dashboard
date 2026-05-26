from fastapi import APIRouter, HTTPException, Query

from app.news import (
    fetch_news_from_feeds,
    get_news_item,
    get_news_items,
)


router = APIRouter(prefix="/news", tags=["News"])


@router.get("")
def read_news(limit: int = Query(default=20, ge=1, le=100)):
    return get_news_items(limit=limit)


@router.get("/{news_id}")
def read_news_item(news_id: int):
    news_item = get_news_item(news_id)

    if news_item is None:
        raise HTTPException(status_code=404, detail="News item not found")

    return news_item


@router.post("/refresh")
def refresh_news():
    return fetch_news_from_feeds()