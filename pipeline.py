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
        logger.info("Fetching clips from Twitch")
        
        try:
            clips = self.fetcher.get_clips()
            if clips:
                logger.info(f"Got {len(clips)} clips")
            else:
                logger.warning("Couldn't find any clips")
            return clips
        except Exception as e:
            logger.error(f"Failed to fetch clips: {e}")
            return []
    
    def _select_clips(self, clips):
        logger.info("Selecting clips by duration")
        
        selected = self.selector.select_by_duration(
            clips, 
            self.config['clips']['max_duration']
        )
        
        if selected:
            logger.info(f"Selected {len(selected)} clips")
        else:
            logger.warning("No clips matched duration criteria")
        
        return selected
    
    def _download_clips(self, clips):
        logger.info("Downloading clips")
        
        try:
            paths = self.downloader.download_clips(clips)
            if paths:
                logger.info(f"Downloaded {len(paths)} of {len(clips)} clips")
            else:
                logger.warning("No clips were downloaded")
            return paths
        except Exception as e:
            logger.error(f"Download failed: {e}")
            return []
    
    def _filter_clips(self, paths, clips):
        logger.info("Filtering clips by motion and language")
        
        try:
            filtered_paths, filtered_clips = self.filter_service.filter_by_motion_and_language(
                paths, 
                clips
            )
            
            if filtered_paths:
                logger.info(f"{len(filtered_paths)} clips passed filtering")
            else:
                logger.warning("No clips passed the filters")
            
            return filtered_paths, filtered_clips
        except Exception as e:
            logger.error(f"Filtering failed: {e}")
            return [], []
    
    def _merge_clips(self, paths, clips):
        logger.info("Merging clips into final video")
        
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
            
            logger.info(f"Saved video to {output_path}")
            return output_path
        except Exception as e:
            logger.error(f"Merge failed: {e}")
            return None