import asyncio
import os
from services.slac_data import SlData
#from core.http_requests import HTTPRequests
from core.logger import get_logger



# this class boots the PyPlc application, and manages the Application data 
class PyPlcService:
    def __init__(self):
        self.logger = get_logger("PyPlcService")
        self._running = True
    
    async def run(self):
        
        pyplc_dir = os.path.expanduser("~/V2G/pyPlc") # the directory the files are located
        cmd = ["sudo", "python3", "-u","pyPlc.py", "pyPlc.ini"]  # commands to run
        
        self.logger.info(f"Starting pyPLC subprocess in {pyplc_dir}: {' '.join(cmd)}")
        #execute commands
        proc = await asyncio.create_subprocess_exec(
        *cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
        cwd=pyplc_dir  # this leads us to the working directory described above
        )
        
        try:
            while self._running:
                line = await proc.stdout.readline()
                if not line:
                    break
                decoded = line.decode().strip()
                self.logger.info(f"[pyPLC] {decoded}")
                data = self.parse_pyplc_line(decoded)
                if data:
                    await self.send_to_backend({"ev_status": data})
        except Exception as e:
            self.logger.error(f"pyPLC/OpenV2G error: {e}")
        finally:
            if proc.returncode is None:
                proc.terminate()
                await proc.wait()
            self.logger.info("pyPLC subprocess terminated.")

    def parse_pyplc_line(self, line):
        if "EVSEStatus" in line:
            try:
                parts = line.strip().split(":")[1].split(",")
                voltage = float(parts[0].split("=")[1].replace("V", "").strip())
                current = float(parts[1].split("=")[1].replace("A", "").strip())
                return {"voltage": voltage, "current": current}
            except Exception as e:
                self.logger.error(f"Failed to parse: {line} -> {e}")
        return None
        
    async def is_car_connected(self):
        return S
                
    def stop(self):
        self._running = False

pyplc = PyPlcService()

