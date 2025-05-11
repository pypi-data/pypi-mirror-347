# PayPal SDK

Minimal PayPal Checkout SDK (with Pydantic models)

[![PyPI version](https://img.shields.io/pypi/v/paypal-checkout-sdk.svg)](https://pypi.org/project/paypal-checkout-sdk.svg/)
[![Python versions](https://img.shields.io/pypi/pyversions/paypal-checkout-sdk.svg)]

A minimalistic Python SDK for PayPal Checkout using Pydantic models and HTTPX.

## Features

- OAuth2 authentication with token caching and auto-refresh
- Pydantic v2 models for request and response payloads
- Synchronous HTTP client powered by HTTPX
- Support for PayPal Orders API (create, capture, retrieve)
- Custom exception types for error handling

## Installation

```bash
pip install paypal-checkout-sdk
```

Requires Python 3.11+, Pydantic 2.x, HTTPX 0.27+

## Quick Start

### Initialize client

```python
from paypal_sdk import PayPalClient
from paypal_sdk.enums import Environment

client = PayPalClient(
    client_id="YOUR_CLIENT_ID",
    client_secret="YOUR_CLIENT_SECRET",
    environment=Environment.SANDBOX,  # Use Environment.LIVE for production
)
```

You can also use the client as a context manager:

```python
with PayPalClient(... ) as client:
    # use client
```

### Create an Order

```python
from paypal_sdk.models.orders import CreateOrderRequest, PurchaseUnitRequest
from paypal_sdk.models.base import Money

order_request = CreateOrderRequest(
    intent="CAPTURE",
    purchase_units=[
        PurchaseUnitRequest(
            amount=Money(currency_code="USD", value="100.00"),
            reference_id="PU1",
        )
    ],
)

order = client.orders.create_order(order_request)
print("Order ID:", order.id)
print("Status:", order.status)

# Extract approval URL
for link in order.links:
    if link.rel == "approve":
        print("Approval URL:", link.href)
        break
```

After the buyer approves the payment, capture the order:

```python
capture = client.orders.capture_order(order.id)
print("Capture status:", capture.purchase_units[0].payments.captures[0].status)
```

### Retrieve an Order

```python
order = client.orders.get_order(order_id)
print(order)
```

## Error Handling

All SDK errors inherit from `paypal_sdk.exceptions.PayPalError`:

- `AuthenticationError`: failed to authenticate or refresh token
- `APIError`: PayPal API returned an error (status code 4xx or 5xx)
- `RequestError`: network or HTTP request issues
- `ConfigurationError`: SDK configuration errors

```python
from paypal_sdk.exceptions import APIError, AuthenticationError, RequestError

try:
    client.orders.get_order("INVALID_ID")
except AuthenticationError as e:
    print("Auth failed:", e)
except APIError as e:
    print("API error:", e)
except RequestError as e:
    print("Request error:", e)
```

## API Reference

### PayPalClient

`PayPalClient(client_id: str, client_secret: str, environment: Environment = Environment.SANDBOX, timeout: float = 30.0, max_retries: int = 3)`

Main client for interacting with the PayPal REST API:

- `orders`: `OrdersService` instance for Orders API methods
- `close()`: close underlying HTTP connection
- Context manager support (`__enter__` / `__exit__`)

### OrdersService

Located at `paypal_sdk.services.orders.OrdersService`:

- `create_order(order_request: CreateOrderRequest, paypal_request_id: Optional[str] = None, prefer: str = "return=representation") -> CreateOrderResponse`
- `capture_order(order_id: str, capture_request: Optional[CaptureOrderRequest] = None, paypal_request_id: Optional[str] = None, prefer: str = "return=representation") -> CaptureOrderResponse`
- `get_order(order_id: str) -> Order`

### Models

Pydantic v2 models are defined under `paypal_sdk.models`:

- `CreateOrderRequest`, `CaptureOrderRequest`, `PurchaseUnitRequest`, `Money`, `Order`, etc.

### Exceptions

Custom exceptions in `paypal_sdk.exceptions`:

- `PayPalError`
- `AuthenticationError`
- `APIError`
- `RequestError`
- `ConfigurationError`

## References

- [PayPal API Documentation](https://developer.paypal.com/docs/api/overview/)

