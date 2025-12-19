import unittest
from datetime import datetime
from unittest.mock import MagicMock

from app.models.expense import ExpenseSchema
from app.models.shared_expense import SharedExpenseSchema
from app.repositories.expense_repo import ExpenseRepository


class TestExpenseRepository(unittest.TestCase):
    def setUp(self):
        self.expense_repo = ExpenseRepository()
        self.expense_repo.collection = MagicMock()
        self.expense_repo.logger = MagicMock()

        self.test_expense = ExpenseSchema(
            expense_id="expense123",
            description="Test Expense",
            total_amount=100.0,
            date=datetime.now(),
            payer_id="user123",
            group_id="group123",
            splits=[
                SharedExpenseSchema(
                    participant_id="user456", amount=50.0, status="unpaid"
                ),
                SharedExpenseSchema(
                    participant_id="user789", amount=50.0, status="unpaid"
                ),
            ],
        )

    def test_add_expense(self):
        # Arrange
        self.expense_repo.collection.insert_one.return_value = MagicMock(
            inserted_id="expense123"
        )

        # Act
        result = self.expense_repo.add(self.test_expense)

        # Assert
        self.assertEqual(result, "expense123")
        self.expense_repo.collection.insert_one.assert_called_once()
        self.expense_repo.logger.info.assert_called_once()

    def test_get_by_id_found(self):
        # Arrange
        mock_data = self.test_expense.model_dump()
        self.expense_repo.collection.find_one.return_value = mock_data

        # Act
        result = self.expense_repo.get_by_id("expense123")

        # Assert
        self.assertIsNotNone(result)
        self.assertEqual(result.expense_id, "expense123")
        self.assertEqual(result.total_amount, 100.0)
        self.expense_repo.collection.find_one.assert_called_once_with(
            {"_id": "expense123"}
        )
        self.expense_repo.logger.debug.assert_called_once()

    def test_get_by_id_not_found(self):
        # Arrange
        self.expense_repo.collection.find_one.return_value = None

        # Act
        result = self.expense_repo.get_by_id("nonexistent")

        # Assert
        self.assertIsNone(result)
        self.expense_repo.collection.find_one.assert_called_once_with(
            {"_id": "nonexistent"}
        )
        self.expense_repo.logger.debug.assert_called_once()

    def test_get_all_by_group(self):
        # Arrange
        mock_cursor = [self.test_expense.model_dump()]
        self.expense_repo.collection.find.return_value = mock_cursor

        # Act
        results = self.expense_repo.get_all_by_group("group123")

        # Assert
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].expense_id, "expense123")
        self.assertEqual(results[0].group_id, "group123")
        self.expense_repo.collection.find.assert_called_once_with(
            {"group_id": "group123"}
        )
        self.expense_repo.logger.debug.assert_called_once()

    def test_update(self):
        # Arrange

        # Act
        self.expense_repo.update("expense123", self.test_expense)

        # Assert
        self.expense_repo.collection.update_one.assert_called_once_with(
            {"_id": "expense123"}, {"$set": self.test_expense.model_dump()}
        )
        self.expense_repo.logger.info.assert_called_once()

    def test_delete(self):
        # Arrange

        # Act
        self.expense_repo.delete("expense123")

        # Assert
        self.expense_repo.collection.delete_one.assert_called_once_with(
            {"_id": "expense123"}
        )
        self.expense_repo.logger.info.assert_called_once()
