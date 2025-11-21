import spidev
import time
from core.logger import get_logger

class DigipotService:
	def __init__(self):
		self.logger = get_logger("DigipotService")  # Initialize logger
		self.spi = None
	def set_digipot(self, value):
		try:
			self.value = value
			self.spi = spidev.SpiDev()
			self.spi.open(0, 0)
			self.spi.max_speed_hz = 1000000
			self.spi.xfer2([0x00, self.value])
			self.logger.info(f"[DigiPot] Set digipot to value: {value}")
		except Exception as e:
			self.logger.error(f"[DigiPot] Failed to set value: {e}")
		finally:
			if self.spi:
				self.spi.close()
			
	def stop(self):
		self._running = False

