import unittest
from datetime import datetime
from unittest.mock import MagicMock

from app.models.expense import Expense, ExpenseCreationRequest, ExpenseSchema
from app.models.group import Group
from app.models.user import User
from app.services.expense import ExpenseService


class TestExpenseIntegration(unittest.TestCase):
    def setUp(self):
        # Setup service with mocked repositories
        self.expense_service = ExpenseService()
        self.expense_service.expense_repo = MagicMock()
        self.expense_service.group_repo = MagicMock()
        self.expense_service.user_repo = MagicMock()

        # Setup test data
        self.test_user = User(
            user_id="user123",
            email="user@example.com",
            name="Test User",
            username="testuser",
        )

        self.test_group = Group(
            group_id="group123",
            group_name="Test Group",
            description="Test Description",
            first_member=self.test_user,
            members=[self.test_user],
            working_invites=[],
            debts=[],
            invite_code="invite123",
            invite_code_expiry=datetime.now(),
        )

        # Setup the get_group and get_user methods to return test data
        self.expense_service.get_group = MagicMock(return_value=self.test_group)
        self.expense_service.get_user = MagicMock(return_value=self.test_user)

        # Setup the _convert_expense_to_schema method
        def convert_mock(expense):
            return ExpenseSchema(
                expense_id=expense.expense_id,
                description=expense.description,
                total_amount=expense.total_amount,
                date=expense.date,
                payer_id=expense.payer.user_id,
                group_id=expense.group.group_id,
            )

        self.expense_service._convert_expense_to_schema = MagicMock(
            side_effect=convert_mock
        )
        self.expense_service.expense_repo.add.return_value = "expense123"

    def test_create_and_save_expense_flow(self):
        """Test the full flow of creating and saving an expense"""
        # Create expense request
        expense_request = ExpenseCreationRequest(
            group_id="group123",
            total_amount=100.0,
            description="Test Expense",
            payer_id="user123",
        )

        # Create new expense
        expense = self.expense_service.create_new_expense(expense_request)

        # Verify expense was created correctly
        self.assertEqual(expense.description, "Test Expense")
        self.assertEqual(expense.total_amount, 100.0)
        self.assertEqual(expense.payer, self.test_user)
        self.assertEqual(expense.group, self.test_group)

        # Save the expense
        expense_id = self.expense_service.save_new_expense(expense)

        # Verify expense was saved correctly
        self.assertEqual(expense_id, "expense123")
        self.expense_service._convert_expense_to_schema.assert_called_once_with(expense)

        # Verify the converted schema was passed to the repository
        schema_arg = self.expense_service.expense_repo.add.call_args[0][0]
        self.assertEqual(schema_arg.description, "Test Expense")
        self.assertEqual(schema_arg.total_amount, 100.0)
        self.assertEqual(schema_arg.payer_id, "user123")
        self.assertEqual(schema_arg.group_id, "group123")

    def test_get_group_expenses_flow(self):
        """Test the flow of retrieving expenses for a group"""
        # Setup mock data for repository response
        expense_schema = ExpenseSchema(
            expense_id="expense123",
            description="Test Expense",
            total_amount=100.0,
            date=datetime.now(),
            payer_id="user123",
            group_id="group123",
        )
        self.expense_service.expense_repo.get_all_by_group.return_value = [
            expense_schema
        ]

        # Setup mock for converting schema to expense
        mock_expense = Expense(
            expense_id="expense123",
            description="Test Expense",
            total_amount=100.0,
            date=expense_schema.date,
            payer=self.test_user,
            group=self.test_group,
        )
        self.expense_service._convert_schema_to_expense = MagicMock(
            return_value=mock_expense
        )

        # Get expenses for group
        expenses = self.expense_service.get_group_expenses("group123")

        # Verify correct results
        self.assertEqual(len(expenses), 1)
        self.assertEqual(expenses[0].expense_id, "expense123")
        self.assertEqual(expenses[0].total_amount, 100.0)
        self.assertEqual(expenses[0].payer, self.test_user)
        self.assertEqual(expenses[0].group, self.test_group)

        # Verify repository was called correctly
        self.expense_service.expense_repo.get_all_by_group.assert_called_once_with(
            "group123"
        )
        self.expense_service._convert_schema_to_expense.assert_called_once_with(
            expense_schema
        )
