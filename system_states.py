from enum import Enum, IntEnum
from services.digipot_controller import digipot
from services.modbus_controller import ModbusService
from services.pyplc_bridge import pyplc
from services.mosfet_controller import *
from core.logger import get_logger
import asyncio

class States(IntEnum):
    CAR_DISCONNECTED = 0
    PRECHARGE = 1
    CHARGING = 2
    DISCHARGING = 3
    IDLE = 4
    ERROR = 5

class Status(IntEnum):
    CAR_DISCONNECTED = 0
    CONNECTING_CAR = 1
    CAR_CONNECTED = 2
    BOOST_CONVERTER = 3
    PRECHARGING = 4
    CHARGING_CAR = 5
    DISCHARGING_CAR = 6
    STANDBY = 7
    ERROR = 8
    
    
class StateMachine:
    def __init__(self):
        self.state = States.IDLE
        self.status = Status.CAR_DISCONNECTED
        self.target_KWH = 0
        self.current_KWH = 0
        self.discharging = False
        self.running = True
        self.logger = get_logger("StateMachine")
        
    #send status to the box API    
    async def GetStatus(self):
        return self.status
        
    #gets called to get ready for charging(not needed in current project goals)    
    async def SetupCharging(self, KWH):
        if(self.state != States.IDLE):
            self.logger.warning("SetupCharging was called with the wrong state!")
            pass
        if self.target_KWH <= 0:
            self.state = States.ERROR
        self.target_KWH = KWH
        self.state = States.CAR_DISCONNECTED
        self.status = Status.SETTING_UP
        self.logger.info(f"Charging setup for {KWH} kWh")
        
    #gets called to get ready for discharging    
    async def SetupDischarging(self ,KWH):
        if(self.state != States.IDLE):
            self.logger.warning("SetupDischarging was called with the wrong state!")
            pass
        self.target_KWH = KWH
        self.discharging = True
        self.state = States.CAR_DISCONNECTED
        self.logger.info(f"Discharging setup for {KWH} kWh")
        
    #loop for the states
    async def run(self):
        while self.running:
            try:
                self.logger.debug(f"STATE = {self.state.name}")
                match self.state:
                    case States.CAR_DISCONNECTED:
                        await self._handle_car_disconnected()
                    case States.PRECHARGE:
                        await self._handle_precharge()
                    case States.CHARGING:
                        await self._handle_charging()
                    case States.DISCHARGING:
                        await self._handle_discharging()
                    case States.IDLE:
                        await self._handle_idle()
                    case States.ERROR:       
                        await self._handle_error()
                        
                await asyncio.sleep(0.5)

            except Exception as e:
                self.logger.exception(e)
                self.state = States.ERROR
    
    #idle switch case, do nothing
    async def _handle_idle(self):
        await mosfet.disable_mosfets()
        self.logger.debug("System idle")
        
    #tries to connect to car, also checks if target KWH is correct    
    async def _handle_car_disconnected(self):
        self.logger.info("Waiting for car connection")

        connected = await pyplc.is_car_prechargemode()
        self.logger.info(connected)
        if connected:
            self.state = States.PRECHARGE
        else:
            self.logger.info("could not connect to car, trying again")
    
    #precharge phase, this is where the boost converter precharge and SSR relays get switched on
    async def _handle_precharge(self):
        self.logger.info("Precharging")
        
        val = 1 #should be true if they need to be switched o
        await mosfet.disable_mosfets()
        await digipot.set_digipot(226)
        await mosfet.set_mosfet(MosfetPins.BOOSTCONVERTER, 1)
        #mosfetStatus = mosfet.get_mosfet_status(MosfetPins.BOOSTCONVERTER) # only works for gpio on raspberry pi
        #self.logger.info(f"{mosfetStatus}")
        await asyncio.sleep(10) 
        await mosfet.set_mosfet(MosfetPins.BOOSTCONVERTER, 0)
        await mosfet.set_mosfet(MosfetPins.PRECHARGE, val)
        await mosfet.set_mosfet(MosfetPins.NEGATIVE_RELAY, val)
        await asyncio.sleep(5)
        await mosfet.set_mosfet(MosfetPins.PRECHARGE, 0)
        await mosfet.set_mosfet(MosfetPins.POSITIVE_RELAY, val)
        
        
        # Decide next state
        if(self.discharging):
            self.state = States.DISCHARGING
        else:
            self.state = States.CHARGING

    async def _handle_discharging(self):
        self.logger.info("Discharging EV")

        if await pyplc.is_car_ListeningTCPmode:
            self.state = States.CAR_DISCONNECTED
        #TODO: can not currently use modbus so add logic 

        if self.current_KWH >= self.target_KWH:
            self.state = States.CHARGE_TARGET_REACHED
            
        
            
    async def _handle_charging(self):
        self.logger.info("Charging EV")

        self.logger.info(f"Charging {self.current_KWH:.2f}  {self.target_KWH} kWh")

        if self.current_KWH >= self.target_KWH:
            self.state = States.CHARGE_TARGET_REACHED

    async def _handle_error(self):
        self.logger.error("System error!")

        await digipot.set_digipot(0)
        await mosfet.disable_mosfets()
        
        await asyncio.sleep(5)
        self.state = States.IDLE


StateSystem = StateMachine()

