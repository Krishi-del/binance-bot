from utils.exceptions import ValidationError
from utils.logger import get_logger

logger = get_logger(__name__)

VALID_SIDES = ("BUY", "SELL")
VALID_ORDER_TYPES = ("MARKET", "LIMIT", "STOP_LIMIT")

# 🔥 prevents repeated log spam for same error
_logged_errors = set()


def _log_once(message: str) -> None:
    """Avoid repeating same validation warnings in logs."""
    if message in _logged_errors:
        return
    _logged_errors.add(message)
    logger.warning("Validation error: %s", message)


def validate_symbol(symbol: str) -> str:
    if not symbol or not symbol.strip():
        msg = "Symbol cannot be empty."
        _log_once(msg)
        raise ValidationError(msg)

    return symbol.strip().upper()


def validate_side(side: str) -> str:
    normalised = side.strip().upper()

    if normalised not in VALID_SIDES:
        msg = f"Side must be one of {VALID_SIDES}. Got: '{side}'."
        _log_once(msg)
        raise ValidationError(msg)

    return normalised


def validate_order_type(order_type: str) -> str:
    normalised = order_type.strip().upper()

    if normalised not in VALID_ORDER_TYPES:
        msg = f"Order type must be one of {VALID_ORDER_TYPES}. Got: '{order_type}'."
        _log_once(msg)
        raise ValidationError(msg)

    return normalised


def validate_quantity(quantity: float) -> float:
    if quantity is None or quantity <= 0:
        msg = f"Quantity must be a positive number. Got: {quantity}."
        _log_once(msg)
        raise ValidationError(msg)

    return quantity


def validate_price(price: float | None, order_type: str) -> float | None:
    if order_type == "MARKET":
        return None

    if price is None:
        msg = f"Price is required for {order_type} orders."
        _log_once(msg)
        raise ValidationError(msg)

    if price <= 0:
        msg = f"Price must be a positive number. Got: {price}."
        _log_once(msg)
        raise ValidationError(msg)

    return price


def validate_stop_price(stop_price: float | None, order_type: str) -> float | None:
    if order_type != "STOP_LIMIT":
        return None

    if stop_price is None:
        msg = "stop_price is required for STOP_LIMIT orders."
        _log_once(msg)
        raise ValidationError(msg)

    if stop_price <= 0:
        msg = f"stop_price must be a positive number. Got: {stop_price}."
        _log_once(msg)
        raise ValidationError(msg)

    return stop_price