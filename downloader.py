import subprocess
import os
from config import CLIPS_FOLDER, GAME_NAME
import shutil
from datetime import datetime
import glob

class ClipDownloader: 
    def __init__(self, clips_folder = CLIPS_FOLDER):
        self.clips_folder = clips_folder
        self._ensure_clips_folder()

    def download_clips(self, clip_data):
        paths = []
        for clip in clip_data:
            # Use --output to specify filename format
            filename = f"{GAME_NAME}_{clip['broadcaster_name']}_{datetime.now().isoformat()}"
            command = [
                "twitch-dl", "download", clip["url"], 
                "-q", "source", 
                "--overwrite",
                "--output", f"{filename}.mp4"
            ]

            if not os.path.exists(self.clips_folder):
                print("Error, no clip folder found")
                return paths

            result = subprocess.run(command, cwd=self.clips_folder, capture_output=True, text=True)

            if result.returncode != 0:
                print("Error:", result.stderr)
            else:
                print("Download successful!")
                expected_path = os.path.join(self.clips_folder, f"{filename}.mp4")
                if os.path.exists(expected_path):
                    paths.append(expected_path)
        
        return paths
        
    def _ensure_clips_folder(self):
        if os.path.exists(self.clips_folder):
            shutil.rmtree(self.clips_folder)
        os.makedirs(self.clips_folder, exist_ok=True)