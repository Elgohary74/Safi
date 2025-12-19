import unittest
from unittest.mock import MagicMock, patch

from flask import Flask

from app.controllers.expense_controller import ExpenseController
from app.models.expense import Expense, ExpenseCreationRequest
from app.models.user import User


class TestExpenseController(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.config["TESTING"] = True
        self.app.config["WTF_CSRF_ENABLED"] = False

        # Setup controller
        self.controller = ExpenseController()
        self.controller.expense_service = MagicMock()
        self.controller.current_user = User(
            user_id="user123",
            email="user@example.com",
            name="Test User",
            username="testuser",
        )

        # Register routes
        ExpenseController.register(self.app)

        # Setup test client
        self.client = self.app.test_client()

    def test_create_expense_success(self):
        # Arrange
        test_expense = Expense(
            expense_id="expense123",
            description="Test Expense",
            total_amount=100.0,
            date=MagicMock(),
            payer=MagicMock(),
            group=MagicMock(),
        )

        self.controller.expense_service.create_new_expense.return_value = test_expense
        self.controller.expense_service.save_new_expense.return_value = "expense123"

        form_data = {
            "group_id": "group123",
            "total_amount": "100.0",
            "description": "Test Expense",
            "payer_id": "user123",
        }

        # Mock request.referrer
        with self.app.test_request_context("/groups/group123/details"):
            with patch("flask.request.referrer", "/groups/group123/details"):
                # Act
                with patch.object(
                    ExpenseController,
                    "expense_service",
                    self.controller.expense_service,
                ):
                    with patch.object(
                        ExpenseController, "current_user", self.controller.current_user
                    ):
                        response = self.client.post("/expenses/create", data=form_data)

                # Assert
                self.assertEqual(response.status_code, 302)  # Redirect status code

                # Verify expense_service methods were called correctly
                self.controller.expense_service.create_new_expense.assert_called_once()

                # Verify the ExpenseCreationRequest was created correctly
                request_arg = (
                    self.controller.expense_service.create_new_expense.call_args[0][0]
                )
                self.assertIsInstance(request_arg, ExpenseCreationRequest)
                self.assertEqual(request_arg.group_id, "group123")
                self.assertEqual(request_arg.total_amount, 100.0)
                self.assertEqual(request_arg.description, "Test Expense")
                self.assertEqual(request_arg.payer_id, "user123")

                # Verify save_new_expense was called with the test_expense
                self.controller.expense_service.save_new_expense.assert_called_once_with(
                    test_expense
                )
