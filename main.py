# Gorilla Tag Update Tracker
import sys

from discord.ext import commands, tasks
from discord import app_commands
from dotenv import load_dotenv
from steam.client import SteamClient

import discord
import os

import db
import msg
import vextract

load_dotenv() # .env

TOKEN = os.getenv("DISCORD_BOT_TOKEN")
GORILLA_TAG_APP_ID = 1533390

if TOKEN is None:
    print("Please set DISCORD_BOT_TOKEN environment variable (we support .env files)")
    sys.exit(1)

intents = discord.Intents.default()

def get_latest_build_id(app_id):
    steam_client = SteamClient()

    steam_client.anonymous_login()

    try:
        product_info = steam_client.get_product_info(apps=[app_id])

        apps_data = product_info.get("apps", {})
        game_data = apps_data.get(app_id, {})
        depots = game_data.get("depots", {})
        branches = depots.get("branches", {})
        public_branch = branches.get("public", {})

        build_id = public_branch.get("buildid")

        return build_id
    except Exception as e:
        print(f"err fetching build id: {e}")
        return None
    finally:
        steam_client.disconnect()

last_build_id = None
last_version_id = "1.1.0"
last_unity_ver_id = "0.0.0f"

def get_init_build_id():
    global last_build_id
    global last_version_id
    global last_unity_ver_id

    last_build_id = get_latest_build_id(GORILLA_TAG_APP_ID)
    last_version_data = vextract.get_version()
    last_version_id = last_version_data.get("gameVersion")
    last_unity_ver_id = last_version_data.get("unityVersion")

    print("       Initial build report:       ")
    print(f"Build ID:      {last_build_id}")
    print(f"GT Version:    {last_version_id}")
    print(f"Unity Version: {last_unity_ver_id}")

    if not last_build_id:
        print("no init Build ID. check API connection")
        sys.exit(0)

@tasks.loop(seconds=300)
async def check_for_updates():
    global last_build_id
    global last_version_id
    global last_unity_ver_id

    current_build_id = get_latest_build_id(GORILLA_TAG_APP_ID)

    if current_build_id and current_build_id != last_build_id:
        current_version_info = vextract.get_version()
        current_version_id = current_version_info.get("gameVersion")
        current_unity_ver = current_version_info.get("unityVersion")

        await msg.dispatch_updates(client, current_build_id, last_version_id, current_version_id, last_unity_ver_id, current_unity_ver)

        last_build_id = current_build_id
        last_version_id = current_version_id
        last_unity_ver_id = current_unity_ver

client = commands.Bot(command_prefix="!", intents=intents)

@client.tree.command(name="set_channel", description="Set the channel that the update tracker will post announcements in")
@app_commands.describe(target_channel="The channel you want to send the message to")
@app_commands.checks.has_permissions(manage_channels=True, administrator=True)
async def set_channel(interaction: discord.Interaction, target_channel: discord.TextChannel):
    db.add_channel(target_channel.id)
    await msg.send_welcome_message(client, target_channel.id, last_build_id, last_unity_ver_id, last_version_id)
    await interaction.response.send_message(f"Now routing messages to {target_channel.mention}")

@client.tree.command(name="del_channel", description="Remove your channels from the update tracker")
@app_commands.checks.has_permissions(manage_channels=True, administrator=True)
async def del_channel(interaction: discord.Interaction):
    await interaction.response.send_message(f"Deleted announcements for channel")

@client.tree.command(name="gt_ping", description="Test connectivity")
async def gt_ping(interaction: discord.Interaction):
    await interaction.response.send_message(f"Pong in {round(client.latency * 1000)}ms")

@client.event
async def on_ready():
    print(f"Auth as {client.user}")
    get_init_build_id()

    check_for_updates.start()

    try:
        await client.tree.sync()
    except Exception as e:
        print(f"could not sync commands: {e}")

client.run(TOKEN)