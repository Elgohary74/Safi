from datetime import datetime
from unittest.mock import MagicMock

from app.models.group import GroupSchema
from app.models.transaction import TransactionSchema
from app.models.user import User
from app.services.transaction_service import TransactionService


def test_create_settlement_success():
    service = TransactionService()
    service.user_repo = MagicMock()
    service.group_repo = MagicMock()
    service.transaction_repo = MagicMock()

    service.user_repo.get_by_id.side_effect = lambda id: User(
        user_id=id, name="User", email="u@e.com", password_hash="h"
    )

    service.group_repo.get_by_id.return_value = GroupSchema(
        group_id="g1",
        group_name="Group",
        description="desc",
        first_member_id="u1",
        members_ids=["u1", "u2"],
        created_by="u1",
        created_at=datetime.utcnow(),
    )
    service.transaction_repo.add.return_value = "trans_1"

    tid = service.create_settlement("u1", "u2", 100.0, "g1")

    # Assert
    assert tid == "trans_1"
    service.transaction_repo.add.assert_called_once()
    args = service.transaction_repo.add.call_args[0][0]
    assert isinstance(args, TransactionSchema)
    assert args.amount == 100.0
    assert args.payer_id == "u1"
    assert args.receiver_id == "u2"
    assert args.group_id == "g1"
    assert args.status == "completed"


def test_get_user_transactions():
    service = TransactionService()
    service.transaction_repo = MagicMock()
    service.user_repo = MagicMock()
    service.group_repo = MagicMock()

    mock_trans = TransactionSchema(
        transaction_id="t1",
        amount=50,
        payer_id="u1",
        receiver_id="u2",
        group_id="g1",
        status="completed",
    )
    service.transaction_repo.get_by_user.return_value = [mock_trans]

    service.user_repo.get_by_id.side_effect = lambda id: User(
        user_id=id, name=f"User{id}", email=f"{id}@e.com", password_hash="h"
    )

    def create_mock_group_schema(group_id):
        return GroupSchema(
            group_id=group_id,
            group_name="Group",
            description="desc",
            first_member_id="u1",
            members_ids=["u1"],
        )

    service.group_repo.get_by_id.side_effect = lambda gid: create_mock_group_schema(gid)

    results = service.get_user_transactions("u1")

    assert len(results) == 1
    assert results[0].transaction_id == "t1"
    assert results[0].payer.user_id == "u1"
    assert results[0].receiver.user_id == "u2"
    assert results[0].group.group_id == "g1"
