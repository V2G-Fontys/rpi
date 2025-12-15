from enum import Enum
from services.digipot_controller import digipot
from services.modbus_controller import ModbusService
from services.pyplc_bridge import PyPlcService # maybe not necesarry
from services.mosfet_controller import mosfet
from core.logger import get_logger
import asyncio

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


class StateMachine:
    def __init__(self):
        self.state = States.IDLE
        self.target_KWH = 0
        self.current_KWH = 0
        self.discharging = False
        self.running = True
        self.logger = get_logger("StateMachine")
        
    async def GetSystemState(self):
        return self.state
        
    async def SetupCharging(self, KWH):
        if(self.state != States.IDLE):
            self.logger.warning("SetupCharging was called with the wrong state!")
            pass
        self.target_KWH = KWH
        self.state = States.CAR_DISCONNECTED
        self.logger.info(f"Charging setup for {KWH} kWh")
        
        
    async def SetupDischarging(self ,KWH):
        if(self.state != States.IDLE):
            self.logger.warning("SetupDischarging was called with the wrong state!")
            pass
        self.target_KWH = KWH
        self.discharging = True
        self.state = States.CAR_DISCONNECTED
        self.logger.info(f"Discharging setup for {KWH} kWh")
        
    async def run(self):
        while self.running:
            try:
                self.logger.debug(f"STATE = {self.state.name}")
                if self.state == States.IDLE:
                    await self._handle_idle()

                elif self.state == States.CAR_DISCONNECTED:
                    await self._handle_car_disconnected()

                elif self.state == States.CAR_CONNECTED:
                    await self._handle_car_connected()

                elif self.state == States.PRECHARGE:
                    await self._handle_precharge()

                elif self.state == States.CHARGING:
                    await self._handle_charging()

                elif self.state == States.DISCHARGING:
                    await self._handle_discharging()

                elif self.state == States.CHARGE_TARGET_REACHED:
                    await self._handle_target_reached()

                elif self.state == States.ERROR:
                    await self._handle_error()

                await asyncio.sleep(0.5)

            except Exception as e:
                self.logger.exception(e)
                self.state = States.ERROR

    async def _handle_idle(self):
        # Waiting for user command
        self.logger.debug("System idle")
        
    async def _handle_car_disconnected(self):
        self.logger.info("Waiting for car connection")

        #connected = await pyplc.is_car_connected()
        connected = True
        
        if connected:
            self.state = States.CAR_CONNECTED

    async def _handle_car_connected(self):
        self.logger.info("Car connected")
        
        # Decide direction based on target
        if self.target_KWH > 0:
            self.state = States.PRECHARGE
        else:
            self.state = States.ERROR
            
    async def _handle_precharge(self):
        self.logger.info("Precharging")

        await mosfet.set_mosfet(11, 1)
        await asyncio.sleep(4) 

        await mosfet.set_mosfet(11, 1)
        await mosfet.set_mosfet(11, 1)
        await digipot.set_digipot(200)
        # Decide next state
        if(self.discharging):
            self.state = States.DISCHARGING
        else:
            self.state = States.CHARGING

    async def _handle_discharging(self):
        self.logger.info("Discharging EV")

        #can not currently use modbus
        #voltage = await modbus.read_voltage()
        #current = await modbus.read_current()
        voltage = 426
        current = 16
        power_kw = (voltage * current) / 1000
        self.current_KWH += power_kw * (0.5 / 3600)
        self.logger.info(f"Discharged {self.current_KWH:.2f}  {self.target_KWH} kWh")

        if self.current_KWH >= self.target_KWH:
            self.state = States.CHARGE_TARGET_REACHED

    async def _handle_target_reached(self):
        self.logger.info("Target reached, shutting down")

        #digipot.set_digipot(0)
        #mosfet.disable_all()

        self.current_KWH = 0
        self.target_KWH = 0
        self.state = States.IDLE

    async def _handle_error(self):
        self.logger.error("System error!")

        #digipot.set_digipot(0)
        #mosfet.disable_all()
        
        await asyncio.sleep(5)
        self.state = States.IDLE


SSystem = StateMachine()

