"""Input validation for trading bot."""
import re
from decimal import Decimal, InvalidOperation
from typing import Tuple

from .logging_config import setup_logger

logger = setup_logger(__name__)


class ValidationError(Exception):
    """Custom exception for validation errors."""
    pass


def validate_symbol(symbol: str) -> str:
    """
    Validate trading symbol format.
    
    Args:
        symbol: Trading symbol (e.g., BTCUSDT)
        
    Returns:
        Validated symbol in uppercase
        
    Raises:
        ValidationError: If symbol format is invalid
    """
    symbol = symbol.upper().strip()
    
    if not symbol:
        raise ValidationError("Symbol cannot be empty")
    
    # Basic pattern: must be alphanumeric, typically 6-12 chars
    if not re.match(r'^[A-Z0-9]{6,12}$', symbol):
        raise ValidationError(
            f"Invalid symbol format: {symbol}. Expected format like BTCUSDT"
        )
    
    logger.debug(f"Symbol validated: {symbol}")
    return symbol


def validate_side(side: str) -> str:
    """
    Validate order side.
    
    Args:
        side: BUY or SELL
        
    Returns:
        Validated side in uppercase
        
    Raises:
        ValidationError: If side is not BUY or SELL
    """
    side = side.upper().strip()
    
    if side not in ['BUY', 'SELL']:
        raise ValidationError(f"Side must be BUY or SELL, got: {side}")
    
    logger.debug(f"Side validated: {side}")
    return side


def validate_order_type(order_type: str) -> str:
    """
    Validate order type.
    
    Args:
        order_type: MARKET or LIMIT
        
    Returns:
        Validated order type in uppercase
        
    Raises:
        ValidationError: If order type is invalid
    """
    order_type = order_type.upper().strip()
    
    if order_type not in ['MARKET', 'LIMIT']:
        raise ValidationError(f"Order type must be MARKET or LIMIT, got: {order_type}")
    
    logger.debug(f"Order type validated: {order_type}")
    return order_type


def validate_quantity(quantity: str) -> Decimal:
    """
    Validate order quantity.
    
    Args:
        quantity: Order quantity as string
        
    Returns:
        Validated quantity as Decimal
        
    Raises:
        ValidationError: If quantity is invalid
    """
    try:
        qty = Decimal(quantity.strip())
    except (ValueError, InvalidOperation):
        raise ValidationError(f"Invalid quantity format: {quantity}")
    
    if qty <= 0:
        raise ValidationError(f"Quantity must be greater than 0, got: {qty}")
    
    logger.debug(f"Quantity validated: {qty}")
    return qty


def validate_price(price: str) -> Decimal:
    """
    Validate order price.
    
    Args:
        price: Order price as string
        
    Returns:
        Validated price as Decimal
        
    Raises:
        ValidationError: If price is invalid
    """
    try:
        p = Decimal(price.strip())
    except (ValueError, InvalidOperation):
        raise ValidationError(f"Invalid price format: {price}")
    
    if p <= 0:
        raise ValidationError(f"Price must be greater than 0, got: {p}")
    
    logger.debug(f"Price validated: {p}")
    return p


def validate_order_params(
    symbol: str,
    side: str,
    order_type: str,
    quantity: str,
    price: str = None
) -> Tuple[str, str, str, Decimal, Decimal]:
    """
    Validate all order parameters together.
    
    Args:
        symbol: Trading symbol
        side: BUY or SELL
        order_type: MARKET or LIMIT
        quantity: Order quantity
        price: Order price (required for LIMIT orders)
        
    Returns:
        Tuple of validated (symbol, side, order_type, quantity, price)
        
    Raises:
        ValidationError: If any parameter is invalid
    """
    logger.debug(f"Validating order params: symbol={symbol}, side={side}, "
                 f"order_type={order_type}, quantity={quantity}, price={price}")
    
    # Validate required params
    symbol = validate_symbol(symbol)
    side = validate_side(side)
    order_type = validate_order_type(order_type)
    quantity = validate_quantity(quantity)
    
    # For LIMIT orders, price is required
    if order_type == 'LIMIT':
        if not price:
            raise ValidationError("Price is required for LIMIT orders")
        price = validate_price(price)
    else:
        # MARKET orders don't need price, set to 0
        price = Decimal('0')
    
    logger.debug("All order parameters validated successfully")
    return symbol, side, order_type, quantity, price
