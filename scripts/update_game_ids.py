import os
import yaml
import requests
from pathlib import Path
from dotenv import load_dotenv
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")

if not CLIENT_ID or not ACCESS_TOKEN:
    logger.error("Missing CLIENT_ID or ACCESS_TOKEN in .env file")
    exit(1)

HEADERS = {
    "Client-ID": CLIENT_ID,
    "Authorization": f"Bearer {ACCESS_TOKEN}"
}

TWITCH_API_BASE = "https://api.twitch.tv/helix/games"
CONFIG_DIR = Path(__file__).parent.parent / "config"


def search_game(game_name: str) -> dict:
    url = f"{TWITCH_API_BASE}?name={game_name}"
    
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        games = data.get("data", [])
        
        if not games:
            logger.warning(f"No exact match found for '{game_name}'")
            return None
        
        game = games[0]
        return {
            "id": game["id"],
            "name": game["name"]
        }
        
    except requests.exceptions.RequestException as e:
        logger.error(f"API error for '{game_name}': {e}")
        return None


def update_config_file(config_path: Path, game_info: dict):
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    
    if 'game' not in config:
        config['game'] = {}
    
    old_id = config['game'].get('id', 'unknown')
    old_name = config['game'].get('name', 'unknown')
    
    config['game']['id'] = game_info['id']
    config['game']['name'] = game_info['name']
    
    with open(config_path, 'w') as f:
        yaml.dump(config, f, default_flow_style=False, sort_keys=False)
    
    logger.info(f"Updated {config_path.name}: {old_name} ({old_id}) to {game_info['name']} ({game_info['id']})")


def main():
    logger.info("Twitch Game ID Updater")
    
    if not CONFIG_DIR.exists():
        logger.error(f"Config directory not found: {CONFIG_DIR}")
        exit(1)
    
    config_files = list(CONFIG_DIR.glob("*.yaml"))
    
    if not config_files:
        logger.error(f"No YAML files found in {CONFIG_DIR}")
        exit(1)
    
    logger.info(f"Found {len(config_files)} config file(s)")
    
    for config_path in sorted(config_files):
        logger.info(f"Processing {config_path.name}")
        
        try:
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)
            
            if not config or 'game' not in config:
                logger.warning(f"No 'game' section found in {config_path.name}, skipping")
                continue
            
            game_name = config['game'].get('name')
            
            if not game_name:
                logger.warning(f"No game name found in {config_path.name}, skipping")
                continue
            
            logger.debug(f"Searching for: {game_name}")
            
            game_info = search_game(game_name)
            
            if game_info:
                update_config_file(config_path, game_info)
            else:
                logger.warning(f"Could not find game '{game_name}', skipping update")
            
        except Exception as e:
            logger.error(f"Error processing {config_path.name}: {e}")
    
    logger.info("Done updating game IDs")


if __name__ == "__main__":
    main()
