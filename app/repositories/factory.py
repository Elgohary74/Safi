from app.repositories.expense_repo import ExpenseRepository
from app.repositories.group_repo import GroupRepository
from app.repositories.notification_repo import NotificationRepository
from app.repositories.transaction_repo import TransactionRepository
from app.repositories.user_repo import UserRepository


class RepositoryFactory:
    @staticmethod
    def get_repository(repo_type: str):
        repo_type = repo_type.lower().strip()

        if repo_type == "user":
            return UserRepository()
        elif repo_type == "group":
            return GroupRepository()
        elif repo_type == "expense":
            return ExpenseRepository()
        elif repo_type == "transaction":
            return TransactionRepository()
        elif repo_type == "notification":
            return NotificationRepository()
        else:
            raise ValueError(f"Unknown repository type: {repo_type}")
