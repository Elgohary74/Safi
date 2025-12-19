import unittest
from datetime import datetime
from unittest.mock import MagicMock

from app.models.expense import Expense, ExpenseCreationRequest, ExpenseSchema
from app.models.group import Group
from app.models.user import User
from app.services.expense import ExpenseService
from app.utils.exceptions import CreationError


class TestExpenseService(unittest.TestCase):
    def setUp(self):
        self.expense_service = ExpenseService()

        # Mock dependencies
        self.expense_service.expense_repo = MagicMock()
        self.expense_service.group_repo = MagicMock()
        self.expense_service.user_repo = MagicMock()

        # Mock user and group
        self.mock_user = User(
            user_id="user123",
            email="user@example.com",
            name="Test User",
            username="testuser",
        )
        self.mock_group = Group(
            group_id="group123",
            group_name="Test Group",
            description="Test Description",
            first_member=self.mock_user,
            members=[self.mock_user],
            working_invites=[],
            debts=[],
            invite_code="invite123",
            invite_code_expiry=datetime.now(),
        )

    def test_create_new_expense_valid_data(self):
        # Arrange
        expense_request = ExpenseCreationRequest(
            group_id="group123",
            total_amount=100.0,
            description="Test Expense",
            payer_id="user123",
        )

        self.expense_service.get_group = MagicMock(return_value=self.mock_group)
        self.expense_service.get_user = MagicMock(return_value=self.mock_user)

        # Act
        expense = self.expense_service.create_new_expense(expense_request)

        # Assert
        self.assertEqual(expense.description, "Test Expense")
        self.assertEqual(expense.total_amount, 100.0)
        self.assertEqual(expense.payer, self.mock_user)
        self.assertEqual(expense.group, self.mock_group)
        self.expense_service.get_group.assert_called_once_with("group123")
        self.expense_service.get_user.assert_called_once_with("user123")

    def test_save_new_expense_success(self):
        # Arrange
        expense = Expense(
            expense_id="expense123",
            description="Test Expense",
            total_amount=100.0,
            date=datetime.now(),
            payer=self.mock_user,
            group=self.mock_group,
        )

        mock_schema = ExpenseSchema(
            expense_id="expense123",
            description="Test Expense",
            total_amount=100.0,
            date=expense.date,
            payer_id="user123",
            group_id="group123",
        )

        self.expense_service._convert_expense_to_schema = MagicMock(
            return_value=mock_schema
        )
        self.expense_service.expense_repo.add.return_value = "expense123"

        # Act
        expense_id = self.expense_service.save_new_expense(expense)

        # Assert
        self.assertEqual(expense_id, "expense123")
        self.expense_service._convert_expense_to_schema.assert_called_once_with(expense)
        self.expense_service.expense_repo.add.assert_called_once_with(mock_schema)

    def test_save_new_expense_failure(self):
        # Arrange
        expense = Expense(
            expense_id="expense123",
            description="Test Expense",
            total_amount=100.0,
            date=datetime.now(),
            payer=self.mock_user,
            group=self.mock_group,
        )

        mock_schema = ExpenseSchema(
            expense_id="expense123",
            description="Test Expense",
            total_amount=100.0,
            date=expense.date,
            payer_id="user123",
            group_id="group123",
        )

        self.expense_service._convert_expense_to_schema = MagicMock(
            return_value=mock_schema
        )
        self.expense_service.expense_repo.add.return_value = None

        # Act & Assert
        with self.assertRaises(CreationError) as context:
            self.expense_service.save_new_expense(expense)

        self.assertEqual(str(context.exception.message), "Failed to create expense")

    def test_get_group_expenses(self):
        # Arrange
        expense_schema = ExpenseSchema(
            expense_id="expense123",
            description="Test Expense",
            total_amount=100.0,
            date=datetime.now(),
            payer_id="user123",
            group_id="group123",
        )

        mock_expense = Expense(
            expense_id="expense123",
            description="Test Expense",
            total_amount=100.0,
            date=expense_schema.date,
            payer=self.mock_user,
            group=self.mock_group,
        )

        self.expense_service.expense_repo.get_all_by_group.return_value = [
            expense_schema
        ]
        self.expense_service._convert_schema_to_expense = MagicMock(
            return_value=mock_expense
        )

        # Act
        expenses = self.expense_service.get_group_expenses("group123")

        # Assert
        self.assertEqual(len(expenses), 1)
        self.assertEqual(expenses[0], mock_expense)
        self.expense_service.expense_repo.get_all_by_group.assert_called_once_with(
            "group123"
        )
        self.expense_service._convert_schema_to_expense.assert_called_once_with(
            expense_schema
        )
