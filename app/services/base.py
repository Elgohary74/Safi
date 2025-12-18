from app.models import Expense, ExpenseSchema, Group, GroupSchema
from app.repositories import ExpenseRepository, GroupRepository, UserRepository
from app.utils.exceptions import ResourceNotFound


class BaseService:
    def __init__(self):
        self.group_repo = GroupRepository()
        self.user_repo = UserRepository()
        self.expense_repo = ExpenseRepository()

    # Group Conversions
    def _convert_group_to_schema(self, group: Group) -> GroupSchema:
        return GroupSchema(
            group_name=group.group_name,
            description=group.description,
            first_member_id=group.first_member.user_id,
            group_id=group.group_id,
            members_ids=[member.user_id for member in group.members],
            working_invites=group.working_invites,
            debts=group.debts,
            invite_code=group.invite_code,
            invite_code_expiry=group.invite_code_expiry,
            pending_members=group.pending_members,
            past_members=group.past_members,
        )

    def _convert_schema_to_group(self, schema: GroupSchema) -> Group:
        first_member = self.user_repo.get_by_id(schema.first_member_id)
        members = [self.user_repo.get_by_id(uid) for uid in schema.members_ids]
        return Group(
            group_id=schema.group_id,
            group_name=schema.group_name,
            description=schema.description,
            first_member=first_member,
            members=members,
            working_invites=schema.working_invites,
            debts=schema.debts,
            invite_code=schema.invite_code,
            invite_code_expiry=schema.invite_code_expiry,
            pending_members=schema.pending_members_ids,
            past_members=schema.past_members_ids,
        )

    def get_group(self, group_id):
        group_data = self.group_repo.get_by_id(group_id)
        if not group_data:
            raise ResourceNotFound(message="Group not found")
        group = self._convert_schema_to_group(group_data)
        return group

    # User Conversions
    def get_user(self, user_id: str):
        return self.user_repo.get_by_id(user_id)

    # Expense Conversions
    def _convert_expense_to_schema(self, expense: Expense) -> ExpenseSchema:
        return ExpenseSchema(
            expense_id=expense.expense_id,
            description=expense.description,
            total_amount=expense.total_amount,
            group_id=expense.group.group_id,
            payer_id=expense.payer.user_id,
            date=expense.date,
        )

    def _convert_schema_to_expense(self, schema: ExpenseSchema) -> Expense:
        group = self.get_group(schema.group_id)
        payer = self.get_user(schema.payer_id)

        return Expense(
            expense_id=schema.expense_id,
            description=schema.description,
            total_amount=schema.total_amount,
            group=group,
            payer=payer,
            date=schema.date,
        )
