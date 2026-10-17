"""
Main entry point for Jarvis AI Assistant
"""

import sys
import os
import logging
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from jarvis import Jarvis
from config import LOG_LEVEL, LOG_FILE
import argparse

# ==================== LOGGING SETUP ====================
def setup_logging():
    """Setup logging configuration"""
    log_dir = Path(LOG_FILE).parent
    log_dir.mkdir(exist_ok=True)
    
    logging.basicConfig(
        level=getattr(logging, LOG_LEVEL),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(LOG_FILE),
            logging.StreamHandler()
        ]
    )

logger = logging.getLogger(__name__)

def main():
    """Main function to run Jarvis"""
    setup_logging()
    logger.info("=" * 50)
    logger.info("🤖 Starting Jarvis AI Assistant")
    logger.info("=" * 50)
    
    try:
        # Initialize Jarvis
        jarvis = Jarvis()
        
        # Start listening
        print("\n" + "="*50)
        print("🎤 Jarvis is listening... Say 'Hello Jarvis' to start!")
        print("="*50 + "\n")
        
        jarvis.listen_and_respond()
        
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye! Jarvis is shutting down...")
        logger.info("Jarvis stopped by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        print(f"\n❌ Error: {e}")
        sys.exit(1)

def run_web_interface():
    """Run web interface"""
    os.chdir('web_interface')
    os.system('python app.py')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Jarvis AI Assistant')
    parser.add_argument('--web', action='store_true', help='Run web interface')
    parser.add_argument('--voice', action='store_true', default=True, help='Run voice interface')
    
    args = parser.parse_args()
    
    if args.web:
        run_web_interface()
    else:
        main()