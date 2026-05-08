#!/usr/bin/env python3
"""
Demo script showing example usage of the trading bot.

This script demonstrates:
1. Importing the trading bot modules
2. Initializing the client and order manager
3. Placing market and limit orders
4. Handling errors
"""

import os
import sys
from dotenv import load_dotenv
from pathlib import Path

# Add parent directory to path so we can import bot module
sys.path.insert(0, str(Path(__file__).parent))

from bot.client import BinanceClient, BinanceAPIError
from bot.orders import OrderManager
from bot.validators import ValidationError
from bot.logging_config import setup_logger

logger = setup_logger(__name__)


def demo_place_market_order(client: BinanceClient):
    """Demo: Place a market order."""
    print("\n" + "=" * 60)
    print("DEMO 1: MARKET ORDER")
    print("=" * 60)
    
    try:
        order_manager = OrderManager(client)
        
        # Place market order
        response = order_manager.place_order(
            symbol="BTCUSDT",
            side="BUY",
            order_type="MARKET",
            quantity="0.001",
            price=None
        )
        
        print(order_manager.format_order_response(response))
        print("✓ Market order placed successfully!")
        
        return response
        
    except ValidationError as e:
        print(f"✗ Validation Error: {e}")
        return None
    except BinanceAPIError as e:
        print(f"✗ API Error: {e}")
        return None
    except Exception as e:
        print(f"✗ Unexpected Error: {e}")
        return None


def demo_place_limit_order(client: BinanceClient):
    """Demo: Place a limit order."""
    print("\n" + "=" * 60)
    print("DEMO 2: LIMIT ORDER")
    print("=" * 60)
    
    try:
        order_manager = OrderManager(client)
        
        # Place limit order
        response = order_manager.place_order(
            symbol="ETHUSDT",
            side="SELL",
            order_type="LIMIT",
            quantity="0.1",
            price="2500"
        )
        
        print(order_manager.format_order_response(response))
        print("✓ Limit order placed successfully!")
        
        return response
        
    except ValidationError as e:
        print(f"✗ Validation Error: {e}")
        return None
    except BinanceAPIError as e:
        print(f"✗ API Error: {e}")
        return None
    except Exception as e:
        print(f"✗ Unexpected Error: {e}")
        return None


def demo_validation_errors():
    """Demo: Show validation errors."""
    print("\n" + "=" * 60)
    print("DEMO 3: VALIDATION ERRORS")
    print("=" * 60)
    
    from bot.validators import (
        validate_symbol,
        validate_side,
        validate_order_type,
        validate_quantity,
        validate_price
    )
    
    test_cases = [
        ("Invalid symbol", lambda: validate_symbol("INVALID"), "validate_symbol"),
        ("Invalid side", lambda: validate_side("BYY"), "validate_side"),
        ("Invalid order type", lambda: validate_order_type("UNKNOWN"), "validate_order_type"),
        ("Invalid quantity (zero)", lambda: validate_quantity("0"), "validate_quantity"),
        ("Invalid quantity (negative)", lambda: validate_quantity("-1"), "validate_quantity"),
        ("Invalid price format", lambda: validate_price("abc"), "validate_price"),
        ("Invalid price (zero)", lambda: validate_price("0"), "validate_price"),
    ]
    
    for test_name, test_func, validator_name in test_cases:
        try:
            test_func()
            print(f"✗ {test_name}: Should have raised ValidationError")
        except ValidationError as e:
            print(f"✓ {test_name}: {e}")
        except Exception as e:
            print(f"? {test_name}: Unexpected error: {e}")


def demo_test_connection(client: BinanceClient):
    """Demo: Test connection to API."""
    print("\n" + "=" * 60)
    print("DEMO 4: TEST CONNECTION")
    print("=" * 60)
    
    try:
        server_time = client.get_server_time()
        print(f"✓ Connected to Binance testnet!")
        print(f"  Server time: {server_time}")
        return True
    except BinanceAPIError as e:
        print(f"✗ Connection failed: {e}")
        return False


def main():
    """Main demo function."""
    
    # Load environment variables
    load_dotenv()
    
    api_key = os.getenv("BINANCE_API_KEY")
    api_secret = os.getenv("BINANCE_API_SECRET")
    
    print("=" * 60)
    print("Trading Bot Demo")
    print("=" * 60)
    
    # Check if API credentials are available
    if not api_key or not api_secret:
        print("\n⚠ API credentials not found in .env file")
        print("To run the actual order placement demos:")
        print("1. Create a .env file with BINANCE_API_KEY and BINANCE_API_SECRET")
        print("2. Or run: python setup.py")
        print("\nRunning validation demos only...\n")
        
        # Run validation demo
        demo_validation_errors()
        
        print("\n" + "=" * 60)
        print("Demo Complete!")
        print("=" * 60)
        print("\nFor full functionality, please set up your API credentials.")
        return
    
    # Initialize client
    try:
        client = BinanceClient(api_key, api_secret)
    except ValueError as e:
        print(f"Error: {e}")
        return
    
    # Run demos
    # Demo 1: Test connection
    if not demo_test_connection(client):
        print("\nCannot continue with order placement demos - connection failed")
        return
    
    # Demo 2: Validation
    demo_validation_errors()
    
    # Demo 3: Market order
    demo_place_market_order(client)
    
    # Demo 4: Limit order
    demo_place_limit_order(client)
    
    # Final message
    print("\n" + "=" * 60)
    print("Demo Complete!")
    print("=" * 60)
    print("\nCheck logs/ directory for detailed API interaction logs")
    print("For CLI usage, run: python cli.py --help")


if __name__ == "__main__":
    main()
