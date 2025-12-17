from fastapi import APIRouter
from fastapi.responses import JSONResponse
from APIServer.wsmanager.ws_manager import manager
from pydantic import BaseModel
from services.digipot_controller import DigipotService # temp 
from services.mosfet_controller import MosfetService # temp
from system_states import SSystem
from core.logger import get_logger

router = APIRouter()
digipot = DigipotService()  # temp for testing before states are done
mosfet = MosfetService()    # temp for testing before states are done
logger = get_logger("V2GRunner")


#different payloads messages we handle from the websocket(APP)
class APIPayload(BaseModel):
    TargetKWH: int

class DigipotPayload(BaseModel):
    potvalue: int
    
class MosfetPayload(BaseModel):
    GPIO: int
    toggle: bool
    
@router.post("/api/charge")
async def start_charging(payload : APIPayload):
    logger.info("Charging setup started")
    await SystemStates.SetupCharging(SystemState, payload.TargetKWH);
    return JSONResponse({"ok": True})
    
@router.post("/api/discharge")
async def start_discharging(payload : APIPayload):
    logger.info("Discharging setup started")
    await SystemStates.SetupDischarging(SystemState, payload.TargetKWH);
    return JSONResponse({"ok": True})

@router.post("/api/status")
async def update_status():
    state = SSystem.GetSystemState()
    print(f"DEBUG: current state sent: {status}")
    await asyncio.sleep(2)
    return JSONResponse({"status" : status})

#temporary endpoints Do not use in production####################################################
@router.post("/api/mosfet")
async def update_mosfet(payload: MosfetPayload):
    print(f"DEBUG: Type of payload: {type(payload)}")
    print(f"DEBUG: Payload dict: {payload.dict()}")
    await mosfet.set_mosfet(payload.GPIO, payload.toggle)
    
    return JSONResponse({"ok" : True})
    
@router.post("/api/digipot")
async def update_digipot(payload: DigipotPayload):
    digipot.set_digipot(payload.potvalue)
    await asyncio.sleep(2)
    return JSONResponse({"ok" : True})

