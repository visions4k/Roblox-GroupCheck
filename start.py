import asyncio
from checker.process import Process
from checker.bypass import Bypass
from checker.cload import *

async def start():
    if proxyEnabled:
        beforeCookie = robloxCookie
        bypass = Bypass(beforeCookie)
        bypassedCookie = bypass.start_process()
        process = Process(bypassedCookie)
    else:
        process = Process(robloxCookie)
    await process.processGroups()

if __name__ == "__main__":
    asyncio.run(start())
