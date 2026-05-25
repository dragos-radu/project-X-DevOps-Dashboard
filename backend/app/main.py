from fastapi import FastAPI

app = FastAPI(
    title="DevOps Dashboard Backend",
    description="Backend API for the Raspberry Pi DevOps Dashboard.",
    version="0.1.0",
)


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "devops-dashboard-backend",
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