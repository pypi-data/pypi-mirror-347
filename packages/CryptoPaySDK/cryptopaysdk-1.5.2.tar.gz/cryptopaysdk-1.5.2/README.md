![](https://raw.githubusercontent.com/sllavon/crypto-pay-api-sdk/3e83818c975a47f4ca61209b478f2508224058db/media/header.svg)

# CryptoPaySDK - Python SDK for Crypto Pay API

[![PyPI version](https://img.shields.io/pypi/v/CryptoPaySDK)](https://pypi.org/project/CryptoPaySDK/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Official Python SDK for seamless integration with [Crypto Pay](https://t.me/CryptoBot) - cryptocurrency payments platform in Telegram.

## Key Features

- Full coverage of [Crypto Pay API](https://help.crypt.bot/crypto-pay-api) methods
- Simple and intuitive interface
- Support for both mainnet and testnet environments
- Type hints for better development experience
- 100% API consistency with official documentation

## Installation

```bash
pip install CryptoPaySDK
```

## Getting Started

1. **Obtain API Token**:
   - Mainnet: [@CryptoBot](http://t.me/CryptoBot?start=pay)
   - Testnet: [@CryptoTestnetBot](http://t.me/CryptoTestnetBot?start=pay)

   Send `/pay` command to create your application.

2. **Environment Configuration**:

| Network  | Bot | API Hostname |
|----------|-----|--------------|
| Mainnet  | [@CryptoBot](http://t.me/CryptoBot?start=pay) | `pay.crypt.bot` |
| Testnet  | [@CryptoTestnetBot](http://t.me/CryptoTestnetBot?start=pay) | `testnet-pay.crypt.bot` |

> All API requests must use HTTPS protocol

## Basic Usage

```python
from CryptoPaySDK import cryptopay

# Initialize client (testnet mode by default)
crypto = cryptopay.Crypto(
    api_token="YOUR_API_TOKEN",
    testnet=True  # Set False for production
)

# Get app information
print(crypto.getMe())

# Create payment invoice
invoice = crypto.createInvoice(
    asset="TON",
    amount="0.4",
    params={
        "description": "Premium subscription",
        "expires_in": 3600,
        "paid_btn_url": "https://your-service.com/premium"
    }
)
```

## API Reference

### Core Methods

#### `getMe()`
Verify authentication token and get basic app info.

```python
response = crypto.getMe()
```

#### `createInvoice(asset: str, amount: str, params: dict)`
Create payment invoice.

**Parameters**:
- `asset` - Cryptocurrency code (BTC, TON, ETH, USDT, etc.)
- `amount` - Payment amount
- `params` - Additional options:
  - `description` - Invoice description (max 1024 chars)
  - `hidden_message` - Post-payment message
  - `paid_btn_name` - Button type (viewItem/openChannel/openBot/callback)
  - `paid_btn_url` - Button URL (required if paid_btn_name set)
  - `payload` - Custom data (up to 4KB)
  - `expires_in` - Invoice TTL (1-2678400 seconds)

```python
invoice = crypto.createInvoice(
    "BTC", "0.01",
    params={
        "description": "VIP Access",
        "paid_btn_name": "openBot",
        "paid_btn_url": "https://t.me/YourBot"
    }
)
```

#### `transfer(user_id: int, asset: str, amount: str, spend_id: str, params: dict)`
Send cryptocurrency to user.

**Parameters**:
- `user_id` - Recipient Telegram ID
- `asset` - Cryptocurrency code
- `amount` - Transfer amount
- `spend_id` - Unique operation ID (prevent duplicates)
- `params`:
  - `comment` - Transfer note (max 1024 chars)

```python
crypto.transfer(
    123456789, "TON", "5.0", "order_123",
    params={"comment": "Order #123 payment"}
)
```

### Additional Methods

| Method | Description |
|--------|-------------|
| `getInvoices()` | Retrieve payment invoices |
| `getBalance()` | Check current balance |
| `getExchangeRates()` | Get current exchange rates |
| `getCurrencies()` | List supported currencies |

## Error Handling

The SDK raises specific exceptions for different error scenarios:

- `AuthError` - Invalid API token
- `NetworkError` - Connection issues
- `APIError` - Crypto Pay API errors
- `ValidationError` - Invalid parameters

```python
try:
    crypto.createInvoice("BTC", "0.01")
except CryptoPaySDK.exceptions.APIError as e:
    print(f"API Error: {e.message}")
```

## License

MIT