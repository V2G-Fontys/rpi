import asyncio
from pymodbus.client import ModbusSerialClient
from pymodbus.exceptions import ModbusIOException
from serial.tools import list_ports
from core.logger import get_logger
from core.http_requests import HTTPRequests

# ---- Configuration ----
MODBUS_ID = 1

# Register map (adjust according to inverter spec)
REG_MODE = 0x3000             # 0 = idle, 1 = charge, 2 = discharge
REG_DISCHARGE_POWER = 0x3002  # Value in watts
REG_BATT_VOLTAGE = 0x3100     # Scaled: /10.0
REG_BATT_CURRENT = 0x3101     # Scaled: /10.0

BAUDRATE = 9600
TIMEOUT = 1
PARITY = 'N'
STOPBITS = 1
BYTESIZE = 8

# Backend (optional)
BACKEND_URL = "http://localhost:8080/api/inverter-status"  # Adjust as needed


class ModbusService:
    def __init__(self, backend_url=BACKEND_URL):
        self.logger = get_logger("ModbusService")
        self._running = True
        self.http = HTTPRequests(backend_url)

    async def run(self):
        port = self.find_serial_port()
        if not port:
            self.logger.error("No Modbus USB adapter found.")
            return
        client = self.init_modbus(port)
        client.slave = MODBUS_ID
        if not client.connect():
            self.logger.error(f"Could not connect to inverter on {port}")
            return
        self.logger.info(f"Connected to inverter on {port}")
        self.set_discharge_power(client, 3000)
        self.set_mode(client, 2)
        try:
            while self._running:
                voltage = self.read_scaled_register(client, REG_BATT_VOLTAGE)
                current = self.read_scaled_register(client, REG_BATT_CURRENT)
                if voltage is not None and current is not None:
                    self.logger.info(f"[Inverter] Voltage: {voltage:.1f} V | Current: {current:.1f} A")
                    await self.send_to_backend(voltage, current)
                await asyncio.sleep(5)
        except Exception as e:
            self.logger.error(f"Modbus error: {e}")
        finally:
            self.set_mode(client, 0)
            client.close()
            self.logger.info("Modbus client closed.")

    def find_serial_port(self):
        ports = list_ports.comports()
        for port in ports:
            if "USB" in port.device:
                return port.device
        return None

    def init_modbus(self, port):
        return ModbusSerialClient(
            port=port,
            baudrate=BAUDRATE,
            stopbits=STOPBITS,
            bytesize=BYTESIZE,
            parity=PARITY,
            timeout=TIMEOUT
        )

    def read_scaled_register(self, client, reg):
        try:
            rr = client.read_holding_registers(reg, 1)
            if not rr.isError():
                return rr.registers[0] / 10.0
            else:
                self.logger.error(f"[Modbus] Error reading register {reg}")
        except ModbusIOException as e:
            self.logger.error(f"[Modbus] IOError on register {reg}: {e}")
        return None

    def set_mode(self, client, mode):
        try:
            client.write_register(REG_MODE, mode)
            self.logger.info(f"[Modbus] Set mode to {mode}")
        except Exception as e:
            self.logger.error(f"[Modbus] Failed to set mode: {e}")

    def set_discharge_power(self, client, watts):
        try:
            client.write_register(REG_DISCHARGE_POWER, watts)
            self.logger.info(f"[Modbus] Set discharge power to {watts}W")
        except Exception as e:
            self.logger.error(f"[Modbus] Failed to set power: {e}")

    async def send_to_backend(self, voltage, current):
        await self.http.post("/api/inverter-status", {"voltage": voltage, "current": current})

    def stop(self):
        self._running = False


if __name__ == "__main__":
    service = ModbusService()
    asyncio.run(service.run())
