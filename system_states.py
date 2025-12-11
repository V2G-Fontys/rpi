from enum import Enum
from services.digipot_controller import DigipotService
from core.logger import get_logger

logger = get_logger("V2GRunner")

class States(Enum):
    CAR_DISCONNECTED = 0
    CAR_CONNECTED = 1
    PRECHARGE = 2
    CHARGING = 3
    DISCHARGING = 4
    CHARGE_TARGET_REACHED = 5
    IDLE = 6
    STOPPED_PROCESS = 7
    ERROR = 8

class SystemStates:
    def __init__(self):
        self.state = States.IDLE
    async def GetSystemState(status):
        return True
    async def SetupCharging(KWH, discharging):
        targetKWH = KWH
        if discharging:
            logger.info("discharging complete!")
        return True
