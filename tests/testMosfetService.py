from pathlib import Path
import sys

# Add the parent directory to the path
parent_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(parent_dir))

boostconverter = 11
precharge = 33
relayHV = 29
relayLV = 31

from services.mosfet_controller import MosfetService
import asyncio

async def main():
    
    mosfet = MosfetService()
    
    #Sets mosfet on or off set_mosfet({PIN}, '{1/0}t')

    await mosfet.set_mosfet(boostconverter, 0)
    await mosfet.set_mosfet(precharge, 0)
    await mosfet.set_mosfet(relayHV, 0)
    await mosfet.set_mosfet(relayLV, 0)

asyncio.run(main())
