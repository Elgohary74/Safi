from typing import Literal, Union

from pydantic import BaseModel, Field


class IPNPayment(BaseModel):
    type: Literal["instapay"] = "instapay"
    ipn_address: str = Field(...)


class WalletPayment(BaseModel):
    type: Literal["e-wallet"] = "e-wallet"
    phone_number: str = Field(...)


class TeldaPayment(BaseModel):
    type: Literal["telda"] = "telda"
    handler: str = Field(...)


PaymentMethod = Union[IPNPayment, WalletPayment, TeldaPayment]
