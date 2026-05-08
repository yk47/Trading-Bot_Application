# Contributing to Trading Bot

Thank you for interest in contributing! This document provides guidelines for contributions.

## Development Setup

### 1. Fork and Clone

```bash
git clone <your-fork-url>
cd trading_bot
python setup.py
```

### 2. Create a Feature Branch

```bash
git checkout -b feature/your-feature-name
```

### 3. Development Workflow

```bash
# Activate virtual environment
source venv/bin/activate  # or .\venv\Scripts\activate on Windows

# Make changes
# Test your changes
python cli.py test-connection
python demo.py

# Check logs
tail -f logs/trading_bot_*.log
```

## Code Style

- Use PEP 8 style guide
- Add type hints to functions
- Document all public methods with docstrings
- Use descriptive variable names
- Keep functions focused and small

## Testing

Before submitting a PR, ensure:

1. ✓ Code runs without errors
2. ✓ API credentials are properly handled
3. ✓ Logging works correctly
4. ✓ Input validation catches invalid inputs
5. ✓ Error messages are helpful

### Manual Testing Checklist

```bash
# Test connection
python cli.py test-connection

# Test market order
python cli.py place-order --symbol BTCUSDT --side BUY --order-type MARKET --quantity 0.001

# Test limit order
python cli.py place-order --symbol ETHUSDT --side SELL --order-type LIMIT --quantity 0.1 --price 2500

# Test validation
python cli.py place-order --symbol INVALID --side BUY --order-type MARKET --quantity 0.001

# View logs
ls logs/
```

## Commit Message Guidelines

Use clear, descriptive commit messages:

```
Good: "Add support for OCO orders"
Bad: "Fix bug"

Good: "Improve error handling for network failures"
Bad: "Update code"
```

## Pull Request Process

1. Update [README.md](README.md) with any new features or changes
2. Ensure all tests pass
3. Include clear description of changes
4. Reference any related issues

## Adding New Features

### Example: Adding Stop-Limit Orders

1. Update `validators.py` to accept new order type
2. Update `client.py` with API parameters for new order type
3. Update `orders.py` to handle new order type logic
4. Update `cli.py` with new command or option
5. Update [README.md](README.md) with usage example
6. Add logging for the new feature
7. Test thoroughly with sample orders
8. Create log files demonstrating the new feature

## Areas for Improvement

We welcome contributions in these areas:

- [ ] Stop-Loss and Take-Profit orders
- [ ] OCO (One-Cancels-Other) orders
- [ ] TWAP (Time-Weighted Average Price) execution
- [ ] Grid Trading strategies
- [ ] Position management commands
- [ ] WebSocket support for real-time updates
- [ ] Database for order history
- [ ] Advanced CLI with interactive menus
- [ ] Dashboard/UI using Streamlit
- [ ] Unit tests and test coverage
- [ ] Performance optimizations

## Questions?

- Check [README.md](README.md) for detailed documentation
- Review [QUICKSTART.md](QUICKSTART.md) for examples
- Look at [demo.py](demo.py) for code examples
- Check log files for API interaction details

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thanks for helping improve the Trading Bot! 🚀
