# Restructure Notes

Reorganized into proper package structure.

### Old Structure

```
automoments/
├── config.py
├── downloader.py
├── fetcher.py
├── filter.py
├── main.py
├── merger.py
├── pipeline.py
├── services.py
├── update_game_ids.py
├── util.py
└── game_configs/
    ├── league.yaml
    ├── overwatch.yaml
    └── valorant.yaml
```

### New Structure

```
automoments/
├── src/automoments/          # Main package (organized by responsibility)
│   ├── core/                 # Core components (pipeline, config)
│   ├── services/             # Business logic (fetcher, downloader, etc)
│   └── utils/                # Utility functions
├── config/                   # Configuration files (moved from game_configs/)
├── scripts/                  # Utility scripts
├── clips/                    # Temporary clip storage
├── main.py                   # CLI entry point
├── run.sh                    # Convenience script
├── requirements.txt          # Dependencies
└── README.md                 # Documentation
```

## Usage

```bash
./run.sh valorant
# or
venv/bin/python main.py valorant
```

## Where things moved

| Old                   | New                                         |
| --------------------- | ------------------------------------------- |
| `config.py`           | `src/automoments/core/config.py`            |
| `pipeline.py`         | `src/automoments/core/pipeline.py`          |
| `fetcher.py`          | `src/automoments/services/fetcher.py`       |
| `downloader.py`       | `src/automoments/services/downloader.py`    |
| `filter.py`           | `src/automoments/services/filter.py`        |
| `merger.py`           | `src/automoments/services/merger.py`        |
| `services.py`         | `src/automoments/services/clip_services.py` |
| `util.py`             | `src/automoments/utils/helpers.py`          |
| `update_game_ids.py`  | `scripts/update_game_ids.py`                |
| `game_configs/*.yaml` | `config/*.yaml`                             |

## Notes

- Everything works the same, just organized differently
- Old files backed up in `_old/` - delete when ready
- Config files moved from `game_configs/` to `config/`
- Use `./run.sh` or activate venv to run
