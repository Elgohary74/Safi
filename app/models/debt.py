from pydantic import BaseModel


class Debt(BaseModel):
    from_user: str
    to_user: str
    amount: float
    currency: str = "EGP"
