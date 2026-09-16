"""
main.py - Main entry point for SIH26063 Polar Portal
Serves backend REST APIs, RAG engine, and frontend assets.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

from server.routers import outreach, repository, media, ai, admin, live

app = FastAPI(
    title="NCPOR Integrated Polar Science Outreach & Repository Portal",
    description="MoES / NCPOR SIH26063 Integrated Portal uniting Science Outreach, Knowledge Repository, and Media Dissemination.",
    version="2.4.0"
)

# Enable CORS for local testing or external clients
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API Routers
app.include_router(outreach.router)
app.include_router(repository.router)
app.include_router(media.router)
app.include_router(ai.router)
app.include_router(admin.router)
app.include_router(live.router)


from server.data_store import data_store

@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "portal": "MoES / NCPOR Polar Science Gateway",
        "code": "SIH26063",
        "active_stations": ["Bharati", "Maitri", "Himadri", "Himansh"],
        "version": "2.4.0"
    }


@app.get("/api/stats")
def get_portal_stats():
    """Dynamically serves hero and portal headline statistics from data store."""
    return {
        "antarctic_expeditions": "43+",
        "arctic_campaigns": "16+",
        "southern_ocean_cruises": "12",
        "third_pole_altitude": "4,050m",
        "total_publications": len(data_store.publications),
        "total_datasets": len(data_store.datasets),
        "total_media_assets": len(data_store.media),
        "active_stations": len(data_store.stations)
    }


from fastapi.responses import FileResponse

# Mount Static directory
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
static_dir = os.path.join(base_dir, "static")
if not os.path.exists(static_dir):
    for candidate in [
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "static"),
        os.path.join(os.getcwd(), "static"),
        os.path.join(os.getcwd(), "server", "static")
    ]:
        if os.path.exists(candidate):
            static_dir = candidate
            break

# Client-side portal routes (SPA fallback to index.html)
@app.get("/resources", include_in_schema=False)
@app.get("/repository", include_in_schema=False)
@app.get("/media", include_in_schema=False)
@app.get("/stations", include_in_schema=False)
@app.get("/about", include_in_schema=False)
@app.get("/admin", include_in_schema=False)
@app.get("/outreach", include_in_schema=False)
def serve_portal_client_routes():
    index_path = os.path.join(static_dir, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    from fastapi import HTTPException
    raise HTTPException(status_code=404, detail="Portal index.html not found")

if os.path.exists(static_dir):
    app.mount("/", StaticFiles(directory=static_dir, html=True), name="static")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server.main:app", host="127.0.0.1", port=8000, reload=True)
