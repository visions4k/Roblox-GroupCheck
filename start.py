import asyncio
from checker.process import Process

async def start():
    process = Process()
    await process.processGroups()

if __name__ == "__main__":
    asyncio.run(start())
