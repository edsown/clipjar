import requests
from datetime import datetime, timedelta
from config import GAME_ID, CLIP_COUNT, HEADERS, CLIPS_AGE

def get_clips(): 
    now = datetime.now()
    past = now - timedelta(days=int(CLIPS_AGE))
    url = (
        "https://api.twitch.tv/helix/clips"
        f"?game_id={GAME_ID}"
        f"&first={CLIP_COUNT}"
        f"&started_at={past.strftime('%Y-%m-%dT%H:%M:%SZ')}"
        f"&ended_at={now.strftime('%Y-%m-%dT%H:%M:%SZ')}"
    )
    res = requests.get(url,headers=HEADERS)
    res.raise_for_status() 
    data = res.json() 
    return data["data"]
