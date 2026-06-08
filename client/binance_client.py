import hashlib
import hmac
import time
from typing import Any
from urllib.parse import urlencode

import requests

from config import BINANCE_API_KEY, BINANCE_API_SECRET, BINANCE_BASE_URL
from utils.exceptions import (
    AuthenticationError,
    BinanceAPIError,
    NetworkError,
    ConfigurationError,
)
from utils.logger import get_logger

logger = get_logger(__name__)


class BinanceClient:
    def __init__(self) -> None:
        self._validate_credentials()
        self._session = requests.Session()
        self._session.headers.update({"X-MBX-APIKEY": BINANCE_API_KEY})

    def place_order(self, params: dict[str, Any]) -> dict[str, Any]:
        signed_params = self._sign(params)
        url = f"{BINANCE_BASE_URL}/fapi/v1/order"

        logger.info(
            "Placing %s %s order | symbol=%s qty=%s",
            params.get("side"),
            params.get("type"),
            params.get("symbol"),
            params.get("quantity"),
        )

        try:
            response = self._session.post(url, params=signed_params, timeout=10)

        except requests.exceptions.Timeout as exc:
            logger.error("Request timeout")
            raise NetworkError("Request timed out") from exc

        except requests.exceptions.ConnectionError as exc:
            logger.error("Connection error")
            raise NetworkError("Could not connect to Binance") from exc

        except requests.exceptions.RequestException as exc:
            logger.error("Unexpected network error")
            raise NetworkError("Network error occurred") from exc

        return self._handle_response(response)

    def _validate_credentials(self) -> None:
        if not BINANCE_API_KEY or not BINANCE_API_SECRET:
            raise ConfigurationError(
                "BINANCE_API_KEY and BINANCE_API_SECRET must be set in .env"
            )

    def _sign(self, params: dict[str, Any]) -> dict[str, Any]:
        params["timestamp"] = int(time.time() * 1000)

        query_string = urlencode(params)

        signature = hmac.new(
            BINANCE_API_SECRET.encode("utf-8"),
            query_string.encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()

        params["signature"] = signature
        return params

    def _handle_response(self, response: requests.Response) -> dict[str, Any]:
        logger.debug("HTTP %s", response.status_code)

        
        if response.status_code in (401, 403):
            logger.error("Authentication failed (invalid API key)")
            raise AuthenticationError("Invalid API credentials")

        try:
            data = response.json()
        except Exception:
            logger.error("Invalid JSON response from Binance")
            raise BinanceAPIError("Invalid response from exchange")

        
        if isinstance(data, dict) and data.get("code"):
            code = data.get("code")
            msg = data.get("msg", "Unknown error")

            logger.error("Binance API error | code=%s", code)

            if code == -2014:
                raise AuthenticationError("Invalid API key")

            raise BinanceAPIError(msg, code=code)

        logger.info("Order placed successfully | orderId=%s", data.get("orderId"))

        return data