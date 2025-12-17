import RPi.GPIO as GPIO
from enum import Enum
#from ws.status_ws import manager

State = bool

class MosfetPins(Enum):
	BOOSTCONVERTERS = 29
	PRECHARGE = 31
	POSITIVE_RELAY = 33
	NEGATIVE_RELAY = 32
	
class MosfetService:
	def __init__(self):
		GPIO.setmode(GPIO.BOARD)
		GPIO.setwarnings(False)
		
		for Mosfet in MosfetPins:
			GPIO.setup(Mosfet.value, GPIO.OUT)
		
	async def set_mosfet(self, GPIOPin, State):
		try:		
			if State:
				GPIO.output(GPIOPin, GPIO.HIGH)
			else:
				GPIO.output(GPIOPin, GPIO.LOW)

			#Print changes in the console
			print(f"[Mosfet] Set mosfet({GPIOPin}) to {State}")

			#Send message to the websocket endpoint from the API
			#await manager.broadcast("mosfet", {"GPIOPin": GPIOPin, "State": State, "error": False})
		except Exception as e:
			#Print changes in the console when something goes wrong
			print(f"[Mosfet] Failed to set value: {e}")

			#Send message to the websocket endpoint from the API when a problem occurs
			#await manager.broadcast("mosfet", {"GPIOPin": GPIOPin, "State": State, "error": True})
	
	async def disable_mosfets(self):
		try:
			for mosfet in MosfetPins:
				GPIO.output(mosfet.value, GPIO.LOW)
		except Exception as e:
			#Print changes in the console when something goes wrong
			print(f"[Mosfet] Failed to disable mosfet: {e}")

			#Send message to the websocket endpoint from the API when a problem occurs
			#await manager.broadcast("mosfet", {"GPIOPin": GPIOPin, "State": State, "error": True})
	def stop(self):
		GPIO.cleanup()
		
mosfet = MosfetService()
