import httpx
from typing import Optional, List, Union, Dict, Any
from uuid import UUID
from .models import (
    CreateTransactionRequest,
    CreateTransactionResponse,
    TransactionStatusResponse,
    RateResponse,
    PaymentMethod
)
from .exceptions import PlategaAPIError

class BasePlategaClient:
    def __init__(self, merchant_id: str, secret_key: str, base_url: str = "https://app.platega.io"):
        self.merchant_id = merchant_id
        self.secret_key = secret_key
        self.base_url = base_url.rstrip("/")
        self._headers = {
            "X-MerchantId": self.merchant_id,
            "X-Secret": self.secret_key,
            "Content-Type": "application/json"
        }

    def _handle_response(self, response: httpx.Response) -> Dict[str, Any]:
        if response.status_code >= 400:
            raise PlategaAPIError(response.status_code, response.text)
        return response.json()

class AsyncPlategaClient(BasePlategaClient):
    def __init__(self, merchant_id: str, secret_key: str, base_url: str = "https://app.platega.io/"):
        super().__init__(merchant_id, secret_key, base_url)
        self._client = httpx.AsyncClient(base_url=self.base_url, headers=self._headers)

    async def close(self):
        await self._client.aclose()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

    async def create_invoice(self, request: CreateTransactionRequest) -> CreateTransactionResponse:
        payload = request.model_dump(by_alias=True, mode='json')
        response = await self._client.post("/transaction/process", json=payload)
        data = self._handle_response(response)
        return CreateTransactionResponse(**data)

    async def check_invoice(self, transaction_id: Union[str, UUID]) -> TransactionStatusResponse:
        response = await self._client.get(f"/transaction/{str(transaction_id)}")
        data = self._handle_response(response)
        return TransactionStatusResponse(**data)

    async def get_rates(self, payment_method: PaymentMethod, currency_from: str, currency_to: str) -> RateResponse:
        params = {
            "merchantId": self.merchant_id,
            "paymentMethod": int(payment_method),
            "currencyFrom": currency_from,
            "currencyTo": currency_to
        }
        response = await self._client.get("/rates/payment_method_rate", params=params)
        data = self._handle_response(response)
        return RateResponse(**data)
    
    async def get_conversions(self, date_from: str, date_to: str, page: int = 1, size: int = 20) -> Any:
        params = {
            "from": date_from,
            "to": date_to,
            "page": page,
            "size": size
        }
        response = await self._client.get("/transaction/balance-unlock-operations", params=params)
        return self._handle_response(response)

class PlategaClient(BasePlategaClient):
    def __init__(self, merchant_id: str, secret_key: str, base_url: str = "https://app.platega.io/"):
        super().__init__(merchant_id, secret_key, base_url)
        self._client = httpx.Client(base_url=self.base_url, headers=self._headers)

    def close(self):
        self._client.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def create_invoice(self, request: CreateTransactionRequest) -> CreateTransactionResponse:
        payload = request.model_dump(by_alias=True, mode='json')
        response = self._client.post("/transaction/process", json=payload)
        data = self._handle_response(response)
        return CreateTransactionResponse(**data)

    def check_invoice(self, transaction_id: Union[str, UUID]) -> TransactionStatusResponse:
        response = self._client.get(f"/transaction/{str(transaction_id)}")
        data = self._handle_response(response)
        return TransactionStatusResponse(**data)

    def get_rates(self, payment_method: PaymentMethod, currency_from: str, currency_to: str) -> RateResponse:
        params = {
            "merchantId": self.merchant_id,
            "paymentMethod": int(payment_method),
            "currencyFrom": currency_from,
            "currencyTo": currency_to
        }
        response = self._client.get("/rates/payment_method_rate", params=params)
        data = self._handle_response(response)
        return RateResponse(**data)

    def get_conversions(self, date_from: str, date_to: str, page: int = 1, size: int = 20) -> Any:
        params = {
            "from": date_from,
            "to": date_to,
            "page": page,
            "size": size
        }
        response = self._client.get("/transaction/balance-unlock-operations", params=params)
        return self._handle_response(response)
