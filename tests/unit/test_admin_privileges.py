import pytest

from app.models import GroupCreationRequest
from app.services import AuthService, GroupService
from app.utils.exceptions import CreationError


def register_random_admin(auth_service, name_prefix="admin_priv"):
    import random
    import uuid

    return auth_service.register_user(
        type(
            "obj",
            (object,),
            {
                "name": f"{name_prefix}_{random.randint(1000, 9999)}",
                "email": f"user_{uuid.uuid4()}@example.com",
                "password": "password",
                "phone_number": "0000",
            },
        )
    )


def test_assign_new_first_member(app):
    with app.app_context():
        auth_service = AuthService()
        admin = register_random_admin(auth_service)
        member = register_random_admin(auth_service, "member")

        group_service = GroupService()
        req = GroupCreationRequest(group_name="Privilege Group")
        group = group_service.create_new_group(req, admin.user_id)
        group_service.save_new_group(group)

        # Add member first
        group_service.join_group_by_code(member.user_id, group.invite_code)

        # Assign new admin
        group_service.assign_new_first_member(
            admin.user_id, group.group_id, member.user_id
        )

        updated_group = group_service.get_group(group.group_id)
        assert updated_group.first_member.user_id == member.user_id


def test_remove_member(app):
    with app.app_context():
        auth_service = AuthService()
        admin = register_random_admin(auth_service)
        member = register_random_admin(auth_service, "member_rem")

        group_service = GroupService()
        req = GroupCreationRequest(group_name="Kick Group")
        group = group_service.create_new_group(req, admin.user_id)
        group_service.save_new_group(group)

        group_service.join_group_by_code(member.user_id, group.invite_code)

        # Remove member
        group_service.remove_member(group.group_id, member.user_id)

        updated_group = group_service.get_group(group.group_id)
        assert member.user_id not in [m.user_id for m in updated_group.members]
        assert member.user_id in updated_group.past_members


def test_update_group_info(app):
    with app.app_context():
        auth_service = AuthService()
        admin = register_random_admin(auth_service)

        group_service = GroupService()
        req = GroupCreationRequest(group_name="Old Name")
        group = group_service.create_new_group(req, admin.user_id)
        group_service.save_new_group(group)

        group_service.update_group_info(group.group_id, "New Name", "New Desc")

        updated_group = group_service.get_group(group.group_id)
        assert updated_group.group_name == "New Name"
        assert updated_group.description == "New Desc"


def test_leave_group_with_successor(app):
    with app.app_context():
        auth_service = AuthService()
        admin = register_random_admin(auth_service)
        successor = register_random_admin(auth_service, "successor")

        group_service = GroupService()
        req = GroupCreationRequest(group_name="Succession Group")
        group = group_service.create_new_group(req, admin.user_id)
        group_service.save_new_group(group)

        group_service.join_group_by_code(successor.user_id, group.invite_code)

        # Admin leaves with successor
        group_service.leave_group(
            admin.user_id, group.group_id, successor_id=successor.user_id
        )

        updated_group = group_service.get_group(group.group_id)
        assert updated_group.first_member.user_id == successor.user_id
        assert admin.user_id not in [m.user_id for m in updated_group.members]


def test_leave_group_without_successor_fails(app):
    with app.app_context():
        auth_service = AuthService()
        admin = register_random_admin(auth_service)
        member = register_random_admin(auth_service, "member")

        group_service = GroupService()
        req = GroupCreationRequest(group_name="Fail Group")
        group = group_service.create_new_group(req, admin.user_id)
        group_service.save_new_group(group)

        group_service.join_group_by_code(member.user_id, group.invite_code)

        # Admin tries to leave without successor
        with pytest.raises(CreationError) as exc:
            group_service.leave_group(admin.user_id, group.group_id)
        assert "must assign a new admin" in str(exc.value)


def test_decorator_blocks_non_admin(app):
    with app.test_request_context():
        auth_service = AuthService()
        admin = register_random_admin(auth_service)
        non_admin = register_random_admin(auth_service, "non_admin")

        group_service = GroupService()
        req = GroupCreationRequest(group_name="Protected Group")
        group = group_service.create_new_group(req, admin.user_id)
        group_service.save_new_group(group)
        assert (
            group_service._is_user_first_member_of_group(admin.user_id, group.group_id)
            is True
        )
        assert (
            group_service._is_user_first_member_of_group(
                non_admin.user_id, group.group_id
            )
            is False
        )
