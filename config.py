import os
import yaml
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

class ConfigLoader:
    CONFIG_DIR = Path(__file__).parent / "configs"
    
    @classmethod
    def load(cls, game_name: str) -> dict:
        config_path = cls.CONFIG_DIR / f"{game_name}.yaml"
        
        if not config_path.exists():
            raise FileNotFoundError(f"Config file not found: {config_path}")
        
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        
        config['client_id'] = os.getenv("CLIENT_ID")
        config['access_token'] = os.getenv("ACCESS_TOKEN")
        config['headers'] = {
            "Client-ID": config['client_id'],
            "Authorization": f"Bearer {config['access_token']}"
        }
        
        return config
    
    @classmethod
    def list_available_games(cls) -> list:
        if not cls.CONFIG_DIR.exists():
            return []
        return [f.stem for f in cls.CONFIG_DIR.glob("*.yaml")]