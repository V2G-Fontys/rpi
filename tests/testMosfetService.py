from pathlib import Path
import sys

# Add the parent directory to the path
parent_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(parent_dir))

from services.mosfet_controller import MosfetService, MosfetPins
import asyncio

async def main():
    
    mosfet = MosfetService()
    
    #Sets mosfet on or off set_mosfet({PIN}, '{1/0}')
    await mosfet.set_arduino(MosfetPins.BOOSTCONVERTER, 0)
    #await mosfet.set_arduino(MosfetPins.PRECHARGE.value, 0)
    #await mosfet.set_arduino(MosfetPins.POSITIVE_RELAY.value, 0)
    #await mosfet.set_arduino(MosfetPins.NEGATIVE_RELAY.value, 0)

asyncio.run(main())
