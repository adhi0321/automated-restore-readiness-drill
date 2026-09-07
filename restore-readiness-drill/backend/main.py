from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from .database import init_db, get_all_drill_results
from .metrics import calculate_metrics
import os

app = FastAPI(title="Automated Restore-Readiness Drill")

@app.on_event("startup")
def on_startup():
    init_db()

@app.get("/api/results")
def get_results():
    results = get_all_drill_results()
    metrics = calculate_metrics(results)
    return {
        "metrics": metrics,
        "results": results
    }

# Serve frontend statically
frontend_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend")
app.mount("/static", StaticFiles(directory=frontend_path), name="static")

@app.get("/")
def serve_index():
    return FileResponse(os.path.join(frontend_path, "index.html"))
