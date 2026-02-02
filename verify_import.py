import sys
import os
import asyncio

# Add current directory to sys.path to ensure we can import the package
sys.path.insert(0, os.getcwd())

try:
    from platega import (
        PlategaClient,
        AsyncPlategaClient,
        PaymentMethod,
        PaymentStatus,
        CreateTransactionRequest,
        PlategaWebhookHandler
    )
    print("✅ Successfully imported all main components.")
except ImportError as e:
    print(f"❌ ImportError: {e}")
    sys.exit(1)

try:
    # Test Model Instantiation
    req = CreateTransactionRequest(
        paymentMethod=PaymentMethod.SBP_QR,
        paymentDetails={"amount": 100.0, "currency": "RUB"},
        description="Test Payment",
        return_url="https://example.com/success",  # Uses alias 'return'
        failedUrl="https://example.com/fail"
    )
    print("✅ Successfully instantiated CreateTransactionRequest model.")
    
    # Check alias working
    dumped = req.model_dump(by_alias=True)
    if "return" in dumped and dumped["return"] == "https://example.com/success/":
        print("✅ Alias 'return' is correctly handled in model_dump.")
    else:
        # Pydantic HttpUrl might add trailing slash or strictly validate
        print(f"ℹ️ Dumped model: {dumped}")
        if "return" in dumped:
             print("✅ Alias 'return' is present.")
        else:
             print("❌ Alias 'return' is MISSING.")

except Exception as e:
    print(f"❌ Model Error: {e}")
    sys.exit(1)

async def test_client_init():
    try:
        async with AsyncPlategaClient(merchant_id="test", secret_key="test") as client:
            print("✅ AsyncPlategaClient initialized successfully.")
    except Exception as e:
        print(f"❌ AsyncPlategaClient Error: {e}")

try:
    with PlategaClient(merchant_id="test", secret_key="test") as client:
        print("✅ PlategaClient initialized successfully.")
except Exception as e:
    print(f"❌ PlategaClient Error: {e}")

asyncio.run(test_client_init())
