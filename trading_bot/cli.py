"""Command-line interface for trading bot."""
import os
import sys
from decimal import Decimal
from typing import Optional

import click
from dotenv import load_dotenv

from bot.client import BinanceClient, BinanceAPIError
from bot.orders import OrderManager
from bot.validators import ValidationError
from bot.logging_config import setup_logger

logger = setup_logger(__name__)

# Load environment variables from .env file
load_dotenv()


@click.group()
@click.version_option(version="1.0.0")
def cli():
    """Trading Bot for Binance Futures Testnet"""
    pass


@cli.command()
@click.option(
    '--symbol',
    prompt='Trading Symbol (e.g., BTCUSDT)',
    help='Trading symbol'
)
@click.option(
    '--side',
    prompt='Order Side (BUY/SELL)',
    type=click.Choice(['BUY', 'SELL', 'buy', 'sell'], case_sensitive=False),
    help='Order side'
)
@click.option(
    '--order-type',
    prompt='Order Type (MARKET/LIMIT)',
    type=click.Choice(['MARKET', 'LIMIT', 'market', 'limit'], case_sensitive=False),
    help='Order type'
)
@click.option(
    '--quantity',
    prompt='Quantity',
    help='Order quantity'
)
@click.option(
    '--price',
    default=None,
    help='Order price (required for LIMIT orders)'
)
@click.option(
    '--api-key',
    envvar='BINANCE_API_KEY',
    help='Binance API Key (or set BINANCE_API_KEY env var)'
)
@click.option(
    '--api-secret',
    envvar='BINANCE_API_SECRET',
    help='Binance API Secret (or set BINANCE_API_SECRET env var)'
)
def place_order(
    symbol: str,
    side: str,
    order_type: str,
    quantity: str,
    price: Optional[str],
    api_key: str,
    api_secret: str
):
    """Place a market or limit order."""
    
    # Validate API credentials
    if not api_key or not api_secret:
        click.echo(
            click.style(
                "ERROR: API credentials not provided. Please set BINANCE_API_KEY "
                "and BINANCE_API_SECRET environment variables or use --api-key and --api-secret options.",
                fg='red'
            ),
            err=True
        )
        sys.exit(1)
    
    try:
        # Initialize client and order manager
        client = BinanceClient(api_key, api_secret)
        order_manager = OrderManager(client)
        
        # Print order request summary
        click.echo("\n" + "=" * 60)
        click.echo("ORDER REQUEST SUMMARY")
        click.echo("=" * 60)
        click.echo(f"Symbol:       {symbol}")
        click.echo(f"Side:         {side.upper()}")
        click.echo(f"Order Type:   {order_type.upper()}")
        click.echo(f"Quantity:     {quantity}")
        if price:
            click.echo(f"Price:        {price}")
        click.echo("=" * 60)
        
        # Place the order
        response = order_manager.place_order(
            symbol=symbol,
            side=side,
            order_type=order_type,
            quantity=quantity,
            price=price
        )
        
        # Print response
        click.echo(order_manager.format_order_response(response))
        
        # Print success message
        click.echo(
            click.style(
                f"\n✓ Order placed successfully! Order ID: {response.get('orderId')}",
                fg='green'
            )
        )
        
        logger.info(f"Order placement successful via CLI: {response}")
        
    except ValidationError as e:
        click.echo(
            click.style(
                f"\n✗ Validation Error: {str(e)}",
                fg='red'
            ),
            err=True
        )
        logger.error(f"Validation error: {e}")
        sys.exit(1)
        
    except BinanceAPIError as e:
        click.echo(
            click.style(
                f"\n✗ API Error: {str(e)}",
                fg='red'
            ),
            err=True
        )
        logger.error(f"API error: {e}")
        sys.exit(1)
        
    except Exception as e:
        click.echo(
            click.style(
                f"\n✗ Unexpected Error: {str(e)}",
                fg='red'
            ),
            err=True
        )
        logger.error(f"Unexpected error: {e}", exc_info=True)
        sys.exit(1)


@cli.command()
@click.option(
    '--symbol',
    prompt='Trading Symbol (e.g., BTCUSDT)',
    help='Trading symbol'
)
@click.option(
    '--order-id',
    prompt='Order ID',
    type=int,
    help='Order ID'
)
@click.option(
    '--api-key',
    envvar='BINANCE_API_KEY',
    help='Binance API Key'
)
@click.option(
    '--api-secret',
    envvar='BINANCE_API_SECRET',
    help='Binance API Secret'
)
def check_order(symbol: str, order_id: int, api_key: str, api_secret: str):
    """Check order status."""
    
    if not api_key or not api_secret:
        click.echo(
            click.style(
                "ERROR: API credentials not provided.",
                fg='red'
            ),
            err=True
        )
        sys.exit(1)
    
    try:
        client = BinanceClient(api_key, api_secret)
        response = client.get_order_status(symbol=symbol, order_id=order_id)
        
        click.echo("\n" + "=" * 60)
        click.echo("ORDER STATUS")
        click.echo("=" * 60)
        click.echo(f"Order ID:       {response.get('orderId')}")
        click.echo(f"Symbol:         {response.get('symbol')}")
        click.echo(f"Status:         {response.get('status')}")
        click.echo(f"Executed Qty:   {response.get('executedQty')}")
        click.echo(f"Avg Price:      {response.get('avgPrice')}")
        click.echo("=" * 60 + "\n")
        
        logger.info(f"Order status checked: {response}")
        
    except BinanceAPIError as e:
        click.echo(
            click.style(
                f"ERROR: {str(e)}",
                fg='red'
            ),
            err=True
        )
        sys.exit(1)


@cli.command()
@click.option(
    '--api-key',
    envvar='BINANCE_API_KEY',
    help='Binance API Key'
)
@click.option(
    '--api-secret',
    envvar='BINANCE_API_SECRET',
    help='Binance API Secret'
)
def test_connection(api_key: str, api_secret: str):
    """Test connection to Binance Futures Testnet."""
    
    if not api_key or not api_secret:
        click.echo(
            click.style(
                "ERROR: API credentials not provided.",
                fg='red'
            ),
            err=True
        )
        sys.exit(1)
    
    try:
        client = BinanceClient(api_key, api_secret)
        server_time = client.get_server_time()
        
        click.echo(
            click.style(
                f"\n✓ Connection successful! Server time: {server_time}",
                fg='green'
            )
        )
        logger.info("Connection test successful")
        
    except BinanceAPIError as e:
        click.echo(
            click.style(
                f"\n✗ Connection failed: {str(e)}",
                fg='red'
            ),
            err=True
        )
        sys.exit(1)


if __name__ == '__main__':
    cli()
