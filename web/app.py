from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse, RedirectResponse
from core.clients.api_client import ApiClient
from core.config import API_URL, API_KEY
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
# from jinja2 import Environment, FileSystemLoader
from web.routes.api import router as api_router

app = FastAPI()
app.include_router(api_router)

api_client = ApiClient(base_url=API_URL, api_key=API_KEY)

# Serve the static files for the dashboard
app.mount("/static", StaticFiles(directory="web/static"), name="static")
templates = Jinja2Templates(directory="web/templates")

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("index.html", {
        "request": request
    })

@app.get("/settings", response_class=HTMLResponse)
def settings(request: Request):
    return RedirectResponse(url="/settings/accounts")

# @app.get("/settings/accounts", response_class=HTMLResponse)
# def accounts(request: Request):
#     accounts = api_client.get_accounts()
#     # Render template manually to avoid potential Jinja2 template cache issues
#     env = Environment(loader=FileSystemLoader("web/templates"))
#     with open("web/templates/accounts.html", "r", encoding="utf-8") as f:
#         tpl = env.from_string(f.read())

#     content = tpl.render(request=request, accounts=accounts)
#     return HTMLResponse(content)

@app.get("/settings/accounts", response_class=HTMLResponse)
def accounts(request: Request):
    accounts = api_client.get_accounts()
    return templates.TemplateResponse(
        request=request,
        name="accounts.html",
        context={"accounts":accounts})