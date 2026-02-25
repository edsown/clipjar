import requests
from datetime import datetime, timedelta
from config import GAME_ID, CLIP_COUNT, HEADERS, CLIPS_AGE
import logging

logger = logging.getLogger(__name__)

class Fetcher:
    def __init__(self):
        self.now = datetime.now()
        self.past = not - timedelta(days=int(CLIPS_AGE))
    def get_clips(self): 
        url = (
            "https://api.twitch.tv/helix/clips"
            f"?game_id={GAME_ID}"
            f"&first={CLIP_COUNT}"
            f"&started_at={self.past.strftime('%Y-%m-%dT%H:%M:%SZ')}"
            f"&ended_at={self.now.strftime('%Y-%m-%dT%H:%M:%SZ')}"
        )
        res = requests.get(url,headers=HEADERS)
        res.raise_for_status() 
        data = res.json() 
        return data["data"]
