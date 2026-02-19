import os
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
GAME_ID = os.getenv("GAME_ID")
GAME_NAME = os.getenv("GAME_NAME")
CLIP_COUNT = int(os.getenv("CLIP_COUNT", "30"))
CLIPS_FOLDER = os.getenv("CLIPS_FOLDER", "clips")
CLIPS_AGE = os.getenv("CLIPS_AGE", 7)
MAX_DURATION = os.getenv("MAX_DURATION", 60)

HEADERS = {
    "Client-ID": CLIENT_ID,
    "Authorization": f"Bearer {ACCESS_TOKEN}"
}