import uuid as uuid_lib

from app.models import GroupCreationRequest
from app.models.expense import Expense
from app.models.shared_expense import SharedExpense
from app.models.user import UserRegister
from app.repositories.notification_repo import NotificationRepository
from app.services import AuthService, ExpenseService, GroupService


def remove_flake_errors(auth: AuthService):
    pass


def _register_user(name_prefix: str):
    return AuthService().register_user(
        UserRegister(
            name=f"{name_prefix}_{uuid_lib.uuid4().hex[:8]}",
            email=f"{uuid_lib.uuid4().hex[:8]}@example.com",
            password="S3cure#Pass",
        )
    )


def test_expense_observer_creates_notifications_for_participants(app):
    with app.app_context():
        notif_repo = NotificationRepository()
        notif_repo.collection.delete_many({})

        auth = AuthService()
        remove_flake_errors(auth)
        payer = _register_user("payer")
        u1 = _register_user("u1")
        u2 = _register_user("u2")

        group_service = GroupService()
        group = group_service.create_new_group(
            GroupCreationRequest(group_name="Observer Group"), payer.user_id
        )
        group = group_service.get_group(group_service.save_new_group(group))
        group_service.join_group_by_code(u1.user_id, group.invite_code)
        group_service.join_group_by_code(u2.user_id, group.invite_code)

        # Build expense with splits for u1 and u2 (excluding payer)
        exp_service = ExpenseService()
        expense = Expense(
            description="Lunch",
            total_amount=150.0,
            date=__import__("datetime", fromlist=["datetime"]).datetime.now(),
            payer=payer,
            group=group,
        )
        expense.splits = [
            SharedExpense(amount=50.0, participant=u1),
            SharedExpense(amount=100.0, participant=u2),
        ]

        exp_service.save_new_expense(expense)

        # Verify notifications were created for u1 and u2 (not payer)
        n1 = notif_repo.get_unread_by_user(u1.user_id)
        n2 = notif_repo.get_unread_by_user(u2.user_id)
        npayer = notif_repo.get_unread_by_user(payer.user_id)

        assert len(n1) == 1
        assert len(n2) == 1
        assert len(npayer) == 0
