import pytest

from app.repositories.group_repo import GroupRepository
from app.services.group import GroupService


@pytest.fixture
def group_service():
    return GroupService()


@pytest.fixture
def group_repo():
    return GroupRepository()


def test_delete_group_functionality(client, auth_client, group_service, group_repo):
    """
    Test that deleting a group:
    1. Sets is_active to False
    2. Moves members to past_members
    3. Clears members list
    """
    auth_client.register("admin@example.com", "Admin User", "ValidPass1!")
    auth_client.login("admin@example.com", "ValidPass1!")
    admin_user = auth_client.get_current_user()

    auth_client.register("member@example.com", "Member User", "ValidPass1!")
    from app.repositories.user_repo import UserRepository

    user_repo = UserRepository()
    member_user = user_repo.get_by_email("member@example.com")

    auth_client.login("admin@example.com", "ValidPass1!")

    response = client.post(
        "/groups/create",
        data={"group_name": "Test Group", "description": "To be deleted"},
        follow_redirects=True,
    )
    assert response.status_code == 200

    groups = group_service.get_user_groups(admin_user.user_id)
    assert len(groups) == 1
    group = groups[0]
    group_id = group.group_id

    group_repo.add_member(group_id, member_user.user_id)

    group_check = group_repo.get_by_id(group_id)
    assert member_user.user_id in group_check.members_ids
    assert admin_user.user_id in group_check.members_ids
    assert group_check.is_active

    response = client.post(f"/groups/{group_id}/delete", follow_redirects=True)
    assert response.status_code == 200
    assert b"Group deleted successfully!" in response.data

    deleted_group = group_repo.get_by_id(group_id)

    assert not deleted_group.is_active
    assert len(deleted_group.members_ids) == 0
    assert admin_user.user_id in deleted_group.past_members_ids
    assert member_user.user_id in deleted_group.past_members_ids
