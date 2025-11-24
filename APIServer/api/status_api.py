from fastapi import APIRouter
from fastapi.responses import JSONResponse
from ws.status_ws import manager
from pydantic import BaseModel
from services.digipot_controller import DigipotService

router = APIRouter()
digipot = DigipotService()

class Payload(BaseModel):
    topic: str
    status: int

@router.post("/api/status")
async def update_status(payload: Payload):
    await manager.broadcast(payload.topic, {"status": payload.status})
    return JSONResponse({"ok": True, "sent": payload.status, "topic": payload.topic})
    
class DigipotPayload(BaseModel):
    voltage: int
    
@router.post("/api/digipot")
async def setDigipot(payload: DigipotPayload):
    # run digipot code
    await digipot.set_digipot(payload.voltage)
    return JSONResponse({"ok": True})
