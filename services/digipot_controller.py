import spidev
from ws.status_ws import manager

class DigipotService:
	def __init__(self):
		#Initialize spiDev
		self.spi = None
		self.spi = spidev.SpiDev()
		self.spi.open(0, 0)
		self.spi.max_speed_hz = 1000000
		
	async def set_digipot(self, value):
		try:
			#Changed Digipot register 0x00 via Spidev based on the value when calling the function
			self.spi.xfer2([0x00, self.value])

			#Print changes in the console
			print(f"[DigiPot] Set digipot to value: {value}")

			#Sent message to the websocket endpoint from the API
			await manager.broadcast("/box/digipot", {"voltage": value, "error": False})
		except Exception as e:
			#Print changes in the console when something goes wrong
			print(f"[DigiPot] Failed to set value: {e}")

			#Sent message to the websocket endpoint from the API when a problem occurs
			await manager.broadcast("/box/digipot", {"voltage": -1, "error": True})
			
	def stop(self):
		self._running = False
		if self.spi:
			self.spi.close()
