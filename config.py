import os
from dotenv import load_dotenv

load_dotenv()

BINANCE_API_KEY: str = os.getenv("BINANCE_API_KEY", "")
BINANCE_API_SECRET: str = os.getenv("BINANCE_API_SECRET", "")
BINANCE_BASE_URL: str = "https://testnet.binancefuture.com"

LOG_DIR: str = "logs"
LOG_FILE: str = "logs/trading_bot.log"
LOG_FORMAT: str = "%(asctime)s | %(levelname)s | %(module)s | %(message)s"
LOG_DATE_FORMAT: str = "%Y-%m-%d %H:%M:%S"