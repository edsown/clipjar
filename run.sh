#!/bin/bash

if [ -z "$1" ]; then
    echo "Usage: ./run.sh <game_name>"
    echo "       ./run.sh --list"
    echo "       ./run.sh --update-ids"
    exit 1
fi

if [ "$1" = "--update-ids" ]; then
    echo "🔄 Updating game IDs..."
    docker run --rm \
      --env-file .env \
      -v "$(pwd)/scripts:/app/scripts" \
      -v "$(pwd)/config:/app/config" \
      clipjar:latest python scripts/update_game_ids.py
    exit 0
fi

# Run container
docker run --rm \
  --env-file .env \
  -v "$(pwd)/output:/app/output" \
  clipjar:latest "$@"