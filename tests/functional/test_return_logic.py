from app.models.group import GroupCreationRequest
from app.models.user import UserRegister
from app.services import AuthService, GroupService


def test_return_logic_dashboard(client):
    # Setup: Register and Login
    email = "test_return@example.com"
    AuthService().register_user(
        UserRegister(name="Test User", email=email, password="Password123!")
    )
    client.post(
        "/auth/login",
        data={"email": email, "password": "Password123!"},
    )

    # Create Group
    user_id = AuthService().authenticate_user(email, "Password123!").user_id
    group = GroupService().create_new_group(
        GroupCreationRequest(group_name="Test Group", description="Desc"),
        first_member_id=user_id,
    )
    GroupService().save_new_group(group)
    group_id = group.group_id

    # Test 1: Referrer IS Dashboard
    # We simulate coming from dashboard
    resp = client.get(
        f"/groups/{group_id}/details",
        environ_base={"HTTP_REFERER": "http://localhost/dashboard/"},
    )
    assert resp.status_code == 200
    # Check if back link points to dashboard
    # The template renders: <a href="/dashboard/" ...
    # url_for('dashboard.dashboard_index') -> /dashboard/ (assuming)
    assert 'href="/dashboard/"' in resp.get_data(as_text=True)

    # Test 2: Referrer IS Groups List
    resp = client.get(
        f"/groups/{group_id}/details",
        environ_base={"HTTP_REFERER": "http://localhost/groups/list"},
    )
    assert resp.status_code == 200
    # Check if back link points to groups list
    assert 'href="/groups/list"' in resp.get_data(as_text=True)

    # Test 3: Unknown Referrer -> Default to groups list
    resp = client.get(
        f"/groups/{group_id}/details",
        environ_base={"HTTP_REFERER": "http://google.com"},
    )
    assert 'href="/groups/list"' in resp.get_data(as_text=True)
