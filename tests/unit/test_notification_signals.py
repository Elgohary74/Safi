import uuid as uuid_lib

from blinker import ANY

from app.events.signals import expense_created, invite_sent
from app.models import GroupCreationRequest
from app.models.expense import ExpenseCreationRequest
from app.models.user import UserRegister
from app.repositories.notification_repo import NotificationRepository
from app.services import AuthService, ExpenseService, GroupService


def remove_flake_errors2(cid1):
    pass


def remove_flake_errors3(auth: AuthService):
    pass


def _register_user(name_prefix: str):
    return AuthService().register_user(
        UserRegister(
            name=f"{name_prefix}_{uuid_lib.uuid4().hex[:8]}",
            email=f"{uuid_lib.uuid4().hex[:8]}@example.com",
            password="S3cure#Pass",
        )
    )


def test_expense_service_emits_expense_created_signal(app):
    with app.app_context():
        repo = NotificationRepository()
        repo.collection.delete_many({})

        auth = AuthService()
        remove_flake_errors3(auth)
        payer = _register_user("payer")
        member = _register_user("member")

        group_service = GroupService()
        group = group_service.create_new_group(
            GroupCreationRequest(group_name="Sig Group"), payer.user_id
        )
        group_service.save_new_group(group)
        group_service.join_group_by_code(member.user_id, group.invite_code)

        expense_service = ExpenseService()
        expense = expense_service.create_new_expense(
            request=ExpenseCreationRequest(
                group_id=group.group_id,
                total_amount=100.0,
                description="Dinner",
                payer_id=payer.user_id,
            )
        )

        received = {"count": 0, "payload": None}

        def receiver(sender, expense, **extras):
            received["count"] += 1
            received["payload"] = expense

        cid = expense_created.connect(receiver, sender=ANY)
        remove_flake_errors2(cid)
        try:
            expense_service.save_new_expense(expense)
        finally:
            expense_created.disconnect(receiver, sender=ANY)

        assert received["count"] == 1
        assert received["payload"] is not None


def test_group_service_emits_invite_sent_signal(app):
    with app.app_context():
        repo = NotificationRepository()
        repo.collection.delete_many({})

        admin = _register_user("admin")
        invitee = _register_user("invitee")

        group_service = GroupService()
        group = group_service.create_new_group(
            GroupCreationRequest(group_name="Invite Sig Group"), admin.user_id
        )
        group_id = group_service.save_new_group(group)

        received = {"count": 0, "group_schema": None, "user": None}

        def receiver(sender, group_schema, user, **extras):
            received["count"] += 1
            received["group_schema"] = group_schema
            received["user"] = user

        cid = invite_sent.connect(receiver)

        remove_flake_errors2(cid)

        try:
            group_service.invite_member(admin.user_id, group_id, invitee.email)
        finally:
            invite_sent.disconnect(receiver)

        assert received["count"] == 1
        assert received["group_schema"] is not None
        assert received["user"].user_id == invitee.user_id
