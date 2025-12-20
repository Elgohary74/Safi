import logging
from typing import List, Optional

from app.models.group import Group, GroupSchema
from app.models.transaction import Transaction, TransactionSchema
from app.repositories.group_repo import GroupRepository
from app.repositories.transaction_repo import TransactionRepository
from app.repositories.user_repo import UserRepository
from app.services.base import BaseService
from app.utils.exceptions import ResourceNotFound


class TransactionService(BaseService):
    def __init__(self):
        super().__init__()
        self.transaction_repo = TransactionRepository()
        self.user_repo = UserRepository()
        self.group_repo = GroupRepository()
        self.logger = logging.getLogger(__name__)

    def create_settlement(
        self, payer_id: str, receiver_id: str, amount: float, group_id: str
    ) -> str:
        # Validate users and group
        payer = self.user_repo.get_by_id(payer_id)
        receiver = self.user_repo.get_by_id(receiver_id)
        group = self.group_repo.get_by_id(group_id)

        if not payer or not receiver or not group:
            raise ResourceNotFound("User or Group not found")

        transaction = TransactionSchema(
            amount=amount,
            payer_id=payer_id,
            receiver_id=receiver_id,
            group_id=group_id,
            status="completed",  # Settlements are usually instant/confirmed
        )

        return self.transaction_repo.add(transaction)

    def get_user_transactions(self, user_id: str) -> List[Transaction]:
        schemas = self.transaction_repo.get_by_user(user_id)
        transactions = []
        for schema in schemas:
            try:
                # Populate related objects
                payer = self.user_repo.get_by_id(schema.payer_id)
                receiver = self.user_repo.get_by_id(schema.receiver_id)
                group_schema = self.group_repo.get_by_id(schema.group_id)

                if payer and receiver and group_schema:
                    # Convert GroupSchema to Group model
                    group = self._convert_schema_to_group(group_schema)

                    trans = Transaction(
                        **schema.model_dump(
                            exclude={"payer_id", "receiver_id", "group_id"}
                        ),
                        payer=payer,
                        receiver=receiver,
                        group=group,
                    )
                    transactions.append(trans)
            except Exception as e:
                self.logger.error(
                    f"Error populating transaction {schema.transaction_id}: {e}"
                )
                continue

        return transactions

    def get_transaction(self, trans_id: str) -> Optional[Transaction]:
        schema = self.transaction_repo.get_by_id(trans_id)
        if not schema:
            return None

        payer = self.user_repo.get_by_id(schema.payer_id)
        receiver = self.user_repo.get_by_id(schema.receiver_id)
        group_schema = self.group_repo.get_by_id(schema.group_id)

        if payer and receiver and group_schema:
            group = self._convert_schema_to_group(group_schema)
            return Transaction(
                **schema.model_dump(exclude={"payer_id", "receiver_id", "group_id"}),
                payer=payer,
                receiver=receiver,
                group=group,
            )

        return None

    def _convert_schema_to_group(self, schema: GroupSchema) -> Group:
        # This is a helper to convert GroupSchema (data model) to Group (domain model)
        # We need to fetch the first member (user) to populate the Group domain model
        if not schema:
            return None

        first_member = self.user_repo.get_by_id(schema.first_member_id)
        if not first_member:
            # Fallback or error handling if first member is missing, likely shouldn't happen in valid state
            return None

        # Basic conversion, populating required fields
        return Group(
            **schema.model_dump(exclude={"first_member_id", "members_ids"}),
            first_member=first_member,
            members=[],  # Members are not fully populated here for performance logic in list views usually
        )
