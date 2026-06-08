"""
main.py - Application entry point
"""

import argparse
from cli.commands import place_order

def parse_args():
    parser = argparse.ArgumentParser(description="Binance Futures Trading Bot")

    parser.add_argument("--symbol", required=True)
    parser.add_argument("--side", required=True, choices=["BUY", "SELL"])
    parser.add_argument("--order-type", required=True, choices=["MARKET", "LIMIT", "STOP_LIMIT"])
    parser.add_argument("--quantity", type=float, required=True)
    parser.add_argument("--price", type=float, default=None)
    parser.add_argument("--stop-price", type=float, default=None)

    # 🔥 IMPORTANT FOR YOU (since you don't have API keys yet)
    parser.add_argument("--mock", action="store_true")

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    place_order()