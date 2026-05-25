from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from web.routes.api import router as api_router

app = FastAPI()
app.include_router(api_router)

# Serve the static files for the dashboard
app.mount("/static", StaticFiles(directory="web/static"), name="static")

@app.get("/")
def home():
    return FileResponse("web/static/index.html")

@app.get("/settings")
def settings():
    return FileResponse("web/static/settings.html")