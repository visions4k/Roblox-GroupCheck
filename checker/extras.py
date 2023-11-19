import requests
import aiohttp
from checker.cload import *
from bs4 import BeautifulSoup
from colorama import Fore, Style

def successful(input):
    print(f"{Fore.GREEN}✓ {input}{Style.RESET_ALL}")
    
def checking(input):
    print(f"{Fore.YELLOW}► {input}{Style.RESET_ALL}")
    
    
async def sendWebhook(gid, group):
    groupName = group["name"]
    groupMem = group["members"]
    groupFunds = group["funds"]
    groupPFunds = group["fundsPending"]
    groupClothing = group["clothing"]
    groupGames = group["games"]
    groupVisits = group["visits"]

    embed = {
        "embeds": [
            {
                "title": groupName,
                "url": f"https://www.roblox.com/groups/{gid}/-",
                "description": f"> **Group ID:** `{gid}`\n> **Members:** `{groupMem}`\n> **Funds:** `{groupFunds}`\n> **Pending Funds:** `{groupPFunds}`\n> **Clothing Count:** `{groupClothing}`\n> **Total Games:** `{groupGames}`\n> **Total Visits:** `{groupVisits}`",
                "color": 0x2f3136
            }
        ]
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(webhookURL, json=embed) as response:
            return response.status
