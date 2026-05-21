from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
#from routes import router

app = FastAPI()
#app.include_router(router)

# Serve the static files for the dashboard
app.mount("/", StaticFiles(directory="static", html=True), name="static")