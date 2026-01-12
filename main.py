import asyncio
from core.logger import get_logger
from system_states import StateSystem
from services.digipot_controller import DigipotService
from services.modbus_controller import ModbusService
from services.pyplc_bridge import PyPlcService
from services.mosfet_controller import *
from APIServer.endpoints.api_endpoints import *
import signal


#include other logger inside class(instead of globally)
logger = get_logger("V2GRunner")

async def main():
    loop = asyncio.get_running_loop()
    stop_event = asyncio.Event()
    
    #start up all the services
    logger.info("Starting V2G software stack...")
    modbus = ModbusService()
    pyplc = PyPlcService()

    #start pyplc and the statesystem
    loop.create_task(pyplc.run())
    logger.info("Starting State Systen loop")
    #await asyncio.sleep(2) # wait until pyplc is done with init
    loop.create_task(StateSystem.run())
    
    loop.create_task(StateSystem.SetupDischarging(20))
    await asyncio.gather(stop_event.wait())
    
    def shutdown():
        logger.info("Shutdown requested by user.")
        stop_event.set()
    
    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(sig, shutdown)
    logger.info("Shutdown requested by user.")
    
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Shutdown requested by user.")
