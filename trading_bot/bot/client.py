"""Binance Futures API client."""
import hmac
import hashlib
import time
import json
from typing import Optional, Dict, Any
from decimal import Decimal
from urllib.parse import urlencode

import requests

from .logging_config import setup_logger
from .validators import ValidationError

logger = setup_logger(__name__)


class BinanceAPIError(Exception):
    """Exception for Binance API errors."""
    pass


class BinanceClient:
    """Client for Binance Futures Testnet API."""
    
    BASE_URL = "https://testnet.binancefuture.com"
    
    def __init__(self, api_key: str, api_secret: str):
        """
        Initialize Binance client.
        
        Args:
            api_key: Binance API key
            api_secret: Binance API secret
            
        Raises:
            ValueError: If API credentials are not provided
        """
        if not api_key or not api_secret:
            raise ValueError("API key and secret must be provided")
        
        self.api_key = api_key
        self.api_secret = api_secret
        self.session = requests.Session()
        
        logger.info(f"BinanceClient initialized for testnet: {self.BASE_URL}")
    
    def _get_request_headers(self) -> Dict[str, str]:
        """Get headers for authenticated requests."""
        return {
            "X-MBX-APIKEY": self.api_key,
            "Content-Type": "application/json"
        }
    
    def _generate_signature(self, params: Dict[str, Any]) -> str:
        """Generate request signature."""
        query_string = urlencode(params)
        signature = hmac.new(
            self.api_secret.encode('utf-8'),
            query_string.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        return signature
    
    def _request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        signed: bool = False
    ) -> Dict[str, Any]:
        """
        Make HTTP request to Binance API.
        
        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint path
            params: Request parameters
            signed: Whether to sign the request
            
        Returns:
            JSON response from API
            
        Raises:
            BinanceAPIError: If API request fails
        """
        url = f"{self.BASE_URL}{endpoint}"
        params = params or {}
        
        # Add timestamp for signed requests
        if signed:
            params['timestamp'] = int(time.time() * 1000)
            params['signature'] = self._generate_signature(params)
        
        headers = self._get_request_headers()
        
        logger.debug(f"{method} {endpoint} with params: {self._mask_sensitive_params(params)}")
        
        try:
            if method == "GET":
                response = self.session.get(url, params=params, headers=headers)
            elif method == "POST":
                response = self.session.post(url, params=params, headers=headers)
            elif method == "DELETE":
                response = self.session.delete(url, params=params, headers=headers)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            
            response.raise_for_status()
            
            data = response.json()
            logger.debug(f"Response: {data}")
            
            return data
            
        except requests.exceptions.RequestException as e:
            error_msg = f"API request failed: {str(e)}"
            if hasattr(e.response, 'text'):
                try:
                    error_data = e.response.json()
                    error_msg += f" - {error_data}"
                except:
                    error_msg += f" - {e.response.text}"
            
            logger.error(error_msg)
            raise BinanceAPIError(error_msg) from e
    
    @staticmethod
    def _mask_sensitive_params(params: Dict[str, Any]) -> Dict[str, Any]:
        """Mask sensitive parameters for logging."""
        masked = params.copy()
        if 'signature' in masked:
            masked['signature'] = '***'
        return masked
    
    def get_server_time(self) -> int:
        """
        Get server time from Binance.
        
        Returns:
            Server time in milliseconds
        """
        try:
            data = self._request("GET", "/fapi/v1/time")
            return data['serverTime']
        except BinanceAPIError as e:
            logger.error(f"Failed to get server time: {e}")
            raise
    
    def get_exchange_info(self, symbol: str) -> Dict[str, Any]:
        """
        Get exchange info for a symbol.
        
        Args:
            symbol: Trading symbol
            
        Returns:
            Exchange info data
        """
        try:
            data = self._request("GET", "/fapi/v1/exchangeInfo", params={"symbol": symbol})
            return data
        except BinanceAPIError as e:
            logger.error(f"Failed to get exchange info for {symbol}: {e}")
            raise
    
    def place_order(
        self,
        symbol: str,
        side: str,
        order_type: str,
        quantity: Decimal,
        price: Decimal = None
    ) -> Dict[str, Any]:
        """
        Place an order on Binance Futures.
        
        Args:
            symbol: Trading symbol (e.g., BTCUSDT)
            side: BUY or SELL
            order_type: MARKET or LIMIT
            quantity: Order quantity
            price: Order price (required for LIMIT orders)
            
        Returns:
            Order response from API
            
        Raises:
            BinanceAPIError: If order placement fails
            ValidationError: If parameters are invalid
        """
        params = {
            'symbol': symbol,
            'side': side,
            'type': order_type,
            'quantity': str(quantity)
        }
        
        if order_type == 'LIMIT':
            if not price or price <= 0:
                raise ValidationError("Price must be provided and greater than 0 for LIMIT orders")
            params['price'] = str(price)
            params['timeInForce'] = 'GTC'  # Good Till Cancel
        
        logger.info(f"Placing {order_type} order: {symbol} {side} {quantity}")
        
        try:
            response = self._request(
                "POST",
                "/fapi/v1/order",
                params=params,
                signed=True
            )
            
            logger.info(f"Order placed successfully: orderId={response.get('orderId')}, "
                       f"status={response.get('status')}, executedQty={response.get('executedQty')}")
            
            return response
            
        except BinanceAPIError as e:
            logger.error(f"Failed to place order: {e}")
            raise
    
    def get_order_status(
        self,
        symbol: str,
        order_id: int = None,
        orig_client_order_id: str = None
    ) -> Dict[str, Any]:
        """
        Get order status.
        
        Args:
            symbol: Trading symbol
            order_id: Order ID
            orig_client_order_id: Client order ID
            
        Returns:
            Order details
        """
        params = {'symbol': symbol}
        if order_id:
            params['orderId'] = order_id
        elif orig_client_order_id:
            params['origClientOrderId'] = orig_client_order_id
        else:
            raise ValueError("Either orderId or origClientOrderId must be provided")
        
        try:
            return self._request(
                "GET",
                "/fapi/v1/order",
                params=params,
                signed=True
            )
        except BinanceAPIError as e:
            logger.error(f"Failed to get order status: {e}")
            raise
    
    def cancel_order(
        self,
        symbol: str,
        order_id: int = None,
        orig_client_order_id: str = None
    ) -> Dict[str, Any]:
        """
        Cancel an order.
        
        Args:
            symbol: Trading symbol
            order_id: Order ID
            orig_client_order_id: Client order ID
            
        Returns:
            Cancelled order details
        """
        params = {'symbol': symbol}
        if order_id:
            params['orderId'] = order_id
        elif orig_client_order_id:
            params['origClientOrderId'] = orig_client_order_id
        else:
            raise ValueError("Either orderId or origClientOrderId must be provided")
        
        logger.info(f"Cancelling order: {symbol} orderId={order_id}")
        
        try:
            return self._request(
                "DELETE",
                "/fapi/v1/order",
                params=params,
                signed=True
            )
        except BinanceAPIError as e:
            logger.error(f"Failed to cancel order: {e}")
            raise
