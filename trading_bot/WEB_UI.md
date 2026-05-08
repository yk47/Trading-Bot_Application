# 🌐 Trading Bot Web UI

A professional web interface for the Trading Bot using Streamlit.

## Features

✨ **Web Dashboard**
- Real-time connection status
- Server time display
- Order count statistics

📊 **Dashboard Tab**
- Connection status
- Server information
- Quick action buttons for common orders

🛒 **Place Order Tab**
- Easy-to-use order form
- Market and Limit order support
- Order summary before placing
- Real-time feedback and order details

📋 **Order Status Tab**
- Check any order by symbol and order ID
- View full order details
- Order execution information

📜 **Order History Tab**
- Track all orders placed in current session
- Statistics (total, buy, sell, filled)
- Export to CSV or JSON
- Clear history

## Installation

### Step 1: Install Dependencies

```bash
cd trading_bot
pip install -r requirements.txt
```

This will install:
- `streamlit` - Web framework
- `pandas` - Data manipulation
- Plus all existing dependencies (requests, click, python-dotenv)

### Step 2: Set Up API Credentials

Create a `.env` file in the `trading_bot/` directory:

```bash
# Create .env file
BINANCE_API_KEY=your_api_key_here
BINANCE_API_SECRET=your_api_secret_here
```

Or enter them in the web UI sidebar.

## Running the Web UI

```bash
cd trading_bot
streamlit run app.py
```

This will:
1. Start the Streamlit server
2. Open your browser to `http://localhost:8501`
3. Show the trading bot web interface

## Using the Web UI

### 1. Connect to Binance

1. In the sidebar, enter your API Key and Secret
2. Click the "🔌 Connect" button
3. Wait for connection confirmation

### 2. Place an Order

**Via Quick Links (Dashboard Tab):**
- Click one of the quick action buttons
- Review the form that appears
- Click "✅ Place Order"

**Via Place Order Form:**
1. Go to "🛒 Place Order" tab
2. Enter symbol (e.g., BTCUSDT)
3. Select side (BUY/SELL)
4. Choose order type (MARKET/LIMIT)
5. Enter quantity
6. For LIMIT orders, enter price
7. Review order summary
8. Click "✅ Place Order"

### 3. Check Order Status

1. Go to "📋 Order Status" tab
2. Enter symbol and order ID
3. Click "🔍 Check Status"
4. View full order details

### 4. View Order History

1. Go to "📜 Order History" tab
2. See all orders from current session
3. View statistics
4. Export data as CSV or JSON

## Example Workflow

```
1. Start Streamlit:        streamlit run app.py
2. Connect:                Enter API credentials + Click Connect
3. Place order:            Fill form + Click Place Order
4. Check status:           Enter order ID + Check Status
5. View history:           Go to Order History tab
6. Export data:            Click Download CSV/JSON
```

## Features in Detail

### Dashboard Tab
- Real-time connection status (🟢 Connected / 🔴 Disconnected)
- Server time synchronization
- Quick action buttons for common trades
- Jump to place order with pre-filled values

### Place Order Tab
- Symbol input with validation
- Side selection (BUY/SELL)
- Order type selection (MARKET/LIMIT)
- Quantity input with decimal support
- Price input (only for LIMIT orders)
- Order summary preview
- Place, Reset, and Clear buttons
- Detailed response with order ID and status

### Order Status Tab
- Symbol and order ID input
- Real-time order details
- Formatted timestamps
- Full order information table
- Price, quantity, and execution details

### Order History Tab
- All orders from current session
- Statistics dashboard
- Sortable, searchable data table
- Export to CSV
- Export to JSON
- Clear history function

## Keyboard Shortcuts

- `Ctrl+C` in terminal to stop the app
- `Cmd+C` on Mac to stop the app

## Troubleshooting

### "No module named streamlit"
```bash
pip install streamlit==1.40.0
```

### "API credentials not provided"
- Enter API credentials in the sidebar
- Make sure they're from Binance Futures Testnet
- Click Connect button

### "Connection Failed"
- Verify API credentials are correct
- Check Binance testnet status: https://testnet.binancefuture.com
- Check your internet connection

### "ModuleNotFoundError"
```bash
pip install -r requirements.txt
```

## Configuration

### Environment Variables
Create `.env` file for auto-loading credentials:
```
BINANCE_API_KEY=your_key
BINANCE_API_SECRET=your_secret
```

### Streamlit Config
For advanced configuration, create `.streamlit/config.toml`:
```toml
[browser]
gatherUsageStats = false

[server]
port = 8501
```

## Security Notes

⚠️ **IMPORTANT:**
- Never share your API credentials
- Never commit `.env` to version control
- Use testnet only for learning
- For production: rotate API keys regularly
- Monitor your testnet account for unauthorized access

## Browser Compatibility

✅ Works with:
- Chrome/Chromium
- Firefox
- Safari
- Edge
- Any modern browser

## Performance

- Fast load times (< 1 second)
- Real-time updates
- Responsive design
- Works on mobile devices

## Advanced Usage

### Batch Operations
1. Place multiple orders
2. Check each one in the Order Status tab
3. Export all results to CSV

### Order Tracking
1. Place order and note the Order ID
2. Come back later to check status
3. Use Order History for complete audit trail

### Data Analysis
1. Export order history to CSV
2. Import to Excel or Python pandas
3. Analyze trading patterns

## Terminal vs Web UI

**CLI (Command Line):**
```bash
python cli.py place-order --symbol BTCUSDT --side BUY --order-type MARKET --quantity 0.001
```

**Web UI:**
1. Go to "Place Order" tab
2. Fill form
3. Click "Place Order"

Both work identically - choose what's comfortable for you!

## Next Steps

1. ✅ Start the web UI: `streamlit run app.py`
2. ✅ Connect with your testnet credentials
3. ✅ Place your first test order
4. ✅ Check order status
5. ✅ Export order history

## Support

- 📖 Read [README.md](README.md) for full documentation
- 💻 Check [QUICKSTART.md](QUICKSTART.md) for quick start
- 🐛 Review logs in `logs/` directory for debugging

## Features Comparison

| Feature | CLI | Web UI |
|---------|-----|--------|
| Place orders | ✅ | ✅ |
| Check status | ✅ | ✅ |
| Input validation | ✅ | ✅ |
| Visual feedback | ⭕ | ✅ |
| Order history | 📝 | ✅ |
| Export data | ⭕ | ✅ |
| Ease of use | ⭕ | ✅ |
| Mobile friendly | ❌ | ✅ |

---

**Version:** 1.0.0  
**Status:** Production Ready  
**Framework:** Streamlit 1.40.0
