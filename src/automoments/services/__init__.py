"""Services for fetching, downloading, filtering, and merging clips"""

from automoments.services.fetcher import Fetcher
from automoments.services.downloader import ClipDownloader
from automoments.services.filter import MotionDetector
from automoments.services.merger import Merger
from automoments.services.clip_services import (
    ClipFilterService,
    ClipDataExtractor,
    ClipSelector
)

__all__ = [
    'Fetcher',
    'ClipDownloader',
    'MotionDetector',
    'Merger',
    'ClipFilterService',
    'ClipDataExtractor',
    'ClipSelector'
]
