from datetime import datetime, timedelta, timezone

from email.utils import parsedate_to_datetime
from typing import Any

import feedparser

from app.database import get_database_config, get_database_connection

NEWS_FEEDS = [
    {
        "source": "DevOps.com",
        "url": "https://devops.com/feed/",
    },
    {
        "source": "The New Stack",
        "url": "https://thenewstack.io/feed/",
    },
    {
        "source": "Kubernetes Blog",
        "url": "https://kubernetes.io/feed.xml",
    },
    {
        "source": "Docker Blog",
        "url": "https://www.docker.com/blog/feed/",
    },
    {
        "source": "CNCF Blog",
        "url": "https://www.cncf.io/rss/",
    },
    {
        "source": "AWS DevOps Blog",
        "url": "https://aws.amazon.com/blogs/devops/feed/",
    },
    {
        "source": "Red Hat Blog",
        "url": "https://www.redhat.com/en/rss/blog",
    },
]


def create_news_table() -> None:
    query = """
        CREATE TABLE IF NOT EXISTS news (
            id SERIAL PRIMARY KEY,
            title TEXT NOT NULL,
            summary TEXT,
            url TEXT NOT NULL UNIQUE,
            source TEXT NOT NULL,
            external_id TEXT,
            published_at TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """

    with get_database_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(query)
        connection.commit()

def parse_feed_datetime(entry: Any) -> datetime | None:
    raw_date = (
        entry.get("published")
        or entry.get("updated")
        or entry.get("created")
    )

    if not raw_date:
        return None

    try:
        parsed_date = parsedate_to_datetime(raw_date)

        if parsed_date.tzinfo is not None:
            parsed_date = parsed_date.astimezone(timezone.utc).replace(tzinfo=None)

        return parsed_date
    except (TypeError, ValueError, IndexError, OverflowError):
        return None
    

def get_news_cutoff_date() -> datetime:
    today = datetime.now(timezone.utc).date()
    yesterday = today - timedelta(days=1)

    return datetime.combine(yesterday, datetime.min.time())


def is_recent_news(published_at: datetime | None) -> bool:
    if published_at is None:
        return True

    return published_at >= get_news_cutoff_date()


def delete_old_news() -> int:
    query = """
        DELETE FROM news
        WHERE published_at IS NOT NULL
          AND published_at < %s;
    """

    cutoff_date = get_news_cutoff_date()

    with get_database_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(query, (cutoff_date,))
            deleted_count = cursor.rowcount
        connection.commit()

    return deleted_count


def insert_news_item(
    title: str,
    summary: str | None,
    url: str,
    source: str | None,
    external_id: str | None,
    published_at: datetime | None,
) -> None:
    query = """
        INSERT INTO news (title, summary, url, source, external_id, published_at)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON CONFLICT (url)
        DO UPDATE SET
            title = EXCLUDED.title,
            summary = EXCLUDED.summary,
            source = EXCLUDED.source,
            external_id = EXCLUDED.external_id,
            published_at = EXCLUDED.published_at,
            updated_at = CURRENT_TIMESTAMP;
    """

    with get_database_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                query,
                (title, summary, url, source, external_id, published_at),
            )
        connection.commit()


def normalize_entry(feed_source: str, entry: Any) -> dict[str, Any] | None:
    title = (entry.get("title") or "").strip()
    url = (entry.get("link") or "").strip()

    if not title or not url:
        return None

    summary = (
        entry.get("summary")
        or entry.get("description")
        or entry.get("subtitle")
        or ""
    )

    external_id = (
        entry.get("id")
        or entry.get("guid")
        or entry.get("link")
    )

    published_at = parse_feed_datetime(entry)

    if not is_recent_news(published_at):
        return None

    return {
        "title": title,
        "summary": summary,
        "url": url,
        "source": feed_source,
        "external_id": external_id,
        "published_at": published_at,
    }


def fetch_news_from_feeds() -> dict[str, Any]:
    create_news_table()

    inserted_or_updated = 0
    failed_feeds: list[dict[str, str]] = []

    for feed in NEWS_FEEDS:
        source = feed["source"]
        feed_url = feed["url"]

        parsed_feed = feedparser.parse(feed_url)

        if parsed_feed.bozo:
            failed_feeds.append(
                {
                    "source": source,
                    "url": feed_url,
                    "error": str(parsed_feed.bozo_exception),
                }
            )
            continue

        for entry in parsed_feed.entries:
            news_item = normalize_entry(source, entry)

            if news_item is None:
                continue

            insert_news_item(**news_item)
            inserted_or_updated += 1

    deleted_old_items = delete_old_news()

    return {
        "status": "ok",
        "inserted_or_updated": inserted_or_updated,
        "deleted_old_items": deleted_old_items,
        "failed_feeds": failed_feeds,
    }


def get_news_items(limit: int = 20) -> list[dict[str, Any]]:
    create_news_table()

    query = """
        SELECT id, title, summary, url, source, external_id, published_at, created_at, updated_at
        FROM news
        ORDER BY COALESCE(published_at, created_at) DESC
        LIMIT %s;
    """

    with get_database_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(query, (limit,))
            rows = cursor.fetchall()

    return [
        {
            "id": row[0],
            "title": row[1],
            "summary": row[2],
            "url": row[3],
            "source": row[4],
            "external_id": row[5],
            "published_at": row[6],
            "created_at": row[7],
            "updated_at": row[8],
        }
        for row in rows
    ]


def get_news_item(news_id: int) -> dict[str, Any] | None:
    create_news_table()

    query = """
        SELECT id, title, summary, url, source, external_id, published_at, created_at, updated_at
        FROM news
        WHERE id = %s;
    """

    with get_database_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(query, (news_id,))
            row = cursor.fetchone()

    if row is None:
        return None

    return {
        "id": row[0],
        "title": row[1],
        "summary": row[2],
        "url": row[3],
        "source": row[4],
        "external_id": row[5],
        "published_at": row[6],
        "created_at": row[7],
        "updated_at": row[8],
    }