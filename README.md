# automoments

Makes compilation videos from Twitch clips. Downloads clips, filters out boring ones with motion detection, merges them together.

## Structure

```
automoments/
├── src/automoments/          # Main source package
│   ├── core/                 # Core components
│   │   ├── config.py         # Configuration loader
│   │   └── pipeline.py       # Main pipeline orchestration
│   ├── services/             # Business logic services
│   │   ├── fetcher.py        # Twitch API clip fetcher
│   │   ├── downloader.py     # Parallel clip downloader
│   │   ├── filter.py         # Motion detection
│   │   ├── merger.py         # Video merger with FFmpeg
│   │   └── clip_services.py  # Clip filtering & selection
│   └── utils/                # Utility functions
│       └── helpers.py        # Helper functions
├── config/                   # Game configuration files
│   ├── league.yaml
│   ├── overwatch.yaml
│   └── valorant.yaml
├── scripts/                  # Utility scripts
│   └── update_game_ids.py    # Update game IDs via Twitch API
├── clips/                    # Temporary clip storage (gitignored)
├── main.py                   # CLI entry point
├── requirements.txt          # Python dependencies
└── .env                      # API credentials (gitignored)
```

## What it does

- Downloads clips in parallel from Twitch
- Filters out static clips (motion detection)
- Filters by language
- Adds streamer names and view counts to videos
- Uses hardware acceleration on Mac
- Config files for different games

## Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

brew install twitch-dl ffmpeg
```

Create `.env` file:

```
CLIENT_ID=your_client_id
ACCESS_TOKEN=your_token
```

## Usage

```bash
./run.sh --list
./run.sh valorant
./run.sh valorant --verbose
```

## Config

Each game has a yaml file in `config/`. Example:

```yaml
game:
  id: "516575"
  name: "VALORANT"

clips:
  count: 100
  age_days: 7
  max_duration: 600
  min_views: 1000

filter:
  motion_threshold: 3.0
  talking_clips_language: "en"

output:
  width: 1920
  height: 1080
  fps: 30
  clips_folder: "clips"
  use_hw_accel: true

processing:
  max_workers: 4
```

## Dependencies

- requests, pyyaml, opencv-python, numpy, python-dotenv
- twitch-dl, ffmpeg
