import json
import aiosonic
import asyncio
import time
import random
from checker.cload import *
from checker.extras import *
from datetime import datetime
from yarl import URL

class Process:
    def __init__(self, bypassedCookie):
        self.gidList = []
        self.groupInfoDict = {}
        self.rateLimit = antiRatelimit
        self.cookie = bypassedCookie
        self.proxyList = loadProxies()
        self.client = aiosonic.HTTPClient()
        self.errors = 0
        self.errorsRL = 0
        

    async def getRequest(self, url, headers=None):
        while proxyEnabled:
            proxy = URL(f"http://{random.choice(self.proxyList)}")
            print("not avaliable yet")
        else:
            for _ in range(3):
                try:
                    r = await self.client.get(url, headers=headers)
                    if r.status_code == 200:
                        return await r.json()
                    elif r.status_code == 429:
                        self.errorsRL += 1
                        break 
                    else:
                        self.errors += 1
                except Exception as e:
                    self.errors += 1
            return None


    async def getGroups(self):
        url = f"https://groups.roblox.com/v2/users/{robloxUserID}/groups/roles"
        d = await self.getRequest(url)
        groups = d.get('data', [])
        for group_data in groups:
            if group_data['role']['rank'] == 255:
                gid = group_data['group']['id']
                groupName = group_data['group']['name']
                groupMem = group_data['group']['memberCount']
                self.gidList.append(gid)
                self.groupInfoDict[gid] = (groupName, groupMem)
        return self.gidList


    async def getFunds(self, gid):
        try:
            headers = {'Cookie': f".ROBLOSECURITY={self.cookie}"}
            url = f"https://economy.roblox.com/v1/groups/{gid}/currency"
            d = await self.getRequest(url, headers=headers)
            return d.get("robux")
        except Exception as e:
            self.errors += 1
            return "error"

    async def getPFunds(self, gid):
        try:
            headers = {'Cookie': f".ROBLOSECURITY={self.cookie}"}
            today = datetime.now().strftime("%Y-%m-%d")
            url = f"https://economy.roblox.com/v1/groups/{gid}/revenue/summary/{today}"
            d = await self.getRequest(url, headers=headers)
            return d.get("pendingRobux")
        except Exception as e:
            self.errors += 1
            return "error"

    async def getClothing(self, gid):
        try:
            url = f"https://catalog.roblox.com/v1/search/items/details?Category=3&SortType=Relevance&CreatorTargetId={gid}&ResultsPerPage=100&CreatorType=2"
            d = await self.getRequest(url)
            clothes = d.get("data", [])
            groupClothing = len(clothes)

            while True:
                if c := d.get("nextPageCursor"):
                    url = f"https://catalog.roblox.com/v1/search/items/details?Category=3&SortType=Relevance&CreatorTargetId={gid}&ResultsPerPage=100&CreatorType=2&cursor={c}"
                    d = await self.getRequest(url)
                    clothes = d.get("data", [])
                    groupClothing += len(clothes)
                else:
                    break

            return groupClothing
        except Exception as e:
            self.errors += 1
            return "error"

    async def getGames(self, gid):
        try:
            url = f"https://games.roblox.com/v2/groups/{gid}/gamesV2?accessFilter=2&limit=100&sortOrder=Asc"
            d = await self.getRequest(url)
            games = d.get("data", [])
            groupVisits = sum(game.get("placeVisits", 0) for game in games)
            groupGames = len(games)
            return groupGames, groupVisits
        except Exception as e:
            self.errors += 1
            return "error", "error"

    async def shutdown(self):
        await self.client.shutdown() 

    async def processGroup(self, gid):
        groupInfo = self.groupInfoDict.get(gid, ("error", "error"))
        groupName, groupMem = groupInfo
        groupFunds = await self.getFunds(gid)
        groupClothing = await self.getClothing(gid)
        groupPFunds = await self.getPFunds(gid)
        groupGames, groupVisits = await self.getGames(gid)
        return gid, {
            "name": groupName,
            "members": groupMem,
            "clothing": groupClothing,
            "funds": groupFunds,
            "fundsPending": groupPFunds,
            "games": groupGames,
            "visits": groupVisits
        }

    async def processGroups(self):
        statG("STARTING")
        gidList = await self.getGroups() 
        groups = {}

        startTimer = time.time()
        statG(f"CHECKING {len(gidList)} GROUPS | DELAY: {self.rateLimit} | WEBHOOK {'ENABLED' if discordEnabled else 'DISABLED'}")
        tasks = [self.processGroup(gid) for gid in gidList]
        for future in asyncio.as_completed(tasks):
            gid, group = await future
            groups[gid] = group
            if discordEnabled:
                await sendWebhook(gid, **group)
            checkedG(f"GROUP {gid} SUCCESSFUL")
            time.sleep(int(self.rateLimit))
        totalRobux = sum(
            group.get("funds", 0) + group.get("fundsPending", 0)
            for group in groups.values()
            if isinstance(group.get("funds", 0), int) and isinstance(group.get("fundsPending", 0), int)
        )
        totalGroups = len(groups)
        timeTook = time.time() - startTimer
        totalErrors = self.errors + self.errorsRL
        results = {
            "totalGroups": totalGroups,
            "totalRobux": totalRobux,
            "timeDuration": timeTook,
            "reqErrors": self.errors,
            "ratelimitErrors": self.errorsRL,
        }
        output = {
            "groups": groups,
            "results": results
        }

        with open('output/groups.json', 'w') as f:
            json.dump(output, f, indent=4)
        doneG(f"FINISHED | {totalGroups} GROUPS | {totalRobux} ROBUX | {timeTook} SECONDS | {totalErrors} ERRORS\nCHECK output/groups.json FOR RESULTS")
        await self.shutdown()
        
