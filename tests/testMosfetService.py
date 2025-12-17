from pathlib import Path
import sys

# Add the parent directory to the path
parent_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(parent_dir))

from services.mosfet_controller import MosfetService
import asyncio

async def main():
    
    mosfet = MosfetService()
    
    #Sets mosfet on or off set_mosfet({PIN}, '{ON/OFF}')
    await mosfet.set_mosfet(11, 'OFF')
    await mosfet.set_mosfet(13, 'ON')

asyncio.run(main())
