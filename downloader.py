import subprocess
import os
from config import CLIPS_FOLDER, GAME_NAME, MAX_WORKERS
import shutil
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
import logging

logger = logging.getLogger(__name__)

class ClipDownloader: 
    def __init__(self, clips_folder = CLIPS_FOLDER, max_workers = int(MAX_WORKERS)):
        self.clips_folder = clips_folder
        self.max_workers = max_workers
        self._ensure_clips_folder()

    def download_clips(self, clip_data):
        if not os.path.exists(self.clips_folder):
            logger.error(f"Clips folder not found: {self.clips_folder}")
            return []

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_index = {executor.submit(self._download_one, clip): i for i, clip in enumerate(clip_data)}
            
            ordered_results = [None] * len(clip_data)
            
            for future in as_completed(future_to_index):
                index = future_to_index[future]
                path = future.result()
                ordered_results[index] = path

        return [path for path in ordered_results if path]

    def _download_one(self, clip):
        filename = f"{GAME_NAME}_{clip['broadcaster_name']}_{datetime.now().isoformat()}"
        command = [
            "twitch-dl", "download", clip["url"], 
            "-q", "source", 
            "--overwrite",
            "--output", f"{filename}.mp4"
        ]

        result = subprocess.run(command, cwd=self.clips_folder, text=True)

        if result.returncode != 0:
            logger.error(f"Failed to download clip from {clip['broadcaster_name']}: {result.stderr}")
            return None

        expected_path = os.path.join(self.clips_folder, f"{filename}.mp4")
        return expected_path if os.path.exists(expected_path) else None

    def _ensure_clips_folder(self):
        if os.path.exists(self.clips_folder):
            shutil.rmtree(self.clips_folder)
        os.makedirs(self.clips_folder, exist_ok=True)