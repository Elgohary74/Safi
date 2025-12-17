from typing import List, Optional

from app.models.transaction import TransactionSchema
from app.repositories.base import IRepository


class TransactionRepository(IRepository):
    def __init__(self):
        super().__init__()
        self.collection = self.db["settlements"]

    def add(self, transaction: TransactionSchema) -> str:
        self.logger.info(
            f"initiating settlement: {transaction.amount} from {transaction.payer_id} to {transaction.receiver_id}"
        )
        self.collection.insert_one(transaction.model_dump())
        return transaction.transaction_id

    def get_by_id(self, trans_id: str) -> Optional[TransactionSchema]:
        self.logger.debug(f"fetching transaction id: {trans_id}")
        data = self.collection.find_one({"_id": trans_id})
        return TransactionSchema.model_validate(data) if data else None

    def get_by_group(self, group_id: str) -> List[TransactionSchema]:
        self.logger.debug(f"fetching all transactions for group {group_id}")
        data_list = list(self.collection.find({"group_id": group_id}))
        return [TransactionSchema.model_validate(data) for data in data_list]

    def update(self, trans_id: str, data: TransactionSchema):
        self.logger.info(f"updating transaction {trans_id} status")
        self.collection.update_one({"_id": trans_id}, {"$set": data.model_dump()})

    def delete(self, trans_id: str):
        self.logger.info(f"deleting transaction id: {trans_id}")
        self.collection.delete_one({"_id": trans_id})
