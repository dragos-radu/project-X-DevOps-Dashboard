from fastapi import FastAPI

from app.database import check_database_connection

app = FastAPI(
    title="DevOps Dashboard Backend",
    description="Backend API for the Raspberry Pi DevOps Dashboard.",
    version="0.1.0",
)


@app.get("/health")
def health_check():
    database_status = "ok" if check_database_connection() else "unavailable"

    return {
        "status": "ok",
        "service": "devops-dashboard-backend",
        "database": database_status,
    }


@app.get("/api/dashboard")
def get_dashboard_data():
    return {
        "system": {
            "device": "Raspberry Pi",
            "cpu": "15%",
            "ram": "42%",
            "temperature": "48°C",
            "wifi": "Connected",
        },
        "weather": {
            "location": "Colibasi, Giurgiu",
            "temperature": "18°C",
            "condition": "Partly cloudy",
        },
        "pipelines": [
            {
                "name": "Backend CI/CD",
                "status": "success",
                "last_run": "placeholder",
            },
            {
                "name": "Frontend Deploy",
                "status": "success",
                "last_run": "placeholder",
            },
        ],
        "services": [
            {
                "name": "backend-api",
                "status": "running",
            },
            {
                "name": "database",
                "status": "running",
            },
            {
                "name": "frontend-ui",
                "status": "running",
            },
        ],
        "news": [
            {
                "title": "DevOps Dashboard backend initialized",
                "source": "local",
            }
        ],
    }