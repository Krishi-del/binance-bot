# Binance Futures Testnet Trading Bot

A lightweight Python CLI application to place MARKET, LIMIT, and STOP-LIMIT orders on Binance USDT-M Futures Testnet with clean architecture, structured logging, and strong validation.

---

## 🚀 Trading Environment

This bot is designed for Binance USDT-M Futures Testnet.

Base URL:
https://testnet.binancefuture.com

---

## 📌 Features

### Core Features (Required)
- Place MARKET orders
- Place LIMIT orders
- BUY and SELL support
- CLI-based input validation (argparse)
- Structured logging (file-based logs)
- Clean layered architecture:
  - API layer (Binance client)
  - Service layer (order logic)
  - CLI layer (user interface)
- Strong error handling:
  - Validation errors
  - API errors
  - Network failures

### Bonus Feature
- STOP-LIMIT order support

---

## 🏗 Project Structure


trading_bot/
│
├── main.py
├── config.py
├── requirements.txt
├── .env.example
├── logs/
│ └── trading_bot.log
│
├── client/
│ └── binance_client.py
│
├── services/
│ └── order_service.py
│
├── cli/
│ └── commands.py
│
└── utils/
├── exceptions.py
├── logger.py
└── validators.py


---

## ⚙️ Installation

```bash
git clone https://github.com/your-username/binance-bot
cd binance-bot

python -m venv venv

# Windows
venv\Scripts\activate

# Linux / Mac
source venv/bin/activate

pip install -r requirements.txt
## Environment Setup

Create a .env file:
--mock flag is used when API credentials are not available.
BINANCE_API_KEY=test
BINANCE_API_SECRET=test
##How to Run
MARKET Order (Required)
python main.py --symbol BTCUSDT --side BUY --order-type MARKET --quantity 0.001
LIMIT Order (Required)
python main.py --symbol BTCUSDT --side SELL --order-type LIMIT --quantity 0.001 --price 70000
STOP-LIMIT Order (Bonus)
python main.py --symbol BTCUSDT --side BUY --order-type STOP_LIMIT --quantity 0.001 --stop-price 65000 --price 65100
##Order Response Format

Each successful order returns:

orderId
status
executedQty
avgPrice (if available)

Example:

Order ID: 123456789
Status: FILLED
Executed Qty: 0.001
Avg Price: 50000

✓ Order placed successfully
## Logging

Logs are stored in:

logs/trading_bot.log
Log Format
2026-06-08 18:10:12 | INFO | binance_client | Placing BUY MARKET order | symbol=BTCUSDT qty=0.001
2026-06-08 18:10:13 | INFO | binance_client | Order successful | orderId=12345 status=FILLED
Log Levels
Level	Meaning
INFO	Order flow events
DEBUG	API request/response details
WARNING	Validation issues
ERROR	API/network failures
## Sample Logs (Required)
MARKET Order
2026-06-08 18:10:12 | INFO | binance_client | Placing BUY MARKET order | symbol=BTCUSDT qty=0.001
2026-06-08 18:10:13 | INFO | binance_client | Order successful | orderId=101 status=FILLED
LIMIT Order
2026-06-08 18:12:40 | INFO | binance_client | Placing SELL LIMIT order | symbol=BTCUSDT qty=0.001 price=70000
2026-06-08 18:12:41 | INFO | binance_client | Order successful | orderId=102 status=NEW
## Validation Rules
symbol → BTCUSDT format only
side → BUY or SELL
order-type → MARKET | LIMIT | STOP_LIMIT
quantity → must be greater than 0
price → required for LIMIT and STOP-LIMIT
stop-price → required for STOP-LIMIT
## Troubleshooting
Issue	Solution
Missing API keys	Create .env file
Authentication error	Regenerate testnet API keys
Invalid symbol	Use BTCUSDT format
Network timeout	Check internet/VPN
Price required error	Add --price for LIMIT orders