from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse
from core.clients.api_client import ApiClient
from core.config import API_URL, API_KEY
from fastapi.templating import Jinja2Templates
from web.routes.api import router as api_router

app = FastAPI()
app.include_router(api_router)

api_client = ApiClient(base_url=API_URL, api_key=API_KEY)

# Serve the static files for the dashboard
templates = Jinja2Templates(directory="web/static")
app.mount("/static", StaticFiles(directory="web/static"), name="static")

@app.get("/")
def home():
    return FileResponse("web/static/index.html")

@app.get("/settings", response_class=HTMLResponse)
def settings(request: Request):
    accounts = api_client.get_accounts()
    print(f"Accounts retrieved for settings page: {accounts}")
    return templates.TemplateResponse(
        request=request,
        name="settings.html",
        context={"accounts":accounts})