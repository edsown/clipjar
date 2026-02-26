import logging
from filter import MotionDetector
from typing import List, Tuple

logger = logging.getLogger(__name__)


class ClipFilterService:
    
    def __init__(self, talking_language: str, motion_threshold: float):
        self.talking_language = talking_language
        self.motion_detector = MotionDetector(motion_threshold)
    
    def filter_by_motion_and_language(
        self, 
        paths: List[str], 
        clips: List[dict]
    ) -> Tuple[List[str], List[dict]]:
        active_paths = []
        filtered_clips = []
        
        for path, clip in zip(paths, clips):
            if self._should_keep_clip(path, clip):
                active_paths.append(path)
                filtered_clips.append(clip)
            else:
                self._log_filtered_clip(clip)
        
        logger.info(f"Kept {len(filtered_clips)} of {len(clips)} clips")
        return active_paths, filtered_clips
    
    def _should_keep_clip(self, path: str, clip: dict) -> bool:
        if clip.get("language") == self.talking_language:
            logger.debug(f"Keeping {clip['broadcaster_name']} ({self.talking_language} clip)")
            return True
        
        has_motion = self.motion_detector.has_motion(path)
        if has_motion:
            logger.debug(f"Keeping {clip['broadcaster_name']} (good motion)")
        
        return has_motion
    
    def _log_filtered_clip(self, clip: dict):
        language = clip.get('language', 'unknown')
        name = clip['broadcaster_name']
        logger.info(f"Filtered out static '{language}' clip: {name}")


class ClipDataExtractor:
    
    def get_streamer_names(self, clips: List[dict]) -> List[str]:
        return [clip["broadcaster_name"] for clip in clips]
    
    def get_view_counts(self, clips: List[dict]) -> List[int]:
        return [clip["view_count"] for clip in clips]


class ClipSelector:
    
    def select_by_duration(self, clips: List[dict], max_duration: int) -> List[dict]:
        selected = []
        total_duration = 0
        
        for clip in clips:
            if total_duration + clip["duration"] >= max_duration:
                break
            selected.append(clip)
            total_duration += clip["duration"]
        
        logger.info(f"Selected {len(selected)} clips, total {total_duration:.1f}s")
        return selected