from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse, RedirectResponse
from core.clients.api_client import ApiClient
from core.config import API_URL, API_KEY
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from web.routes.api import router as api_router
from core.services.account_service import get_accounts
from core.db import init_db

app = FastAPI()
app.include_router(api_router)

api_client = ApiClient(base_url=API_URL, api_key=API_KEY)

# Serve the static files for the dashboard
app.mount("/static", StaticFiles(directory="web/static"), name="static")
templates = Jinja2Templates(directory="web/templates")

@app.on_event("startup")
def startup_event():
    init_db()
    print("Database initialised successfully.")

# @app.get("/")
# def read_root():
#     return {"status": "online"}

@app.get("/")
def home(request: Request):
    sure_accounts = api_client.get_accounts()
    accounts = get_accounts()
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "sure_accounts": sure_accounts,
            "filtered_accounts": [a for a in accounts if a.sure_account_id in {sa['id'] for sa in sure_accounts}]
        }
    )
    
@app.get("/settings", response_class=HTMLResponse)
def settings(request: Request):
    return RedirectResponse(url="/settings/accounts")

@app.get("/settings/accounts", response_class=HTMLResponse)
def accounts(request: Request):
    sure_accounts = api_client.get_accounts()
    accounts = get_accounts()
    return templates.TemplateResponse(
        request=request,
        name="accounts.html",
        context=
         {
            "sure_accounts": sure_accounts,
            "accounts": accounts
         }
        )