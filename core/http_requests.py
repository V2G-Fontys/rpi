import aiohttp
from core.logger import get_logger

logger = get_logger("HTTPRequests")

class HTTPRequests:
    def __init__(self, backend_url):
        self.backend_url = backend_url

    async def post(self, endpoint: str, data: dict):
        url = f"{self.backend_url.rstrip('/')}/{endpoint.lstrip('/')}"
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=data) as resp:
                    text = await resp.text()
                    logger.info(f"POST {url} - Status: {resp.status}, Response: {text}")
                    return resp.status, text
        except Exception as e:
            logger.error(f"HTTP POST to {url} failed: {e}")
            return None, str(e)
