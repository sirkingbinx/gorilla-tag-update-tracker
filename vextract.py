import os
import re
import subprocess

from dotenv import load_dotenv
load_dotenv()

STEAMCMD_FOLDER = os.getenv("STEAMCMD_FOLDER")
STEAMCMD_PATH = os.getenv("STEAMCMD_PATH")
STEAMCMD_USER = os.getenv("STEAMCMD_CACHE_USERNAME")

commands = (
      f'+login {STEAMCMD_USER} '
      '+sDepotDownloadFileFilter "*globalgamemanagers;*data.unity3d" '
      '+download_depot 1533390 1533391 '
      '+quit'
)

OUTPUT_DIR = os.path.join(STEAMCMD_FOLDER, "steamapps", "content",
                          "app_1533390", "depot_1533391",
                          "Gorilla Tag_Data")

def run_steam_download():
    print(f'{STEAMCMD_PATH} {commands}')

    process = subprocess.run(
      f'{STEAMCMD_PATH} {commands}', capture_output=True, text=True, shell=True
    )

    return OUTPUT_DIR

def get_version():
    game_path = run_steam_download()

    if game_path is None:
        return {
            "unityVersion": "Unknown",
            "gameVersion": "Failed Steam download"
        }

    ggm_path = os.path.join(game_path, "globalgamemanagers")

    with open(ggm_path, "rb") as f:
        content = f.read()

    matches = re.findall(b"[0-9]+\\.[0-9]+\\.[0-9]+[a-zA-Z0-9]*", content)
    if matches:
        # 0 is Unity version
        # 1 is GT version
        version_table = [m.decode('utf-8') for m in matches]

        return {
            "unityVersion": version_table[0],
            "gameVersion": version_table[1]
        }

    return {
        "unityVersion": "Unknown",
        "gameVersion": "Failed parsing"
    }