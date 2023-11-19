import requests
import aiohttp
from checker.cload import *
from bs4 import BeautifulSoup
from colorama import Fore, Style

    
psUrl = [  
    'https://api.proxyscrape.com/v2/?request=displayproxies&protocol=https&timeout=1000&country=all&ssl=all&anonymity=all',      
]

def loadProxies():
    if not autoScrape:
        with open('config/proxies.txt') as f:
            proxyList.extend(line.strip() for line in f if line.strip())
    else:
        proxyList.clear()
        for url in psUrl:
            r = requests.get(url)
            soup = BeautifulSoup(r.text, 'html.parser')
            sproxies = {
                line.strip()
                for line in soup.get_text().splitlines()
                if line.strip()
            }
            ndproxies = [proxy for proxy in sproxies if proxy not in proxyList]
            proxyList.extend(ndproxies)
    return proxyList

def checkedG(input):
    print(f"{Fore.BLUE}★ {input}{Style.RESET_ALL}")
    
def statG(input):
    print(f"{Fore.YELLOW}► {input}{Style.RESET_ALL}")
    
def doneG(input):
    print(f"{Fore.GREEN}► {input}{Style.RESET_ALL}")
    
    
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
