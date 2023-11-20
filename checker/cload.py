import json

with open('config/config.json', 'r') as f:
    data = json.load(f)

autoScrape = False
proxyEnabled = False
robloxUserID = data['Config']['robloxUserID']
robloxCookie =  data['Config']['robloxCookie']
# proxyEnabled = data['Checker']['Proxy']['isEnabled']
# autoScrape = data['Checker']['Proxy']['autoScrape']
# timeoutC = data['Checker']['Proxy']['timeout']
antiRatelimit = data['Checker']['antiRatelimit']
fullAccuracy = data['Checker']['fullAccuracy']
isCustomEnabled = data['Checker']['customDetections']['isEnabled']
isClothingEnabled = data['Checker']['customDetections']['clothing']
isFundsEnabled = data['Checker']['customDetections']['funds']
isPFundsEnabled = data['Checker']['customDetections']['fundsPending']
isGameEnabled = data['Checker']['customDetections']['gameInfo']
outputFilter = data['Checker']['outputFilter']
discordEnabled = data['Discord']['isEnabled']
webhookURL = data['Discord']['webhookURL']
proxyList = []
