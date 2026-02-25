import logging
from typing import Optional
import fetcher
import downloader
import merger
from services import ClipFilterService, ClipDataExtractor, ClipSelector
from config import ConfigLoader

logger = logging.getLogger(__name__)


class ClipPipeline:
    
    def __init__(self, config):
        self.config = config
        
        self.fetcher = fetcher.Fetcher(config)
        self.downloader = downloader.ClipDownloader(
            clips_folder=config['output']['clips_folder'],
            max_workers=config['processing']['max_workers'],
            game_name=config['game']['name']
        )
        self.filter_service = ClipFilterService(
            talking_language=config['filter']['talking_clips_language'],
            motion_threshold=config['filter']['motion_threshold']
        )
        self.merger = merger.Merger(
            width=config['output']['width'],
            height=config['output']['height'],
            fps=config['output']['fps'],
            use_hw_accel=config['output']['use_hw_accel']
        )
        self.selector = ClipSelector()
        self.extractor = ClipDataExtractor()
    
    def run(self) -> Optional[str]:
        clips = self._fetch_clips()
        if not clips:
            return None
        
        selected_clips = self._select_clips(clips)
        if not selected_clips:
            return None
        
        paths = self._download_clips(selected_clips)
        if not paths:
            return None
        
        filtered_paths, filtered_clips = self._filter_clips(paths, selected_clips)
        if not filtered_paths:
            return None
        
        output_path = self._merge_clips(filtered_paths, filtered_clips)
        return output_path
    
    def _fetch_clips(self):
        logger.info("=" * 60)
        logger.info("STEP 1: Fetching clips from Twitch")
        logger.info("=" * 60)
        
        try:
            clips = self.fetcher.get_clips()
            if clips:
                logger.info(f"✓ Fetched {len(clips)} clips")
            else:
                logger.warning("No clips found")
            return clips
        except Exception as e:
            logger.error(f"Failed to fetch clips: {e}")
            return []
    
    def _select_clips(self, clips):
        logger.info("=" * 60)
        logger.info("STEP 2: Selecting clips by duration")
        logger.info("=" * 60)
        
        selected = self.selector.select_by_duration(
            clips, 
            self.config['clips']['max_duration']
        )
        
        if selected:
            logger.info(f"✓ Selected {len(selected)} clips")
        else:
            logger.warning("No clips selected")
        
        return selected
    
    def _download_clips(self, clips):
        logger.info("=" * 60)
        logger.info("STEP 3: Downloading clips")
        logger.info("=" * 60)
        
        try:
            paths = self.downloader.download_clips(clips)
            if paths:
                logger.info(f"✓ Downloaded {len(paths)}/{len(clips)} clips")
            else:
                logger.warning("No clips downloaded successfully")
            return paths
        except Exception as e:
            logger.error(f"Failed to download clips: {e}")
            return []
    
    def _filter_clips(self, paths, clips):
        logger.info("=" * 60)
        logger.info("STEP 4: Filtering clips")
        logger.info("=" * 60)
        
        try:
            filtered_paths, filtered_clips = self.filter_service.filter_by_motion_and_language(
                paths, 
                clips
            )
            
            if filtered_paths:
                logger.info(f"✓ {len(filtered_paths)} clips passed filtering")
            else:
                logger.warning("No clips passed filtering")
            
            return filtered_paths, filtered_clips
        except Exception as e:
            logger.error(f"Failed to filter clips: {e}")
            return [], []
    
    def _merge_clips(self, paths, clips):
        logger.info("=" * 60)
        logger.info("STEP 5: Merging clips")
        logger.info("=" * 60)
        
        try:
            streamer_names = self.extractor.get_streamer_names(clips)
            view_counts = self.extractor.get_view_counts(clips)
            
            output_path = f"{self.config['game']['name']}.mp4"
            
            self.merger.merge_clips(
                paths, 
                streamer_names, 
                view_counts, 
                output_path=output_path
            )
            
            logger.info(f"✓ Video saved: {output_path}")
            return output_path
        except Exception as e:
            logger.error(f"Failed to merge clips: {e}")
            return None