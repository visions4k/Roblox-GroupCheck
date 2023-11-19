import json
import aiosonic
import time
from checker.cload import *
from checker.extras import *
from datetime import datetime
from colorama import Fore, Style

class Process:
    def __init__(self):
        self.client = aiosonic.HTTPClient()
        self.gidList = []
        self.rateLimit = antiRatelimit
        
    async def getGroups(self):
        r = await self.client.get(f"https://groups.roproxy.com/v2/users/{robloxUserID}/groups/roles")
        d = await r.json()
        groups = d.get('data', [])
        for group_data in groups:
            if group_data['role']['rank'] == 255:
                self.gidList.append(group_data['group']['id'])
        return self.gidList
    
    async def getInfo(self, group_id):
        try:
            response = await self.client.get(f"https://groups.roproxy.com/v1/groups/{group_id}")
            d = await response.json()
            groupName = d.get("name")
            groupMem = d.get("memberCount")
            return groupName, groupMem
        except Exception as e:
            return str(e)
        
    async def getFunds(self, GID):
        headers = {'Cookie': f".ROBLOSECURITY={robloxCookie}"}
        r = await self.client.get(f"https://economy.roblox.com/v1/groups/{GID}/currency", headers=headers)
        d = await r.json()
        print(d)
        return d.get("robux")
        
    
    async def getPFunds(self, GID):
        headers = {'Cookie': f".ROBLOSECURITY={robloxCookie}"}
        today = datetime.now().strftime("%Y-%m-%d")
        r = await self.client.get(f"https://economy.roblox.com/v1/groups/{GID}/revenue/summary/{today}", headers=headers)
        d = await r.json()
        return d.get("pendingRobux")
    
    async def getClothing(self, GID):
        try:
            r = await self.client.get(f"https://catalog.roblox.com/v1/search/items/details?Category=3&SortType=Relevance&CreatorTargetId={GID}&ResultsPerPage=100&CreatorType=2")
            d = await r.json()
            clothes = d.get("data", [])
            groupClothing = len(clothes)

            while True:
                if c := d.get("nextPageCursor"):
                    r = await self.client.get(f"https://catalog.roblox.com/v1/search/items/details?Category=3&SortType=Relevance&CreatorTargetId={GID}&ResultsPerPage=100&CreatorType=2&cursor={cursor}")
                    d = await r.json()
                    clothes = d.get("data", [])
                    groupClothing += len(clothes)
                else:
                    break

            return groupClothing
        except Exception:
            return 0
    
    async def getGames(self, GID):
        r = await self.client.get(f"https://games.roblox.com/v2/groups/{GID}/gamesV2?accessFilter=2&limit=100&sortOrder=Asc")
        d = await r.json()
        games = d.get("data", [])
        groupVisits = sum(game.get("placeVisits", 0) for game in games)
        groupGames = len(games)
        return groupGames, groupVisits
    
    
    async def shutdown(self):
        await self.client.shutdown()
        
    async def process_groups(self):
        gidList = await self.getGroups() 
        groups = {}
        
        startTimer = time.time()
        checking(f"CHECKING {len(gidList)} GROUPS | DELAY: {self.rateLimit} | WEBHOOK {'ENABLED' if discordEnabled else 'DISABLED'}")
        for i, gid in enumerate(gidList):
            groupName, groupMem = await self.getInfo(gid)
            groupFunds = await self.getFunds(gid)
            groupClothing = await self.getClothing(gid)
            groupPFunds = await self.getPFunds(gid)
            groupGames, groupVisits = await self.getGames(gid)
            groups[gid] = {
                "name": groupName,
                "members": groupMem,
                "clothing": groupClothing,
                "funds": groupFunds,
                "fundsPending": groupPFunds,
                "games": groupGames,
                "visits": groupVisits
            }
            if discordEnabled:
                await sendWebhook(gid, groupName, groupMem, groupFunds, groupClothing, groupPFunds, groupGames, groupVisits)
            successful(f"GROUP {gid} SUCCESSFUL")
            time.sleep(int(self.rateLimit))
        totalRobux = sum(group.get("funds", 0) + group.get("fundsPending", 0) for group in groups.values())
        totalGroups = len(groups)
        timeTook = time.time() - startTimer
        results = {
            "totalGroups": totalGroups,
            "totalRobux": totalRobux,
            "timeDuration": timeTook
        }
        output = {
            "groups": groups,
            "results": results
        }

        with open('output/groups.json', 'w') as f:
            json.dump(output, f, indent=4)

        await self.shutdown()
