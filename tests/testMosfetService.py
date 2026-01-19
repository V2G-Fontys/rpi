from pathlib import Path
import sys

# Add the parent directory to the path
parent_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(parent_dir))

from services.mosfet_controller import *
import asyncio

async def main():
    
    mosfet = MosfetService()
    
    #Sets mosfet on or off set_mosfet({PIN}, '{1/0}')
    
    await mosfet.set_mosfet(MosfetPins.BOOSTCONVERTER, 1)
    await mosfet.set_mosfet(MosfetPins.PRECHARGE, 0)
    await mosfet.set_mosfet(MosfetPins.POSITIVE_RELAY, 0)
    await mosfet.set_mosfet(MosfetPins.NEGATIVE_RELAY, 0)
    
    await asyncio.sleep(2)
    #await mosfet.disable_mosfets()

asyncio.run(main())
