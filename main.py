import util
import fetcher
from datetime import datetime
import downloader
from config import MAX_DURATION, GAME_NAME
import merger
import filter


if __name__ == "__main__":
    clip_data = fetcher.get_clips()
    clip_amount = util.get_clip_amount(clip_data, max_duration=MAX_DURATION)
    clip_data = clip_data[:clip_amount]
    gameplay_clips = filter.filter_gameplay_clips(clip_data)
    clip_downloader = downloader.ClipDownloader()
    paths = clip_downloader.download_clips(gameplay_clips)
    if paths:
        merger.merge_clips(paths)
    else:
        print("No clips to merge.")