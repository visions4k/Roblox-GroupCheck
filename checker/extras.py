import requests
import aiohttp
from checker.cload import *
from bs4 import BeautifulSoup
from colorama import Fore, Style

def successful(input):
    print(f"{Fore.GREEN}✓ {input}{Style.RESET_ALL}")
    
def checking(input):
    print(f"{Fore.YELLOW}► {input}{Style.RESET_ALL}")
    
    
async def sendWebhook(gid, name, members, clothing, funds, fundsPending, games, visits):
    embed = {
        "embeds": [
            {
                "title": name,
                "url": f"https://www.roblox.com/groups/{gid}/-",
                "description": f"> **Group ID:** `{gid}`\n> **Members:** `{members}`\n> **Funds:** `{funds}`\n> **Pending Funds:** `{fundsPending}`\n> **Clothing Count:** `{clothing}`\n> **Total Games:** `{games}`\n> **Total Visits:** `{visits}`",
                "color": 0x2f3136
            }
        ]
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(webhookURL, json=embed) as response:
            return response.status
