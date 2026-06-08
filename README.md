# Binance Futures Testnet Trading Bot

A clean, production-ready CLI trading bot for Binance USDT-M Futures Testnet.  
Supports **MARKET**, **LIMIT**, and **STOP-LIMIT** orders with strong input validation, structured logging, and a layered architecture.

---

## Features

- Place **MARKET**, **LIMIT**, and **STOP-LIMIT** orders via the CLI
- BUY and SELL support
- Strong input validation with helpful error messages
- File-based logging with timestamps, levels, and module names
- Custom exception hierarchy for clean error handling
- `.env`-based credential management (no hardcoded secrets)
- SOLID-aligned project structure (API / service / CLI layers)

---

## Project Structure

```
project/
├── main.py
├── config.py
├── requirements.txt
├── .env.example
├── README.md
├── logs/
│   └── trading_bot.log
├── client/
│   ├── __init__.py
│   └── binance_client.py
├── services/
│   ├── __init__.py
│   └── order_service.py
├── cli/
│   ├── __init__.py
│   └── commands.py
└── utils/
    ├── __init__.py
    ├── exceptions.py
    ├── logger.py
    └── validators.py
```

---

## Installation

```bash
git clone https://github.com/Krishi-del/binance-bot
cd binance_bot
python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate

pip install -r requirements.txt
```

---

## Environment Setup

1. Copy `.env.example` to `.env`:
```bash
   cp .env.example .env
```
2. Fill in your Binance Testnet credentials:
```env
   BINANCE_API_KEY=test
   BINANCE_API_SECRET=test
```

## Example Commands

### Market Buy
```bash
python main.py --symbol BTCUSDT --side BUY --order-type MARKET --quantity 0.001
```

### Limit Sell
```bash
python main.py --symbol BTCUSDT --side SELL --order-type LIMIT --quantity 0.001 --price 70000
```

### Stop-Limit Buy
```bash
python main.py --symbol BTCUSDT --side BUY --order-type STOP_LIMIT --quantity 0.001 --stop-price 65000 --price 65100
```

---

## Example Successful Output

```
## Order Summary

  Symbol:    BTCUSDT
  Side:      BUY
  Type:      LIMIT
  Quantity:  0.001
  Price:     50000

## Order Response

  Order ID:     123456789
  Status:       NEW
  Executed Qty: 0
  Avg Price:    0

✓ Order placed successfully
```

## Example Error Output

```
✗ Price is required for LIMIT orders.
```

```
✗ Binance API error: Binance error -1121: Invalid symbol.
```

---

## Logging

Logs are written to `logs/trading_bot.log`.

Format:
```
2025-01-01 10:00:00 | INFO | binance_client | Placing BUY LIMIT order | symbol=BTCUSDT qty=0.001
```

Levels used:
| Level   | When                                             |
|---------|--------------------------------------------------|
| DEBUG   | Full request/response details                    |
| INFO    | Order placement and successful completion        |
| WARNING | Validation errors, user input problems           |
| ERROR   | API errors, auth failures, network issues        |

Console output only shows WARNING and above to keep the CLI clean.

---

## Troubleshooting

| Problem | Solution |
|---|---|
| `ConfigurationError: API keys missing` | Ensure `.env` exists with valid keys |
| `AuthenticationError` | Regenerate keys on the testnet dashboard |
| `Binance error -1121: Invalid symbol` | Check the symbol format — must match exactly (e.g. `BTCUSDT`) |
| `NetworkError: timed out` | Check your internet connection or VPN settings |
| `ValidationError: Price required` | Add `--price` for LIMIT and STOP_LIMIT orders |

## Tech Stack

- Python 3.10+
- Requests / Binance REST API
- python-dotenv
- Logging module