from dataclasses import dataclass
from typing import Any

from client.binance_client import BinanceClient
from utils.logger import get_logger
from utils.validators import (
    validate_order_type,
    validate_price,
    validate_quantity,
    validate_side,
    validate_stop_price,
    validate_symbol,
)

logger = get_logger(__name__)


@dataclass
class OrderRequest:
    symbol: str
    side: str
    order_type: str
    quantity: float
    price: float | None = None
    stop_price: float | None = None


@dataclass
class OrderResult:
    order_id: int | str
    status: str
    executed_qty: str
    avg_price: str
    raw: dict[str, Any]


class OrderService:

    def __init__(self, client: BinanceClient) -> None:
        self._client = client

    def build_and_validate(
        self,
        symbol: str,
        side: str,
        order_type: str,
        quantity: float,
        price: float | None = None,
        stop_price: float | None = None,
    ) -> OrderRequest:
        return OrderRequest(
            symbol=validate_symbol(symbol),
            side=validate_side(side),
            order_type=validate_order_type(order_type),
            quantity=validate_quantity(quantity),
            price=validate_price(price, validate_order_type(order_type)),
            stop_price=validate_stop_price(stop_price, validate_order_type(order_type)),
        )

    def submit(self, order: OrderRequest) -> OrderResult:
        params: dict[str, Any] = {
            "symbol": order.symbol,
            "side": order.side,
            "type": self._api_order_type(order.order_type),
            "quantity": order.quantity,
        }

        tif = self._time_in_force(order.order_type)
        if tif:
            params["timeInForce"] = tif

        if order.price is not None:
            params["price"] = order.price

        if order.stop_price is not None:
            params["stopPrice"] = order.stop_price

        logger.debug("Submitting order params: %s", params)
        raw = self._client.place_order(params)

        return OrderResult(
            order_id=raw.get("orderId", "N/A"),
            status=raw.get("status", "N/A"),
            executed_qty=raw.get("executedQty", "0"),
            avg_price=raw.get("avgPrice", "0"),
            raw=raw,
        )

    @staticmethod
    def _api_order_type(order_type: str) -> str:
        return {"MARKET": "MARKET", "LIMIT": "LIMIT", "STOP_LIMIT": "STOP"}[order_type]

    @staticmethod
    def _time_in_force(order_type: str) -> str | None:
        return None if order_type == "MARKET" else "GTC"