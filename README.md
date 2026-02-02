# **Unofficial**

# Platega API Library

A comprehensive Python library for interacting with the Platega.io API.

## Features

- Full support for all Platega API endpoints (Payments, Rates, etc.)
- Synchronous and Asynchronous clients
- Pydantic models for request/response validation
- Webhook handler with decorator support
- Type hinting

## Installation

```bash
pip install platega
```

## Usage

### Synchronous Client

```python
from platega import PlategaClient

client = PlategaClient(merchant_id="your-uuid", secret_key="your-secret")

status = client.check_invoice("transaction-uuid")
print(status)
```

### Asynchronous Client

```python
import asyncio
from platega import AsyncPlategaClient

async def main():
    client = AsyncPlategaClient(merchant_id="your-uuid", secret_key="your-secret")
    async with client:
        status = await client.check_invoice("transaction-uuid")
        print(status)

asyncio.run(main())
```

### Webhooks

```python
from platega import PlategaWebhookHandler, PaymentStatus

handler = PlategaWebhookHandler()

@handler.on(PaymentStatus.CONFIRMED)
async def handle_confirmed(payload):
    print(f"Payment confirmed: {payload.id}")

# In your web framework (e.g., FastAPI/Flask)
# handler.process_webhook(request_json)
```
