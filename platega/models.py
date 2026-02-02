from enum import IntEnum, Enum
from typing import Optional, Any
from pydantic import BaseModel, Field, HttpUrl, ConfigDict
from uuid import UUID
from datetime import datetime

class PaymentMethod(IntEnum):
    SBP_QR = 2
    CARDS_RUB = 10
    CARD_ACQUIRING = 11
    INTERNATIONAL_ACQUIRING = 12
    CRYPTO = 13

class PaymentStatus(str, Enum):
    PENDING = "PENDING"
    CANCELED = "CANCELED"
    CONFIRMED = "CONFIRMED"
    CHARGEBACKED = "CHARGEBACKED"

class PaymentDetails(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    amount: float
    currency: str = "RUB"

class CreateTransactionRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    paymentMethod: PaymentMethod
    paymentDetails: PaymentDetails
    description: str
    return_url: HttpUrl = Field(alias="return")
    failedUrl: HttpUrl
    payload: Optional[str] = None

class CreateTransactionResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    paymentMethod: str
    transactionId: UUID
    redirect: HttpUrl
    return_url: Optional[HttpUrl] = Field(None, alias="return")
    paymentDetails: Any
    status: PaymentStatus
    expiresIn: str
    merchantId: UUID
    usdtRate: Optional[float] = None

class TransactionStatusResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id: UUID
    status: PaymentStatus
    paymentDetails: PaymentDetails
    merchantName: Optional[str] = None
    merchantId: Optional[UUID] = Field(None, alias="mechantId")
    comission: Optional[float] = None
    paymentMethod: Optional[str] = None
    expiresIn: Optional[str] = None
    return_url: Optional[HttpUrl] = Field(None, alias="return")
    comissionUsdt: Optional[float] = None
    amountUsdt: Optional[float] = None
    qr: Optional[str] = None
    payformSuccessUrl: Optional[HttpUrl] = None
    payload: Optional[str] = None
    comissionType: Optional[int] = None
    externalId: Optional[str] = None
    description: Optional[str] = None

class CallbackPayload(BaseModel):
    id: UUID
    amount: float
    currency: str
    status: PaymentStatus
    paymentMethod: int

class RateResponse(BaseModel):
    paymentMethod: int
    currencyFrom: str
    currencyTo: str
    rate: float
    updatedAt: datetime
