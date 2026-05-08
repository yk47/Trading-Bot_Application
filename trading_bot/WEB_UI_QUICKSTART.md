# 🌐 Web UI Quick Start

**Start your trading bot web dashboard in 30 seconds!**

## Quick Start (3 Steps)

### 1️⃣ **Install Updated Dependencies**
```bash
cd trading_bot
pip install -r requirements.txt
```

This adds:
- `streamlit` - Web framework
- `pandas` - Data handling

### 2️⃣ **Run the Web UI**
```bash
streamlit run app.py
```

Opens automatically at: `http://localhost:8501`

### 3️⃣ **Connect & Trade**
1. Enter your Binance testnet API Key & Secret in sidebar
2. Click "🔌 Connect" button
3. Go to "🛒 Place Order" tab
4. Fill in order details
5. Click "✅ Place Order"

Done! 🎉

---

## What You Get

### 📊 Dashboard Tab
- Real-time connection status
- Server time display
- Order statistics
- Quick action buttons

### 🛒 Place Order Tab
- Easy order form
- Market & Limit support
- Order summary preview
- Instant feedback

### 📋 Order Status Tab
- Check any order by ID
- View full details
- Formatted timestamps
- Real-time updates

### 📜 Order History Tab
- All orders from session
- Statistics dashboard
- Export to CSV/JSON
- Clear history option

---

## Example: Place Your First Order

1. **Start Web UI**
   ```bash
   streamlit run app.py
   ```

2. **Enter API Credentials** (Sidebar)
   - Paste your Binance testnet API Key
   - Paste your Binance testnet API Secret

3. **Click Connect** (Sidebar)
   - Wait for "✅ Connected" message

4. **Go to Place Order Tab**
   - Symbol: `BTCUSDT`
   - Side: `BUY`
   - Type: `MARKET`
   - Quantity: `0.001`

5. **Click Place Order**
   - See order response immediately
   - Order ID and status displayed

6. **View History**
   - Go to "Order History" tab
   - See your order in the table

---

## Commands Comparison

| Task | Web UI | CLI |
|------|--------|-----|
| **Place Order** | Click form → Submit | `python cli.py place-order ...` |
| **Check Status** | Input ID → View | `python cli.py check-order ...` |
| **View History** | Auto-tracked | Check logs/ |
| **Export Data** | Click Download | Manual |
| **Mobile Friendly** | ✅ Yes | ❌ No |
| **Ease of Use** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |

---

## Troubleshooting

### "No module named streamlit"
```bash
pip install streamlit==1.40.0
```

### "Cannot connect"
- Check API credentials are correct
- Verify Binance testnet is online
- Try clicking Connect again

### "Port 8501 already in use"
```bash
streamlit run app.py --server.port 8502
```

---

## Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `Ctrl+C` | Stop the app |
| `R` | Refresh page |
| `S` | Show settings |
| `Cmd+C` | Stop (Mac) |

---

## Browser Support

✅ Works on:
- Chrome
- Firefox
- Safari
- Edge
- Mobile browsers

---

## Next Steps

1. ✅ Install dependencies
2. ✅ Run `streamlit run app.py`
3. ✅ Connect with testnet credentials
4. ✅ Place test order
5. ✅ Check order history

**Full documentation**: [WEB_UI.md](WEB_UI.md)

---

## Tips & Tricks

### Quick Orders
Use dashboard quick buttons for common trades:
- 📈 Market Buy (0.001 BTC)
- 📉 Market Sell (0.001 BTC)
- 💹 ETH Limit Buy
- 💹 ETH Limit Sell

### Export Data
After trading session, export to Excel:
1. Go to Order History tab
2. Click "📥 Download as CSV"
3. Open in Excel

### Mobile Trading
Open on your phone/tablet:
```
http://localhost:8501
```

### Check Logs
While web UI is running:
```bash
tail -f logs/trading_bot_*.log
```

---

**You're ready to trade! 🚀**

Start with: `streamlit run app.py`
