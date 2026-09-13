# Gorilla Tag Update Tracker
Source code for "Gorilla Tag Updates" bot

<img width="375" height="258" alt="image" src="https://github.com/user-attachments/assets/87a6dc46-a68d-4771-b757-d02e91aed9be" />

## Features
- `/set_channel <text channel>`: Adds a channel to the update announcement queue, so it will receive a message when Gorilla Tag updates
- `/del_channel <text channel>`: Deletes a channel from the update announcement queue.
- `/current`: Retrieves the current version information including Unity version, game version, and SteamDB changelog.

## Setup
Setup is easy minus a couple strange gimmicks the Steam library has. Install Python and Pip3 and then run the following:
```
git clone https://github.com/sirkingbinx/gorilla-tag-update-tracker
cd gorilla-tag-update-tracker
pip install -r requirements.txt
```

<!-- requirements fix should work fine now -->

If you are ready to deploy the bot, make sure the user running it has read permissions for the directory holding SteamCMD, and read/write permissions for the current directory, then create a .env file with the following:
```
DISCORD_BOT_TOKEN={bot token here}
STEAMCMD_FOLDER={folder holding steamcmd.exe / steamcmd)
STEAMCMD_PATH=absolute path to steamcmd.exe / steamcmd
STEAMCMD_CACHE_USERNAME=(your steam username that steamcmd has cached credentials for, if you haven't used steamcmd before do .\steamcmd.exe +login {username}
```
