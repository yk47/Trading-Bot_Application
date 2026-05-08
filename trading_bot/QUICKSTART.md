# Quick Start Guide

Get your trading bot up and running in 5 minutes!

## Prerequisites

- Python 3.8 or higher
- Binance Futures Testnet account (register at https://testnet.binancefuture.com)
- API Key and Secret from your testnet account

## Step 1: Get Your API Credentials (2 minutes)

1. Go to https://testnet.binancefuture.com
2. Sign in or create a new account
3. Click on your profile icon → API Management
4. Create a new API key
5. Copy your API Key and API Secret (keep the secret safe!)

## Step 2: Set Up the Project (2 minutes)

### Windows

```bash
# Clone or download the project
cd trading_bot

# Run the interactive setup
python setup.py
```

### macOS / Linux

```bash
cd trading_bot
python3 setup.py
```

The setup script will:
- ✓ Create a Python virtual environment
- ✓ Install dependencies
- ✓ Ask for your API credentials and create `.env` file

## Step 3: Test Your Connection (1 minute)

```bash
# Activate virtual environment first

# Windows
.\venv\Scripts\activate

# macOS/Linux
source venv/bin/activate

# Test connection
python cli.py test-connection
```

You should see:
```
✓ Connection successful! Server time: 1715163047234
```

## Step 4: Place Your First Order (1 minute)

### Market Order (BUY)

```bash
python cli.py place-order \
  --symbol BTCUSDT \
  --side BUY \
  --order-type MARKET \
  --quantity 0.001
```

### Limit Order (SELL)

```bash
python cli.py place-order \
  --symbol ETHUSDT \
  --side SELL \
  --order-type LIMIT \
  --quantity 0.1 \
  --price 2500
```

### Interactive Mode

```bash
python cli.py place-order
```

Just follow the prompts!

## Check Logs

View all API interactions:

```bash
# View latest log
type logs\trading_bot_*.log              # Windows
cat logs/trading_bot_*.log               # macOS/Linux

# Monitor live (macOS/Linux)
tail -f logs/trading_bot_*.log
```

## Common Commands

```bash
# Test connection
python cli.py test-connection

# Place order (with prompts)
python cli.py place-order

# Place order (with parameters)
python cli.py place-order --symbol BTCUSDT --side BUY --order-type MARKET --quantity 0.001

# Check order status
python cli.py check-order --symbol BTCUSDT --order-id 123456789

# Get help
python cli.py --help
python cli.py place-order --help
```

## Example Output

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
Order ID:          9876543210
Symbol:            BTCUSDT
Side:              BUY
Order Type:        MARKET
Status:            FILLED
Quantity:          0.001
Executed Qty:      0.001
Price:             0
Avg Price:         45234.5
Time in Force:     GTC
Update Time:       1715163047234
============================================================

✓ Order placed successfully! Order ID: 9876543210
```

## Troubleshooting

### "API credentials not provided"
- Make sure `.env` file exists with `BINANCE_API_KEY` and `BINANCE_API_SECRET`
- Or run `python setup.py` to create it

### "Connection failed"
- Check your internet connection
- Verify API credentials are correct
- Check if Binance testnet is online: https://testnet.binancefuture.com

### "Invalid symbol"
- Use correct format (e.g., `BTCUSDT`, not `BTC-USDT`)
- Check symbol exists on testnet

### "Virtual environment not activated"
- Windows: Run `.\venv\Scripts\activate`
- macOS/Linux: Run `source venv/bin/activate`

## Next Steps

1. ✓ Test with small quantities first
2. ✓ Review logs to understand API interactions
3. ✓ Check [README.md](README.md) for advanced usage
4. ✓ Explore the [demo.py](demo.py) script for code examples

## Security Reminders

- ⚠️ Never share your `.env` file
- ⚠️ Never commit `.env` to git
- ⚠️ This is testnet only - for learning purposes
- ⚠️ Start with small quantities to test

---

You're all set! Questions? Check [README.md](README.md) for detailed documentation.
