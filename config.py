import os
import yaml
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()


class ConfigLoader:
    
    CONFIG_DIR = Path(__file__).parent / "game_configs"
    
    @classmethod
    def load(cls, game_name: str) -> dict:
        """Load configuration for a specific game"""
        config_path = cls.CONFIG_DIR / f"{game_name}.yaml"
        
        if not config_path.exists():
            available = cls.list_available_games()
            available_str = ", ".join(available) if available else "none"
            raise FileNotFoundError(
                f"Config file not found: {config_path}\n"
                f"Available games: {available_str}"
            )
        
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        
        client_id = os.getenv("CLIENT_ID")
        access_token = os.getenv("ACCESS_TOKEN")
        
        if not client_id or not access_token:
            raise ValueError(
                "Missing Twitch API credentials in .env file.\n"
                "Required: CLIENT_ID and ACCESS_TOKEN"
            )
        
        config['client_id'] = client_id
        config['access_token'] = access_token
        config['headers'] = {
            "Client-ID": client_id,
            "Authorization": f"Bearer {access_token}"
        }
        
        return config
    
    @classmethod
    def list_available_games(cls) -> list:
        if not cls.CONFIG_DIR.exists():
            return []
        
        return [f.stem for f in cls.CONFIG_DIR.glob("*.yaml")]