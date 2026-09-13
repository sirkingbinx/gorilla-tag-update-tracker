# manager for loading/saving/updating channel data

import json
import os

CHANNELS_FILE = "channels.json"
channels = []

def get_channels() -> list[int]:
    return channels

def load_db():
    global channels

    if not os.path.exists(CHANNELS_FILE):
        return {}

    with open(CHANNELS_FILE, "r") as f:
        try:
            channels = json.load(f)
        except json.JSONDecodeError:
            channels = []

def save_db():
    global channels

    with open(CHANNELS_FILE, "w") as f:
        try:
            json.dump(channels, f)
        except json.JSONDecodeError:
            print("could not save; skipping")

def add_channel(channel_id):
    channels.append(channel_id)
    save_db()