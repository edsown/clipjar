import logging
import argparse
import sys
from config import ConfigLoader
from pipeline import ClipPipeline

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def parse_args():
    parser = argparse.ArgumentParser(
        description="Generate highlight compilations from Twitch clips",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
                    Examples:
                      python main.py valorant
                      python main.py league_of_legends
                      python main.py --list
                            """
    )
    
    parser.add_argument(
        'game',
        type=str,
        nargs='?',
        help='Game name (must match a YAML file in configs/)'
    )
    
    parser.add_argument(
        '--list',
        action='store_true',
        help='List all available game configurations'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose debug logging'
    )
    
    return parser.parse_args()


def list_games():
    games = ConfigLoader.list_available_games()
    
    if not games:
        print("\nNo game configurations found in configs/ directory")
        print("Create a YAML file (e.g., configs/valorant.yaml)")
        return
    
    print("\nAvailable game configurations:")
    for game in sorted(games):
        print(f"  • {game}")
    print()


def main():
    args = parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    if args.list:
        list_games()
        return
    
    if not args.game:
        logger.error("Error: game name is required")
        print("\nUsage: python main.py <game_name>")
        print("Use --list to see available games")
        sys.exit(1)
    
    try:
        config = ConfigLoader.load(args.game)
        logger.info(f"Loaded configuration for: {config["game"]["name"]}")
    except FileNotFoundError as e:
        logger.error(str(e))
        print("\nUse --list to see available games")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Error loading config: {e}")
        sys.exit(1)
    
    try:
        pipeline = ClipPipeline(config)
        output = pipeline.run()
        
        if output:
            logger.info(f"All done! Video saved to {output}")
        else:
            logger.error("Something went wrong")
            sys.exit(1)
            
    except KeyboardInterrupt:
        logger.info("Stopped by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()