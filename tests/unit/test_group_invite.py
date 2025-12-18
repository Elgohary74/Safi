import random
import uuid as uuid_lib
from datetime import datetime, timedelta

import pytest

from app.models import GroupCreationRequest
from app.models.user import UserRegister
from app.services import AuthService, GroupService
from app.utils.exceptions import CreationError, ResourceAlreadyExists, ResourceNotFound


def generate_random_email():
    return f"user_{uuid_lib.uuid4()}@example.com"


def register_random_reader(auth_service, name_prefix="user"):
    return auth_service.register_user(
        UserRegister(
            name=f"{name_prefix}_{random.randint(1000, 9999)}",
            email=generate_random_email(),
            password="1234#Abcd",
        )
    )


def test_generate_invite_code(app):
    group_service = GroupService()
    code1 = group_service.generate_invite_code("admin1", "group1")
    code2 = group_service.generate_invite_code("admin1", "group2")

    assert len(code1) == 8
    assert len(code2) == 8
    assert code1 != code2


def test_create_group_generates_code(app):
    with app.app_context():
        # Setup
        auth_service = AuthService()
        user = register_random_reader(auth_service, "testuser_gen")

        group_service = GroupService()
        req = GroupCreationRequest(group_name="Test Group")
        group = group_service.create_new_group(req, user.user_id)

        assert group.invite_code is not None
        assert len(group.invite_code) == 8
        assert group.invite_code_expiry > datetime.now()


def test_join_group_success(app):
    with app.app_context():
        # Setup
        auth_service = AuthService()
        admin = register_random_reader(auth_service, "admin_join")
        member = register_random_reader(auth_service, "member_join")

        group_service = GroupService()
        req = GroupCreationRequest(group_name="Join Group")
        group = group_service.create_new_group(req, admin.user_id)
        group_service.save_new_group(group)

        # Join
        updated_group = group_service.join_group_by_code(
            member.user_id, group.invite_code
        )

        assert len(updated_group.members) == 2
        assert updated_group.members[1].user_id == member.user_id


def test_join_group_invalid_code(app):
    with app.app_context():
        group_service = GroupService()

        with pytest.raises(ResourceNotFound):
            group_service.join_group_by_code("someuser", "invalidcode")


def test_join_group_expired(app):
    with app.app_context():
        # Setup
        auth_service = AuthService()
        admin = register_random_reader(auth_service, "admin_exp")
        member = register_random_reader(auth_service, "member_exp")

        group_service = GroupService()
        req = GroupCreationRequest(group_name="Expired Group")
        group = group_service.create_new_group(req, admin.user_id)

        group.invite_code_expiry = datetime.now() - timedelta(days=1)
        group_service.save_new_group(group)

        with pytest.raises(CreationError) as exc:
            group_service.join_group_by_code(member.user_id, group.invite_code)
        assert "expired" in str(exc.value)


def test_join_group_already_member(app):
    with app.app_context():
        auth_service = AuthService()
        admin = register_random_reader(auth_service, "admin_dup")

        group_service = GroupService()
        req = GroupCreationRequest(group_name="Already Member Group")
        group = group_service.create_new_group(req, admin.user_id)
        group_service.save_new_group(group)
        with pytest.raises(ResourceAlreadyExists):
            group_service.join_group_by_code(admin.user_id, group.invite_code)


def test_invite_member_flow(app):
    with app.app_context():
        # Setup
        auth_service = AuthService()
        admin = register_random_reader(auth_service, "admin_inv")
        user = register_random_reader(auth_service, "user_inv")

        group_service = GroupService()
        req = GroupCreationRequest(group_name="Invite Group")
        group = group_service.create_new_group(req, admin.user_id)
        group_service.save_new_group(group)

        # 1. Admin invites user
        group_service.invite_member(admin.user_id, group.group_id, user.email)

        # Verify pending
        group = group_service.get_group(group.group_id)
        assert user.user_id in group.pending_members

        # Verify notification
        notifs = group_service.notification_repo.get_unread_by_user(user.user_id)
        assert len(notifs) >= 1
        assert notifs[0].type == "invite"

        # 2. User accepts
        group_service.respond_to_invite(user.user_id, group.group_id, "accept")

        # Verify member
        group = group_service.get_group(group.group_id)
        assert user.user_id in [m.user_id for m in group.members]
        assert user.user_id not in group.pending_members


def test_leave_group_flow(app):
    with app.app_context():
        # Setup
        auth_service = AuthService()
        admin = register_random_reader(auth_service, "admin_leave")
        user = register_random_reader(auth_service, "user_leave")

        group_service = GroupService()
        req = GroupCreationRequest(group_name="Leave Group")
        group = group_service.create_new_group(req, admin.user_id)
        group_service.save_new_group(group)

        # Add user directly (simulating join)
        group_service.join_group_by_code(user.user_id, group.invite_code)

        # User leaves
        group_service.leave_group(user.user_id, group.group_id)

        # Verify past member
        group = group_service.get_group(group.group_id)
        assert user.user_id not in [m.user_id for m in group.members]
        assert user.user_id in group.past_members


def test_admin_cannot_leave(app):
    with app.app_context():
        auth_service = AuthService()
        admin = register_random_reader(auth_service, "admin_static")

        group_service = GroupService()
        req = GroupCreationRequest(group_name="Admin Group")
        group = group_service.create_new_group(req, admin.user_id)
        group_service.save_new_group(group)

        with pytest.raises(CreationError):
            group_service.leave_group(admin.user_id, group.group_id)


def test_history_access_after_leaving(app):
    with app.app_context():
        # Setup
        auth_service = AuthService()
        admin = register_random_reader(auth_service, "admin_hist")
        user = register_random_reader(auth_service, "user_hist")

        group_service = GroupService()
        req = GroupCreationRequest(group_name="History Group")
        group = group_service.create_new_group(req, admin.user_id)
        group_service.save_new_group(group)

        # User joins then leaves
        group_service.join_group_by_code(user.user_id, group.invite_code)
        group_service.leave_group(user.user_id, group.group_id)

        # Verify user can still "see" the group (it returns in their list)
        user_groups = group_service.get_user_groups(user.user_id)

        assert len(user_groups) >= 1
        # Find the specific group
        found_group = next(
            (g for g in user_groups if g.group_id == group.group_id), None
        )
        assert found_group is not None
        assert user.user_id in found_group.past_members


def test_create_group_sets_2_hour_expiry(app):
    with app.app_context():
        auth_service = AuthService()
        user = register_random_reader(auth_service, "creator")
        group_service = GroupService()
        req = GroupCreationRequest(group_name="Short Expiry Group")

        group = group_service.create_new_group(req, user.user_id)

        # Check expiry is roughly 2 hours from now
        now = datetime.now()
        expected_expiry = now + timedelta(hours=2)

        # Allow small delta for execution time
        assert abs((group.invite_code_expiry - expected_expiry).total_seconds()) < 10


def test_refresh_invite_code_success(app):
    with app.app_context():
        auth_service = AuthService()
        admin = register_random_reader(auth_service, "admin_regen")
        group_service = GroupService()
        req = GroupCreationRequest(group_name="Regen Group")
        group = group_service.create_new_group(req, admin.user_id)
        group_id = group_service.save_new_group(group)

        old_code = group.invite_code
        # old_expiry = group.invite_code_expiry

        # Manually set expiry to something old to verify update
        group.invite_code_expiry = datetime.now() - timedelta(days=1)
        schema = group_service._convert_group_to_schema(group)
        group_service.group_repo.update(group_id, schema)

        # Refresh
        new_code = group_service.refresh_invite_code(admin.user_id, group_id)

        assert new_code != old_code

        updated_group = group_service.get_group(group_id)
        assert updated_group.invite_code == new_code

        # Check expiry is updated to 2 hours from now
        now = datetime.now()
        expected_expiry = now + timedelta(hours=2)
        assert (
            abs((updated_group.invite_code_expiry - expected_expiry).total_seconds())
            < 10
        )


def test_refresh_invite_code_non_admin(app):
    with app.app_context():
        auth_service = AuthService()
        admin = register_random_reader(auth_service, "admin_strict")
        user = register_random_reader(auth_service, "user_hacker")

        group_service = GroupService()
        req = GroupCreationRequest(group_name="Secure Group")
        group = group_service.create_new_group(req, admin.user_id)
        group_id = group_service.save_new_group(group)

        with pytest.raises(CreationError):
            group_service.refresh_invite_code(user.user_id, group_id)
