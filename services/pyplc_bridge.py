import asyncio
import os
from core.http_requests import HTTPRequests
from core.logger import get_logger

PYPLC_SCRIPT = os.path.expanduser("~/V2G/pyPlc/pyplc.py")
PYPLC_CONFIG = os.path.expanduser("~/V2G/pyPlc/pyplc.ini")

class PyPlcService:
    def __init__(self, send_to_backend_callback=None, backend_url="http://localhost:8080/api/ev-status"):
        self.logger = get_logger("PyPlcService")
        self._running = True
        self.http = HTTPRequests(backend_url)
        self.send_to_backend = send_to_backend_callback or self._send_to_backend

    async def run(self):
        cmd = ["sudo", "python3", PYPLC_SCRIPT, PYPLC_CONFIG]
        self.logger.info(f"Starting pyPLC subprocess: {' '.join(cmd)}")
        proc = await asyncio.create_subprocess_exec(*cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.STDOUT)
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

    async def _send_to_backend(self, data):
        await self.http.post("/api/ev-status", data)

    def stop(self):
        self._running = False

if __name__ == "__main__":
    service = PyPlcService()
    asyncio.run(service.run())