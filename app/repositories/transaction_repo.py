from typing import List, Optional

from app.models.transaction import Transaction
from app.repositories.base import IRepository


class TransactionRepository(IRepository):
    def __init__(self):
        super().__init__()
        self.collection = self.db["settlements"]

    def add(self, transaction: Transaction) -> str:
        self.logger.info(
            f"initiating settlement: {transaction.amount} from {transaction.payer_id}"
        )
        self.collection.insert_one(transaction.to_dict())
        return transaction.transaction_id

    def get_by_id(self, trans_id: str) -> Optional[dict]:
        return self.collection.find_one({"_id": trans_id})

    def get_by_group(self, group_id: str) -> List[dict]:
        return list(self.collection.find({"group_id": group_id}))

    def update(self, trans_id: str, data: dict):
        self.logger.info(f"updating transaction {trans_id} status")
        self.collection.update_one({"_id": trans_id}, {"$set": data})

    def delete(self, trans_id: str):
        self.collection.delete_one({"_id": trans_id})
