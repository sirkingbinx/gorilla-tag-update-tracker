import discord
from datetime import datetime
from discord import Client

import db


async def send_welcome_message(client: Client, channel_id, build_id, build_version, unity_ver):
    embed = discord.Embed(title="Welcome",
                          description="You are now subscribed to Gorilla Tag update notifications. If this was not intended, run /del_channel with *Manage Channels* permissions.",
                          timestamp=datetime.now())

    steamdb_url = f"https://steamdb.info/patchnotes/{build_id}/"

    embed.add_field(name="Unity Version",
                    value=f"`{unity_ver}`",
                    inline=True)
    embed.add_field(name="Game Version",
                    value=f"`{build_version}`",
                    inline=True)
    embed.add_field(name="SteamDB",
                    value=steamdb_url,
                    inline=False)

    embed.set_footer(text="Gorilla Tag Update Tracker")

    channel = client.get_channel(channel_id)

    if isinstance(channel, discord.TextChannel):
        await channel.send(embed=embed)

async def send_update_message(client: Client, channel_id, build_id, prev_version, new_version, last_unity_ver, new_unity_ver):
    steamdb_url = f"https://steamdb.info/patchnotes/{build_id}/"

    embed = discord.Embed(title="Gorilla Tag Update",
                          url=steamdb_url,
                          description="Gorilla Tag has updated.",
                          timestamp=datetime.now())

    embed.add_field(name="Previous Version",
                    value=f"`{prev_version}`",
                    inline=True)
    embed.add_field(name="Current Version",
                    value=f"`{new_version}`",
                    inline=True)
    embed.add_field(name="SteamDB",
                    value=steamdb_url,
                    inline=False)

    embed.set_footer(text="Gorilla Tag Update Tracker")

    channel = client.get_channel(channel_id)

    if isinstance(channel, discord.TextChannel):
        await channel.send(embed=embed)

async def dispatch_updates(client: Client, build_id, prev_version, new_version, last_unity_ver, new_unity_ver):
    for channel_id in db.get_channels():
        await send_update_message(client, channel_id, build_id, prev_version, new_version, last_unity_ver, new_unity_ver)