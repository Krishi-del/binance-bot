# Binance Futures Testnet Trading Bot

## Overview

A Python CLI application for placing MARKET and LIMIT orders on Binance Futures Testnet (USDT-M).

Features:

* MARKET orders
* LIMIT orders
* STOP_LIMIT orders (bonus)
* BUY and SELL support
* Input validation
* Structured logging
* Error handling
* Modular architecture

## Setup

### Clone Repository

```bash
git clone <repo-url>
cd binance-bot
```

### Create Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Configure Environment Variables

Create a `.env` file:

```env
BINANCE_API_KEY=your_api_key
BINANCE_API_SECRET=your_api_secret
```

## Usage

### Market Order

```bash
python main.py --symbol BTCUSDT --side BUY --order-type MARKET --quantity 0.001
```

### Limit Order

```bash
python main.py --symbol BTCUSDT --side BUY --order-type LIMIT --quantity 0.001 --price 50000
```

### Stop-Limit Order

```bash
python main.py --symbol BTCUSDT --side BUY --order-type STOP_LIMIT --quantity 0.001 --price 50000 --stop-price 49000
```

## Project Structure

```text
cli/
client/
services/
utils/
main.py
config.py
```

## Logging

Logs are written to:

```text
logs/trading_bot.log
```

## Assumptions

* Binance Futures Testnet credentials are required for successful order execution.
* Validation, logging, request generation, and API communication were tested successfully.
* Successful order placement could not be verified without valid Binance Futures Testnet credentials.
