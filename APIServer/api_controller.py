from fastapi import FastAPI
from api.status_api import router as api_router
from ws.status_ws import router as ws_router

app = FastAPI()

app.include_router(api_router)
app.include_router(ws_router)
