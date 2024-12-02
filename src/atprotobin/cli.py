import os
import asyncio

import uvicorn

async def async_main():
    config = uvicorn.Config(
        "atprotobin.server:app",
        port=int(os.environ.get("PORT", "8000")),
        log_level="debug",
    )
    server = uvicorn.Server(config)
    await server.serve()

def main() -> None:
    asyncio.run(async_main())
