import spidev
import time
from ws.status_ws import manager

class DigipotService:
	def __init__(self):
		self.spi = None
		self.spi = spidev.SpiDev()
		self.spi.open(0, 0)
		self.spi.max_speed_hz = 1000000
		
	async def set_digipot(self, value):
		try:
			self.spi.xfer2([0x00, self.value])
			print(f"[DigiPot] Set digipot to value: {value}")
			await manager.broadcast("/box/digipot", {"voltage": value, "error": False})
		except Exception as e:
			print(f"[DigiPot] Failed to set value: {e}")
			await manager.broadcast("/box/digipot", {"voltage": -1, "error": True})
			
	def stop(self):
		self._running = False
		if self.spi:
			self.spi.close()
