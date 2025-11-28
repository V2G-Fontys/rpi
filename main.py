import asyncio
from services.modbus_controller import ModbusService
from services.pyplc_bridge import PyPlcService
from services.digipot_controller import DigipotService
from core.logger import get_logger
import signal

logger = get_logger("V2GRunner")

async def main():
    logger.info("Starting V2G software stack...")

    modbus = ModbusService()
    pyplc = PyPlcService(modbus.send_to_backend)
    digipot = DigipotService()

    loop = asyncio.get_running_loop()
    stop_event = asyncio.Event()

    def shutdown():
        logger.info("Shutdown requested by user.")
        modbus.stop()
        pyplc.stop()
        digipot.stop()
        stop_event.set()

    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(sig, shutdown)

    await asyncio.gather(
        modbus.run(),
        pyplc.run(),
        stop_event.wait()
    )

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Shutdown requested by user.")
