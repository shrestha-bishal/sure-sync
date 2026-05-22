from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from web.routes.api import router as api_router

app = FastAPI()
app.include_router(api_router)

# Serve the static files for the dashboard
app.mount("/", StaticFiles(directory="web/static", html=True), name="static")