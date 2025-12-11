from pathlib import Path
import sys

# Add the parent directory to the path
parent_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(parent_dir))

from services.digipot_controller import DigipotService
import asyncio

async def main():
    
    digipot = DigipotService()
    
    wiper_value = 100
    
    await digipot.set_digipot(wiper_value)

asyncio.run(main())
