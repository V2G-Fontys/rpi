import RPi.GPIO as GPIO
from enum import Enum
#from ws.status_ws import manager

class State(Enum):
	ON = 1
	OFF = 0
	
class MosfetService:
	def __init__(self):
		GPIO.setmode(GPIO.BOARD)
	async def set_mosfet(self, GPIOPin, State):
		try:
			GPIO.setup(GPIOPin, GPIO.OUT)
			
			if (State == 'ON'):
				GPIO.output(GPIOPin, GPIO.HIGH)
			elif (State == 'OFF'):
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
			
	def stop(self):
		GPIO.cleanup()
