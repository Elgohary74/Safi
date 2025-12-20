import pytest

from app.repositories.user_repo import UserRepository
from app.services.transaction_service import TransactionService


@pytest.fixture
def auth_headers(client):
    client.post(
        "/auth/register",
        data={
            "name": "Test User",
            "email": "test@example.com",
            "password": "Password1!",
            "confirm_password": "Password1!",
        },
    )
    response = client.post(
        "/auth/login", data={"email": "test@example.com", "password": "Password1!"}
    )

    return response.headers


def test_activity_page_access(client):
    client.post(
        "/auth/register",
        data={
            "name": "ActivityUser",
            "email": "activity@example.com",
            "password": "Password1!",
            "confirm_password": "Password1!",
        },
    )
    client.post(
        "/auth/login", data={"email": "activity@example.com", "password": "Password1!"}
    )

    response = client.get("/transactions/activity", follow_redirects=True)
    assert response.status_code == 200
    assert b"Activity Log" in response.data


def test_create_settlement_flow(client):
    resp = client.post(
        "/auth/register",
        data={
            "name": "Payer",
            "email": "payer@example.com",
            "password": "Password1!",
            "confirm_password": "Password1!",
        },
    )
    assert resp.status_code == 302, f"Registration failed: {resp.data}"

    resp = client.post(
        "/auth/login", data={"email": "payer@example.com", "password": "Password1!"}
    )
    assert resp.status_code == 302, f"Login failed: {resp.data}"

    user_repo = UserRepository()
    from app.models.user import User

    receiver_data = User(
        name="Receiver", email="receiver@example.com", password_hash="hash_placeholder"
    )

    receiver_id = user_repo.add(receiver_data)

    client.post("/groups/create", data={"group_name": "Test Group"})

    from app.models.group import GroupCreationRequest
    from app.repositories.group_repo import GroupRepository

    group_repo = GroupRepository()

    payer = user_repo.get_by_email("payer@example.com")

    import uuid

    from app.services import GroupService

    group_service = GroupService()
    unique_group_name = f"Test Group {uuid.uuid4()}"
    group = group_service.create_new_group(
        GroupCreationRequest(group_name=unique_group_name),
        first_member_id=payer.user_id,
    )
    group_service.save_new_group(group)
    group_repo.add_member(group.group_id, receiver_id)
    response = client.post(
        "/transactions/create",
        data={"pay_to": receiver_id, "amount": "50.0", "group_id": group.group_id},
    )

    # Should redirect
    assert response.status_code == 302

    trans_service = TransactionService()
    transactions = trans_service.get_user_transactions(payer.user_id)
    assert len(transactions) == 1
    assert transactions[0].amount == 50.0
    assert transactions[0].receiver.user_id == receiver_id
