import json

with open('config/config.json', 'r') as f:
    data = json.load(f)

robloxUserID = data['Config']['robloxUserID']
robloxCookie =  data['Config']['robloxCookie']
proxyEnabled = data['Checker']['Proxy']['isEnabled']
autoScrape = data['Checker']['Proxy']['autoScrape']
timeoutC = data['Checker']['Proxy']['timeout']
antiRatelimit = data['Checker']['antiRatelimit']
discordEnabled = data['Discord']['isEnabled']
webhookURL = data['Discord']['webhookURL']
proxyList = []
