from datetime import date

import pytest

from tracker.database import Database
from tracker.models import Expense


@pytest.fixture
def db():
    database = Database(":memory:")
    yield database
    database.close()


def test_empty_database_has_no_expenses(db):
    assert db.get_expenses() == []


def test_add_expense_returns_id(db):
    first_id = db.add_expense(Expense(12.5, "food", "lunch"))
    second_id = db.add_expense(Expense(40, "transport"))
    assert first_id == 1
    assert second_id == 2

def test_summary_by_category(db):
    db.add_expense(Expense(10, "food"))
    db.add_expense(Expense(20, "food"))
    db.add_expense(Expense(15, "transport"))
    summary = db.summary_by_category()
    assert summary == [("food", 30), ("transport", 15)]

def test_date_is_a_date_object(db):
    expense = Expense(10, "food", day=date(2024, 1, 1))
    db.add_expense(expense)
    retrieved_expense = db.get_expenses()[0]
    assert isinstance(retrieved_expense.day, date)
    assert retrieved_expense.day == date(2024, 1, 1)

def test_saved_expense_comes_back_correctly(db):
    expense = Expense(10, "food", "lunch", date(2024, 1, 1))
    db.add_expense(expense)
    retrieved_expense = db.get_expenses()[0]

    assert len(db.get_expenses()) == 1
    assert retrieved_expense.amount == expense.amount
    assert retrieved_expense.category == expense.category
    assert retrieved_expense.note == expense.note
    assert retrieved_expense.day == expense.day