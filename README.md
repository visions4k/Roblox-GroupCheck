
# Roblox Group Checker

This super faster roblox group checker utilizes the speeds of aiosonic to achieve the best speed possible. The group checker includes features such as anti ratelimit customization, and discord webhook support. When group checking is finished, it imports all the group and the groups information in a organized json file, which also includes the finished results (total groups, total robux, & time taken)


# Data Scraped
- Group Name
- Group Member Count
- Group Clothing Count
- Group Funds
- Group Pending Funds
- Group Game Count
- Group Games Visits Count

# Setup

The configuration file is config/config.json

"robloxUserID" & "robloxCookie" are required for checking groups

"antiRatelimit" is default "1", this adds a delay inbetween groups to help with ratelimits. 

in "Discord" > "isEnabled", this is default false, if set to true, it will be expecting a "webhookURL" which will send each group through the discord webhook. 

"fullAccuracy" will garuentee a successful request, meaning it will retry until successful. 

"customDetections" will allow you to change what you want to get. This can help with ratelimits and if your not interested in some of the groups information. 

"outputFilter" will only put groups in output/groups.json if the members are more then 100, if it has any funds/pending funds, and if the clothing is more then 25. 

# Start

Run python start.py when the config file is configured.






## Examples
Console-

![Console](https://cdn.discordapp.com/attachments/1172623368994955354/1175634122379632670/image.png?ex=656bf199&is=65597c99&hm=dd9d1470191b507aa24def8b960b3e6b00f0bd7d093924491a3bcd7d5ac830f2&)

Group Data-

![Group Data](https://cdn.discordapp.com/attachments/1172623368994955354/1175634284439158845/image.png?ex=656bf1bf&is=65597cbf&hm=24444279b9fa7fae8f9c665323dc7afe7569aa4de9a2504050e97f8036b405e9&)

Result Data-

![Results Data](https://cdn.discordapp.com/attachments/1172623368994955354/1175645379044311091/image.png?ex=656bfc14&is=65598714&hm=3cc7d8acd084a269be65ef9bdd4197d91ca0503c60bf6d2fbd2b3329b4df4e3c&)

Discord Embed-

![Discord Embed](https://cdn.discordapp.com/attachments/1172623368994955354/1175633667209560174/image.png?ex=656bf12c&is=65597c2c&hm=611843008b6fe4c3d1df5dca43f9b912c6d3ad19ee363e499a600963730df6be&)


##  Changelog

+ 11/18/2023 - Released & Fixes
  - Released publicly
  - Bug fixes (decoding issues)
  - Speed increase (made concurrent)
  - Error handling (will ignore errors, and set info as "error")
  - Error counting

+ 11/19/2023 - 
  - Speed increase, help w/ ratelimits (removed unnessary req)
  - Ratelimit counting
 
+ 11/20/2023
   - Full Accuracy option added (will retry all ratelimited request, ensuring for a 100% ok response)
   - Custom detections option added (can choose what to request, can help with ratelimits, or if your only interested in one asset of groups)
   - Output filter option added (will only show groups in output if the group members are more then 100, funds are more then 0, pending funds more then 0, and clothing more then 25)


## To do (coming soon) 

+ Proxy support (w/ proxychecker & scraper)
+ Interchangable http clients (between aiohttp & aiosonic)
+ Multiple account queue
+ Discord bot client w/ commands (optional)
+ Improvement in UI


## Thanks

Concept & Idea from [lad / novak](https://github.com/ladiscool)

Bypass code from [xolo](https://github.com/efenatuyo)
