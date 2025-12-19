import unittest
from datetime import datetime

from app.models.expense import Expense, ExpenseCreationRequest, ExpenseSchema
from app.models.group import Group
from app.models.shared_expense import SharedExpenseSchema
from app.models.user import User


class TestExpenseModels(unittest.TestCase):
    def setUp(self):
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

    def test_expense_creation_request(self):
        # Act
        expense_request = ExpenseCreationRequest(
            group_id="group123",
            total_amount=100.0,
            description="Test Expense",
            payer_id="user123",
        )

        # Assert
        self.assertEqual(expense_request.group_id, "group123")
        self.assertEqual(expense_request.total_amount, 100.0)
        self.assertEqual(expense_request.description, "Test Expense")
        self.assertEqual(expense_request.payer_id, "user123")

    def test_expense(self):
        # Arrange
        current_time = datetime.now()

        # Act
        expense = Expense(
            expense_id="expense123",
            description="Test Expense",
            total_amount=100.0,
            date=current_time,
            payer=self.test_user,
            group=self.test_group,
        )

        # Assert
        self.assertEqual(expense.expense_id, "expense123")
        self.assertEqual(expense.description, "Test Expense")
        self.assertEqual(expense.total_amount, 100.0)
        self.assertEqual(expense.date, current_time)
        self.assertEqual(expense.payer, self.test_user)
        self.assertEqual(expense.group, self.test_group)
        self.assertEqual(expense.splits, [])

    def test_expense_schema(self):
        # Arrange
        current_time = datetime.now()

        shared_expense_schema1 = SharedExpenseSchema(
            participant_id="user456", amount=50.0, status="unpaid"
        )

        shared_expense_schema2 = SharedExpenseSchema(
            participant_id="user789", amount=50.0, status="unpaid"
        )

        # Act
        expense_schema = ExpenseSchema(
            expense_id="expense123",
            description="Test Expense",
            total_amount=100.0,
            date=current_time,
            payer_id="user123",
            group_id="group123",
            splits=[shared_expense_schema1, shared_expense_schema2],
        )

        # Assert
        self.assertEqual(expense_schema.expense_id, "expense123")
        self.assertEqual(expense_schema.description, "Test Expense")
        self.assertEqual(expense_schema.total_amount, 100.0)
        self.assertEqual(expense_schema.date, current_time)
        self.assertEqual(expense_schema.payer_id, "user123")
        self.assertEqual(expense_schema.group_id, "group123")
        self.assertEqual(len(expense_schema.splits), 2)
        self.assertEqual(expense_schema.splits[0].participant_id, "user456")
        self.assertEqual(expense_schema.splits[0].amount, 50.0)
        self.assertEqual(expense_schema.splits[1].participant_id, "user789")

    def test_auto_generated_expense_id(self):
        # Act
        expense1 = Expense(
            description="Test Expense 1",
            total_amount=100.0,
            date=datetime.now(),
            payer=self.test_user,
            group=self.test_group,
        )

        expense2 = Expense(
            description="Test Expense 2",
            total_amount=200.0,
            date=datetime.now(),
            payer=self.test_user,
            group=self.test_group,
        )

        # Assert
        self.assertIsNotNone(expense1.expense_id)
        self.assertIsNotNone(expense2.expense_id)
        self.assertNotEqual(expense1.expense_id, expense2.expense_id)
