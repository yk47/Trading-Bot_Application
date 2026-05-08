# Trading Bot for Binance Futures Testnet

A clean, production-ready Python application for placing orders on Binance Futures Testnet (USDT-M Futures).

## Features

- ✓ Place **Market** and **Limit** orders
- ✓ Support for **BUY** and **SELL** sides
- ✓ Comprehensive input validation
- ✓ Structured API client with proper error handling
- ✓ Detailed logging with file rotation
- ✓ **CLI interface** with multiple commands
- ✓ **Web UI Dashboard** with Streamlit (NEW!)
- ✓ Environment variable support for API credentials
- ✓ Exception handling for network failures and API errors

## Project Structure

```
trading_bot/
├── bot/
│   ├── __init__.py              # Package initialization
│   ├── client.py                # Binance Futures API client
│   ├── orders.py                # Order placement logic
│   ├── validators.py            # Input validation
│   └── logging_config.py        # Logging configuration
├── cli.py                        # CLI entry point
├── app.py                        # Web UI (Streamlit)
├── requirements.txt              # Dependencies
├── .env.example                  # Environment variables template
├── README.md                     # This file
├── WEB_UI.md                     # Web UI documentation
└── logs/                         # Log files (auto-generated)
```

## Setup

### Prerequisites

- Python 3.8 or higher
- Binance Futures Testnet account
- API Key and Secret from testnet account

### 1. Register for Binance Futures Testnet

1. Go to https://testnet.binancefuture.com
2. Register a new account
3. Complete KYC if required
4. Generate API Key and Secret

### 2. Clone or Download Repository

```bash
cd trading_bot
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure API Credentials

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Edit `.env` and add your testnet API credentials:

```
BINANCE_API_KEY=your_api_key_here
BINANCE_API_SECRET=your_api_secret_here
```

**Security Note:** Never commit `.env` to version control. Use environment variables in production.

## Usage

### Option A: Web UI (Recommended for Easy Use)

```bash
streamlit run app.py
```

This opens a professional web dashboard where you can:
- ✓ Place orders with a visual form
- ✓ Check order status instantly
- ✓ View order history
- ✓ Export data to CSV/JSON

**See [WEB_UI.md](WEB_UI.md) for detailed web UI documentation.**

### Option B: CLI (Command Line)

#### 1. Test Connection

```bash
python cli.py test-connection
```

This verifies your API credentials are correct.

#### 2. Place a Market Order

```bash
python cli.py place-order --symbol BTCUSDT --side BUY --order-type MARKET --quantity 0.001
```

#### 3. Place a Limit Order

```bash
python cli.py place-order --symbol BTCUSDT --side SELL --order-type LIMIT --quantity 0.001 --price 45000
```

### 4. Check Order Status

```bash
python cli.py check-order --symbol BTCUSDT --order-id 12345678
```

### 5. Interactive Mode

Run without options for interactive prompts:

```bash
python cli.py place-order
```

You'll be prompted for:
- Trading Symbol (e.g., BTCUSDT)
- Order Side (BUY/SELL)
- Order Type (MARKET/LIMIT)
- Quantity
- Price (for LIMIT orders only)

## API Endpoints Used

The application uses the following Binance Futures Testnet endpoints:

- `GET /fapi/v1/time` - Get server time
- `GET /fapi/v1/exchangeInfo` - Get exchange information
- `POST /fapi/v1/order` - Place an order
- `GET /fapi/v1/order` - Get order status
- `DELETE /fapi/v1/order` - Cancel an order

Base URL: `https://testnet.binancefuture.com`

## Logging

All requests, responses, and errors are logged to `logs/trading_bot_YYYYMMDD_HHMMSS.log`.

Log files include:
- Timestamp of each operation
- API request/response details
- Validation errors
- Network errors
- Order execution details

## Error Handling

The application handles:

### Input Validation Errors
- Invalid symbol format
- Invalid order side (not BUY/SELL)
- Invalid order type (not MARKET/LIMIT)
- Invalid quantity or price (non-numeric, negative, zero)
- Missing price for LIMIT orders

### API Errors
- Network connection failures
- Invalid API credentials
- Insufficient balance
- Symbol not found
- API rate limiting

### Response Parsing
- Malformed JSON responses
- Missing fields in responses

## Example Output

### Successful Market Order

```
============================================================
ORDER REQUEST SUMMARY
============================================================
Symbol:       BTCUSDT
Side:         BUY
Order Type:   MARKET
Quantity:     0.001
============================================================

============================================================
ORDER RESPONSE
============================================================
Order ID:          123456789
Symbol:            BTCUSDT
Side:              BUY
Order Type:        MARKET
Status:            FILLED
Quantity:          0.001
Executed Qty:      0.001
Price:             0
Avg Price:         45234.5
Time in Force:     GTC
Update Time:       1234567890123
============================================================

✓ Order placed successfully! Order ID: 123456789
```

### Successful Limit Order

```
============================================================
ORDER REQUEST SUMMARY
============================================================
Symbol:       ETHUSDT
Side:         SELL
Order Type:   LIMIT
Quantity:     0.1
Price:        2500
============================================================

============================================================
ORDER RESPONSE
============================================================
Order ID:          987654321
Symbol:            ETHUSDT
Side:              SELL
Order Type:        LIMIT
Status:            NEW
Quantity:          0.1
Executed Qty:      0
Price:             2500
Avg Price:         0
Time in Force:     GTC
Update Time:       1234567890456
============================================================

✓ Order placed successfully! Order ID: 987654321
```

## Code Quality

- **Modular Structure**: Separate modules for client, orders, validation, and logging
- **Exception Handling**: Custom exceptions for API and validation errors
- **Logging**: Comprehensive logging with file rotation
- **Type Hints**: Full type annotations for better IDE support
- **Documentation**: Docstrings for all classes and methods
- **Input Validation**: Strict validation before API calls

## Testing

### Manual Testing Steps

1. **Connection Test**
   ```bash
   python cli.py test-connection
   ```
   Should show server time confirming connection works.

2. **Market Order Test**
   ```bash
   python cli.py place-order --symbol BTCUSDT --side BUY --order-type MARKET --quantity 0.001
   ```
   Should show order response with status FILLED.

3. **Limit Order Test**
   ```bash
   python cli.py place-order --symbol BTCUSDT --side SELL --order-type LIMIT --quantity 0.001 --price 50000
   ```
   Should show order response with status NEW.

4. **Validation Test**
   ```bash
   python cli.py place-order --symbol INVALID --side BUY --order-type MARKET --quantity 0.001
   ```
   Should show validation error.

5. **Check Logs**
   ```bash
   tail -f logs/trading_bot_*.log
   ```
   Should show detailed API interactions.

## Assumptions

1. **Testnet Only**: This application is configured for Binance Futures Testnet. Do NOT use with real money.
2. **Default Permissions**: Assumes API key has permissions for order placement.
3. **Decimal Precision**: Uses Python Decimal for precise price/quantity handling.
4. **UTC Timestamps**: All timestamps from API are in milliseconds UTC.
5. **Base Asset**: Assumes USDT margin for all futures pairs.
6. **API Rate Limits**: Respects Binance rate limits; implement exponential backoff for production use.

## Security Considerations

1. **Environment Variables**: Store API credentials in `.env` file (not committed to git)
2. **API Key Permissions**: On testnet, enable only necessary permissions
3. **Secret Storage**: Never hardcode API secret in code
4. **HTTPS Only**: All requests use HTTPS to the testnet
5. **Signature**: All signed requests use HMAC-SHA256

## Troubleshooting

### "API credentials not provided"
- Ensure `.env` file exists with BINANCE_API_KEY and BINANCE_API_SECRET
- Or use `--api-key` and `--api-secret` options

### "Connection failed"
- Verify internet connection
- Check Binance testnet status: https://testnet.binancefuture.com
- Verify API credentials are correct

### "Invalid symbol"
- Ensure symbol format is correct (e.g., BTCUSDT, not BTC-USDT)
- Check symbol exists on testnet

### "Insufficient balance"
- Testnet accounts start with demo funds
- If depleted, register a new account or contact Binance support

## Future Enhancements

- [ ] Stop-Loss and Take-Profit orders
- [ ] OCO (One-Cancels-Other) orders
- [ ] TWAP (Time-Weighted Average Price) execution
- [ ] Grid Trading
- [ ] Position management
- [ ] WebSocket support for real-time updates
- [ ] Database for order history
- [ ] Advanced CLI with menus and validation messages
- [ ] Dashboard/UI using Streamlit or similar

## Dependencies

- **requests** (2.31.0): HTTP library for API calls
- **click** (8.1.7): CLI framework
- **python-dotenv** (1.0.0): Environment variable management

## License

MIT License - Feel free to use this code for learning and development.

## Disclaimer

This application is for educational and testnet purposes only. Use at your own risk. The authors are not responsible for any losses incurred from using this software.

## Support

For issues or questions:
1. Check the README troubleshooting section
2. Review log files in `logs/` directory
3. Verify API credentials and Binance testnet status
4. Check Binance API documentation: https://binance-docs.github.io/apidocs/futures/en/

---

**Version**: 1.0.0  
**Last Updated**: 2024  
**Python**: 3.8+
