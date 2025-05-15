# MDAS Python SDK

A Python SDK for the MDAS API. This SDK provides an easy-to-use interface for interacting with the MDAS API.

## Installation

```bash
pip install mdas-python-sdk
```

## Usage

### Authentication

First, create a client instance with your credentials:

```python
from mdas_python_sdk import MdasClient

# Create a client instance
client = MdasClient(
    base_url="https://mdas-api-dev.viewtrade.dev",
    username="your-username",
    password="your-password"
)
```

The client will automatically authenticate and obtain a token upon initialization.

### Get Level 1 Quote

```python
# Get level 1 quote for a single symbol
quote_response = client.quote.get_level1_quote("TSLA")
print(quote_response)

# Get level 1 quote for multiple symbols
quotes = client.quote.get_level1_quote(["TSLA", "AAPL", "MSFT"])
print(quotes)
```

### Refresh Token

If your token expires, you can refresh it:

```python
client.refresh_token()
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License. 