from app.events.signals import (
    confirmation_requested,
    expense_created,
    invite_sent,
    transaction_confirmed,
)
from app.models import Expense, GroupSchema, NotificationSchema, Transaction, User
from app.repositories import NotificationRepository


def handle_involved_users(sender, expense: Expense, **extra):
    notify_repo = NotificationRepository()

    for shared_expense in expense.splits:
        if shared_expense.participant.user_id != expense.payer.user_id:
            message = (
                f"{expense.payer.name} has paid a new expense of {expense.total_amount}EGP Total"
                f"Description: {expense.description}. "
                f"you should participate with {shared_expense.amount}EGP in this expense."
            )
            notification = NotificationSchema(
                user_id=shared_expense.participant.user_id,
                message=message,
                timestamp=expense.date,
            )
            notify_repo.add(notification)


def handle_User_invite(sender, group_schema: GroupSchema, user: User, **extra):
    notify_repo = NotificationRepository()

    notification = NotificationSchema(
        user_id=user.user_id,
        message=f"You have been invited to join group: {group_schema.group_name}",
        type="invite",
        payload={
            "group_id": group_schema.group_id,
            "group_name": group_schema.group_name,
            "first_member": group_schema.first_member_id,
        },
    )
    notify_repo.add(notification)


def handle_confirmation_requested(sender, transaction: Transaction, **extra):
    notify_repo = NotificationRepository()

    message = (
        f"{transaction.payer.name} has made a transaction of {transaction.amount}EGP."
        f"Did you receive it?"
    )

    notification = NotificationSchema(
        user_id=transaction.receiver.user_id,
        message=message,
        type="confirmation",
        payload={"transaction_id": transaction.transaction_id},
    )
    notify_repo.add(notification)


def handle_transaction_confirmed(sender, transaction: Transaction, **extra):
    notify_repo = NotificationRepository()

    message = f"Your transaction of {transaction.amount}EGP to {transaction.receiver.name} has been confirmed."

    notification = NotificationSchema(
        user_id=transaction.payer.user_id,
        message=message,
        payload={"transaction_id": transaction.transaction_id},
    )
    notify_repo.add(notification)


def enable_notifications(app):
    expense_created.connect(handle_involved_users)
    invite_sent.connect(handle_User_invite)
    confirmation_requested.connect(handle_confirmation_requested)
    transaction_confirmed.connect(handle_transaction_confirmed)
