# Gorilla Tag Update Tracker
Source code for "Gorilla Tag Updates" bot

<img width="601" height="259" alt="image" src="https://github.com/user-attachments/assets/5f73cd0f-cb4c-4978-ac05-2c4f313126f5" />

## Setup
Setup is easy minus a couple strange gimmicks the Steam library has. Install Python and Pip3 and then run the following:
```
git clone https://github.com/sirkingbinx/gorilla-tag-update-tracker
cd gorilla-tag-update-tracker
pip install -r requirements.txt

# fix steam
pip uninstall eventemitter
pip install -U "steam[client]"
```

If you are ready to deploy the bot, make sure the user running it has R permissions for the directory holding SteamCMD, and R/W permissions for the current directory, then create a .env file with the following:
```
DISCORD_BOT_TOKEN={bot token here}
STEAMCMD_FOLDER={folder holding steamcmd.exe / steamcmd)
STEAMCMD_PATH=absolute path to steamcmd.exe / steamcmd
STEAMCMD_CACHE_USERNAME=(your steam username that steamcmd has cached credentials for, if you haven't used steamcmd before do .\steamcmd.exe +login {username}
```
