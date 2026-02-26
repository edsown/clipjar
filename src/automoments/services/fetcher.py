import requests
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

class Fetcher:
    def __init__(self, config):
        self.now = datetime.now()
        self.past = self.now - timedelta(days=int(config["clips"]["age_days"]))
        self.game_id = config["game"]["id"]
        self.clip_count = config["clips"]["count"]
        self.headers = config["headers"]
    def get_clips(self): 
        url = (
            "https://api.twitch.tv/helix/clips"
            f"?game_id={self.game_id}"
            f"&first={self.clip_count}"
            f"&started_at={self.past.strftime('%Y-%m-%dT%H:%M:%SZ')}"
            f"&ended_at={self.now.strftime('%Y-%m-%dT%H:%M:%SZ')}"
        )
        res = requests.get(url,headers=self.headers)
        res.raise_for_status() 
        data = res.json() 
        return data["data"]
