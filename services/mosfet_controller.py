import RPi.GPIO as GPIO
from enum import IntEnum
import serial
import logging
#from ws.status_ws import manager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("MosfetService")

#the pins used on the arduino , if you need to change the pins do that here
class MosfetPins(IntEnum):
	BOOSTCONVERTER = 10
	PRECHARGE = 11
	POSITIVE_RELAY = 12
	NEGATIVE_RELAY = 13
	
class MosfetService:
	def __init__(self):
		GPIO.setmode(GPIO.BOARD)
		GPIO.setwarnings(False) #if true gives extra error codes like this pin is already in use
		try:
			#find if arduino is connected by ls /dev , they show up as ttyACMx
			#self.ser = serial.Serial('/dev/ttyACM1', 9600, timeout=1) #comment this out if you do not need arduino for mosfets
			logger.info("Serial port arduino opened")
		except serial.SerialException as e:
			logger.error(f"Failed to open serial: {e}")
			logger.info("If you didnt connect an arduino for mosfets you can comment this out")
			exit()
			
		for mosfet in MosfetPins:
			GPIO.setup(mosfet.value, GPIO.OUT, initial=GPIO.LOW)
			
	#main function to turn on gpio pins on rpi
	async def set_mosfet(self, GPIOPin: MosfetPins, state: bool):
		try:		
			if state:
				GPIO.output(GPIOPin.value, GPIO.HIGH)
			else:
				GPIO.output(GPIOPin.value, GPIO.LOW)

			#Print changes in the console
			logger.info(f"[Mosfet] Set mosfet({GPIOPin}) to {state}")

		except Exception as e:
			#Print changes in the console when something goes wrong
			logger.error(f"[Mosfet] Failed to set value: {e}")
				
	#this function is only used in the case that you have mosfets that switch on around 5v
	#you can test it on an arduino(uses 5v for example instead of rpi's 3.3v, which is not enough for some mosfets)
	async def set_arduino(self, pin, state = bool):
		print(f"{str(pin)},{str(state)}")
		try:
			#TODO: do two way communication to see if arduino is connected
			self.ser.write(chr(pin).encode('utf-8')) 
			self.ser.write(chr(state).encode('utf-8')) 
		except Exception as e:
			logger.error(f"[Mosfet]Failed to Set mosfet({GPIOPin}) to {state}")
			print(e)
			
	#this function is used to disable all the mosfets to off. only works with raspberry pi GPIO
	async def disable_mosfets(self):
		try:
			for mosfet in MosfetPins:
				GPIO.output(mosfet.value, GPIO.LOW)
		except Exception as e:
			#Print changes in the console when something goes wrong
			logger.error(f"[Mosfet] Failed to disable mosfet: {e}")
			
	#only works if raspberry pi GPIO pins are used
	def get_mosfet_status(self, GPIOPin):
		return GPIO.input(GPIOPin)
		
	#cleans up the gpio pins
	def stop(self):
		GPIO.cleanup()
		
mosfet = MosfetService()
