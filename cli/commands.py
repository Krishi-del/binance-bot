import sys
from typing import Optional

import click

from client.binance_client import BinanceClient
from services.order_service import OrderService, OrderRequest
from utils.exceptions import (
    AuthenticationError,
    BinanceAPIError,
    ConfigurationError,
    NetworkError,
    ValidationError,
)
from utils.logger import get_logger

logger = get_logger(__name__)


def _print_order_summary(order: OrderRequest) -> None:
    click.echo("\n## Order Summary\n")
    click.echo(f"  Symbol:    {order.symbol}")
    click.echo(f"  Side:      {order.side}")
    click.echo(f"  Type:      {order.order_type}")
    click.echo(f"  Quantity:  {order.quantity}")

    if order.price is not None:
        click.echo(f"  Price:     {order.price}")

    if order.stop_price is not None:
        click.echo(f"  Stop Price:{order.stop_price}")

    click.echo()


def _print_order_result(result) -> None:
    click.echo("## Order Response\n")
    click.echo(f"  Order ID:     {result.order_id}")
    click.echo(f"  Status:       {result.status}")
    click.echo(f"  Executed Qty: {result.executed_qty}")
    click.echo(f"  Avg Price:    {result.avg_price}")
    click.echo()


@click.command(context_settings={"help_option_names": ["-h", "--help"]})
@click.option("--symbol", required=True, help="Trading pair, e.g. BTCUSDT")
@click.option("--side", required=True, help="BUY or SELL")
@click.option("--order-type", "order_type", required=True, help="MARKET, LIMIT, STOP_LIMIT")
@click.option("--quantity", required=True, type=float, help="Order quantity")
@click.option("--price", default=None, type=float, help="Limit price")
@click.option("--stop-price", "stop_price", default=None, type=float, help="Stop price")
@click.option("--mock", is_flag=True, default=False, help="Run without API (mock mode)")
def place_order(
    symbol: str,
    side: str,
    order_type: str,
    quantity: float,
    price: Optional[float],
    stop_price: Optional[float],
    mock: bool,
) -> None:
    """
    Place a futures order on Binance Testnet or run in mock mode.
    """

    try:
        #  LOG MODE
        logger.info("Mode selected | mock=%s", mock)

        # Build + validate order
        order = OrderService(None).build_and_validate(
            symbol=symbol,
            side=side,
            order_type=order_type,
            quantity=quantity,
            price=price,
            stop_price=stop_price,
        )

        _print_order_summary(order)

        # =========================
        #  MOCK MODE
        # =========================
        if mock:
            logger.info("Running in MOCK mode (no API call will be made)")

            class MockResult:
                def __init__(self, order):
                    self.order_id = 999999
                    self.status = "FILLED" if order.order_type == "MARKET" else "NEW"
                    self.executed_qty = order.quantity
                    self.avg_price = order.price or "N/A"

            result = MockResult(order)

            logger.info(
                "Mock order executed | orderId=%s status=%s",
                result.order_id,
                result.status,
            )

        # =========================
        #  REAL MODE
        # =========================
        else:
            logger.info("Running in REAL API mode (BinanceClient active)")

            client = BinanceClient()
            service = OrderService(client)
            result = service.submit(order)

            logger.info(
                "Real order executed | orderId=%s status=%s",
                result.order_id,
                result.status,
            )

        # Output result
        _print_order_result(result)

        click.secho("\n✓ Order processed successfully", fg="green", bold=True)

    # =========================
    # ERROR HANDLING
    # =========================
    except (ValidationError, ConfigurationError) as exc:
        click.secho(f"\n✗ {exc}", fg="red", bold=True)
        sys.exit(1)

    except AuthenticationError as exc:
        click.secho(f"\n✗ Authentication failed: {exc}", fg="red", bold=True)
        sys.exit(1)

    except BinanceAPIError as exc:
        click.secho(f"\n✗ Binance API error: {exc}", fg="red", bold=True)
        sys.exit(1)

    except NetworkError as exc:
        click.secho(f"\n✗ Network error: {exc}", fg="red", bold=True)
        sys.exit(1)

    except Exception as exc:
        click.secho(f"\n✗ Unexpected error: {exc}", fg="red", bold=True)
        logger.exception("Unexpected error: %s", exc)
        sys.exit(1)