"""Order placement logic."""
from decimal import Decimal
from typing import Dict, Any

from .client import BinanceClient, BinanceAPIError
from .validators import validate_order_params, ValidationError
from .logging_config import setup_logger

logger = setup_logger(__name__)


class OrderManager:
    """Manages order placement and tracking."""
    
    def __init__(self, client: BinanceClient):
        """
        Initialize order manager.
        
        Args:
            client: BinanceClient instance
        """
        self.client = client
        logger.info("OrderManager initialized")
    
    def place_order(
        self,
        symbol: str,
        side: str,
        order_type: str,
        quantity: str,
        price: str = None
    ) -> Dict[str, Any]:
        """
        Place an order with validation.
        
        Args:
            symbol: Trading symbol
            side: BUY or SELL
            order_type: MARKET or LIMIT
            quantity: Order quantity
            price: Order price (required for LIMIT)
            
        Returns:
            Order response
            
        Raises:
            ValidationError: If input validation fails
            BinanceAPIError: If API request fails
        """
        # Validate all parameters
        try:
            symbol, side, order_type, quantity, price = validate_order_params(
                symbol, side, order_type, quantity, price
            )
        except ValidationError as e:
            logger.error(f"Validation failed: {e}")
            raise
        
        # Place order with validated parameters
        try:
            response = self.client.place_order(
                symbol=symbol,
                side=side,
                order_type=order_type,
                quantity=quantity,
                price=price if order_type == 'LIMIT' else None
            )
            
            return response
            
        except BinanceAPIError as e:
            logger.error(f"Order placement failed: {e}")
            raise
    
    def format_order_response(self, response: Dict[str, Any]) -> str:
        """
        Format order response for display.
        
        Args:
            response: Order response from API
            
        Returns:
            Formatted string representation
        """
        lines = [
            "\n" + "=" * 60,
            "ORDER RESPONSE",
            "=" * 60,
            f"Order ID:          {response.get('orderId', 'N/A')}",
            f"Symbol:            {response.get('symbol', 'N/A')}",
            f"Side:              {response.get('side', 'N/A')}",
            f"Order Type:        {response.get('type', 'N/A')}",
            f"Status:            {response.get('status', 'N/A')}",
            f"Quantity:          {response.get('origQty', 'N/A')}",
            f"Executed Qty:      {response.get('executedQty', 'N/A')}",
            f"Price:             {response.get('price', 'N/A')}",
            f"Avg Price:         {response.get('avgPrice', 'N/A')}",
            f"Time in Force:     {response.get('timeInForce', 'N/A')}",
            f"Update Time:       {response.get('updateTime', 'N/A')}",
            "=" * 60,
        ]
        
        return "\n".join(lines)
