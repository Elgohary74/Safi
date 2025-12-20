from app.models.payment_method import (
    IPNPayment,
    PaymentMethod,
    TeldaPayment,
    WalletPayment,
)
from app.utils.exceptions import UnkownTypeError


class PaymentFactory:
    @staticmethod
    def create_payment_method(data: dict) -> PaymentMethod:
        if data.get("type") == "instapay":
            return IPNPayment.model_validate(data)

        elif data.get("type") == "e-wallet":
            return WalletPayment.model_validate(data)

        elif data.get("type") == "telda":
            return TeldaPayment.model_validate(data)

        else:
            raise UnkownTypeError()
