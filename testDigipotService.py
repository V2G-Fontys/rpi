from services.digipot_controller import DigipotService
import asyncio

async def main():
    
    digipot = DigipotService()
    
    wiper_value = 100
    
    await digipot.set_digipot(wiper_value)

asyncio.run(main())
