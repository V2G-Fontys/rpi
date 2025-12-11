from fastapi import APIRouter
from fastapi.responses import JSONResponse
from APIServer.wsmanager.ws_manager import ConnectionManager
from pydantic import BaseModel
from services.digipot_controller import DigipotService
from system_states import SystemStates
from core.logger import get_logger

router = APIRouter()
digipot = DigipotService()
logger = get_logger("V2GRunner")

#endpoints:
#post charge({"target": 200}) -> {"ok": True} target = KWH target 
#post discharge({"target": 200}) -> {"ok": True}

#different payloads messages we handle from the websocket(APP)
class APIPayload(BaseModel):
    TargetKWH : int

class digipotPayload(BaseModel):
    DigitalPot : int
    
class MosfetPayload(BaseModel):
    GPIO : int
    toggle : bool
    
@router.post("/api/charge")
async def start_charging(payload : APIPayload):
    logger.info("Discharging started")
    discharging = False
    await SystemStates.SetupCharging(payload.TargetKWH, discharging);
    return JSONResponse({"ok": True})
    
@router.post("/api/discharge")
async def start_discharging(payload : APIPayload):
    logger.info("Discharging started")
    discharging = True
    await SystemStates.SetupCharging(payload, discharging);
    return JSONResponse({"ok": True})

@router.post("/api/status")
async def update_status():
    status = SystemState.GetSystemState()
    await asyncio.sleep(2)
    return JSONResponse({"status" : status})

@router.post("/api/mosfet")
async def update_status():
    
    await asyncio.sleep(2)
    return JSONResponse({"status" : status})
    
@router.post("/api/digipot")
async def update_status():
    
    await asyncio.sleep(2)
    return JSONResponse({"status" : status})

