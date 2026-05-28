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
from datetime import datetime

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
    filtered_accounts = [a for a in accounts if a.sure_account_id in {sa['id'] for sa in sure_accounts}]
    recent_transactions = {}
    mapped_accounts = [
        {
            "id": a.id,
            "sure_account_id": a.sure_account_id,
            "name": a.account_name
        }
        for a in accounts
    ]
    for account in filtered_accounts:
        response = api_client.get_transactions(params={"account_id": account.sure_account_id})
        txs = response.get("transactions", [])
        
        if txs:
            raw_date = txs[0].get("date")
            dt = datetime.fromisoformat(raw_date.replace('Z', '+00:00'))
            recent_transactions[account.sure_account_id] = dt.strftime("%A, %b %d, %Y")
        else:
            recent_transactions[account.sure_account_id] = None

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "sure_accounts": sure_accounts,
            "filtered_accounts": filtered_accounts,
            "recent_transactions": recent_transactions,
            "mapped_accounts": mapped_accounts
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