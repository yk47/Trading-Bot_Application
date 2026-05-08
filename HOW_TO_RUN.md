# 🚀 How to Run Trading Bot

**Everything you need to get trading!**

---

## ⚡ Quick Start (Choose One)

### Option 1: Web UI (Easiest) 🌐

```bash
cd trading_bot
pip install -r requirements.txt
streamlit run app.py
```

Opens dashboard at: `http://localhost:8501`

[Full Guide](WEB_UI_QUICKSTART.md)

### Option 2: Command Line (CLI)

```bash
cd trading_bot
pip install -r requirements.txt
python cli.py place-order
```

[Full Guide](QUICKSTART.md)

---

## 📋 Step-by-Step Setup

### 1. Get Binance Testnet Account

1. Go to https://testnet.binancefuture.com
2. Register new account
3. Verify email
4. Go to Account → API Management
5. Create new API Key
6. **Copy API Key and Secret** (save securely!)

### 2. Install Python Dependencies

```bash
cd trading_bot
pip install -r requirements.txt
```

This installs:
- `requests` - HTTP library
- `click` - CLI framework
- `python-dotenv` - Environment variables
- `streamlit` - Web framework (NEW!)
- `pandas` - Data handling (NEW!)

### 3. Set Up API Credentials

**Option A: Environment File (.env)**
```bash
# Create .env file in trading_bot/
BINANCE_API_KEY=your_key_here
BINANCE_API_SECRET=your_secret_here
```

**Option B: Web UI (Recommended)**
1. Run: `streamlit run app.py`
2. Enter credentials in sidebar
3. Click Connect

---

## 🌐 WEB UI (Recommended)

### Start the Dashboard

```bash
cd trading_bot
streamlit run app.py
```

### What You Can Do

✅ **Place Orders**
- Market orders (BUY/SELL)
- Limit orders with price
- Real-time feedback
- Order ID confirmation

✅ **Check Status**
- Enter order ID
- View full details
- Execution info
- Timestamps

✅ **Track History**
- All orders from session
- Statistics dashboard
- Export to CSV/JSON
- Clear history

✅ **Dashboard**
- Connection status
- Server time
- Order count
- Quick action buttons

### Example Workflow

```
1. streamlit run app.py
2. Enter API credentials
3. Click "Connect"
4. Click "Place Order" tab
5. Fill in order details
6. Click "Place Order"
7. See confirmation
8. Check "Order History" tab
```

[Web UI Guide](WEB_UI.md)

---

## 💻 CLI (Command Line)

### Test Connection

```bash
python cli.py test-connection
```

### Place Market Order

```bash
python cli.py place-order \
  --symbol BTCUSDT \
  --side BUY \
  --order-type MARKET \
  --quantity 0.001
```

### Place Limit Order

```bash
python cli.py place-order \
  --symbol ETHUSDT \
  --side SELL \
  --order-type LIMIT \
  --quantity 0.1 \
  --price 2500
```

### Check Order Status

```bash
python cli.py check-order \
  --symbol BTCUSDT \
  --order-id 123456789
```

### Interactive Mode

```bash
python cli.py place-order
# Then follow prompts for: symbol, side, type, quantity, price
```

### Get Help

```bash
python cli.py --help
python cli.py place-order --help
```

[CLI Guide](QUICKSTART.md)

---

## 🎯 Which to Choose?

### Use **Web UI** if you want:
- ✅ Easy visual interface
- ✅ Mobile-friendly dashboard
- ✅ Order history tracking
- ✅ Data export (CSV/JSON)
- ✅ Real-time feedback
- ✅ No command line knowledge needed

### Use **CLI** if you want:
- ✅ Faster order placement
- ✅ Scriptable/automated
- ✅ Lightweight
- ✅ Terminal-based
- ✅ Direct control

**Recommendation**: Start with **Web UI**, it's easier! 🌐

---

## 📊 Features Comparison

| Feature | Web UI | CLI |
|---------|--------|-----|
| Place orders | ✅ | ✅ |
| Check status | ✅ | ✅ |
| Limit orders | ✅ | ✅ |
| Market orders | ✅ | ✅ |
| Order history | ✅ | ⭕ |
| Export data | ✅ | ❌ |
| Visual interface | ✅ | ❌ |
| Mobile friendly | ✅ | ⭕ |
| Command line | ❌ | ✅ |
| Scriptable | ⭕ | ✅ |

---

## 🧪 Testing

### Test Market Order

**Web UI:**
1. Go to "Place Order"
2. Symbol: BTCUSDT
3. Side: BUY
4. Type: MARKET
5. Quantity: 0.001
6. Click "Place Order"

**CLI:**
```bash
python cli.py place-order \
  --symbol BTCUSDT \
  --side BUY \
  --order-type MARKET \
  --quantity 0.001
```

### Test Limit Order

**Web UI:**
1. Go to "Place Order"
2. Symbol: ETHUSDT
3. Side: SELL
4. Type: LIMIT
5. Quantity: 0.1
6. Price: 2500
7. Click "Place Order"

**CLI:**
```bash
python cli.py place-order \
  --symbol ETHUSDT \
  --side SELL \
  --order-type LIMIT \
  --quantity 0.1 \
  --price 2500
```

---

## 📁 Project Structure

```
trading_bot/
├── app.py                    ← Web UI (run with: streamlit run app.py)
├── cli.py                    ← CLI (run with: python cli.py)
├── setup.py                  ← Interactive setup
├── demo.py                   ← Demo code
├── requirements.txt          ← Dependencies
├── .env.example              ← Credentials template
├── bot/                      ← Core package
│   ├── client.py             (API client)
│   ├── orders.py             (Order logic)
│   ├── validators.py         (Validation)
│   └── logging_config.py     (Logging)
├── logs/                     ← Order logs
├── README.md                 ← Full documentation
├── WEB_UI.md                 ← Web UI guide
├── WEB_UI_QUICKSTART.md      ← Web UI quick start
└── QUICKSTART.md             ← CLI quick start
```

---

## 🔐 Security

### Important!

1. **Never share your API Secret**
   - Keep it private
   - Don't commit .env to git
   - Don't share screenshots with it

2. **Use Testnet Only**
   - This is for learning
   - No real money
   - Safe to experiment

3. **Protect Your Account**
   - Monitor for unauthorized access
   - Rotate API keys regularly
   - Use IP whitelist if available

---

## ⚠️ Troubleshooting

### "No module named streamlit"
```bash
pip install streamlit==1.40.0
```

### "No module named dotenv"
```bash
pip install python-dotenv==1.0.0
```

### "API credentials not provided"
- Create .env file with BINANCE_API_KEY and BINANCE_API_SECRET
- Or enter in Web UI sidebar

### "Connection failed"
- Verify API credentials are correct
- Check testnet.binancefuture.com is online
- Check your internet connection
- Try again in a moment

### "Port 8501 already in use"
```bash
streamlit run app.py --server.port 8502
```

### "ModuleNotFoundError"
```bash
pip install -r requirements.txt
```

---

## 📞 Getting Help

### Documentation
- **[README.md](README.md)** - Full guide
- **[WEB_UI.md](WEB_UI.md)** - Web UI documentation
- **[QUICKSTART.md](QUICKSTART.md)** - Quick start guide

### Logs
Check `logs/` directory for detailed activity:
```bash
cat logs/trading_bot_*.log
```

### Issues
1. Check README.md troubleshooting section
2. Review log files
3. Verify API credentials
4. Check Binance testnet status

---

## 🚀 Next Steps

### To Get Started Right Now:

```bash
# 1. Navigate to project
cd trading_bot

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run Web UI (Easiest!)
streamlit run app.py

# 4. In the web interface:
#    - Enter API credentials
#    - Click "Connect"
#    - Place your first order!
```

### Or Use CLI:

```bash
# 1. Navigate to project
cd trading_bot

# 2. Install dependencies
pip install -r requirements.txt

# 3. Test connection
python cli.py test-connection

# 4. Place an order
python cli.py place-order --symbol BTCUSDT --side BUY --order-type MARKET --quantity 0.001
```

---

## ✅ Checklist

- [ ] Python 3.8+ installed
- [ ] Binance testnet account created
- [ ] API Key and Secret obtained
- [ ] `pip install -r requirements.txt` run
- [ ] `.env` file created (or use Web UI)
- [ ] Connection test successful
- [ ] First order placed
- [ ] Order confirmation seen
- [ ] History exported (optional)

---

## 🎉 You're Ready!

Choose your approach:

**🌐 Start with Web UI:**
```bash
streamlit run app.py
```

**💻 Or use CLI:**
```bash
python cli.py place-order
```

**Questions?** Read [README.md](README.md) or [WEB_UI.md](WEB_UI.md)

Good luck trading! 🚀

---

*Last updated: May 2024*  
*Version: 1.0.0*
