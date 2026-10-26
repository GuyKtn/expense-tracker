import pytest

from tracker.models import Expense, ValidationError

def test_valid_expense():
    expense = Expense(10.0, "food", "lunch")
    assert expense.amount == 10.0
    assert expense.category == "food"

def test_negative_amount_is_rejected():
    with pytest.raises(ValidationError):
        Expense(-5, "food")

def test_empty_category_is_rejected():
    with pytest.raises(ValidationError):
        Expense(10, "")

def test_whitespace_category_is_rejected():
    with pytest.raises(ValidationError):
        Expense(10, "   ")

def test_zero_amount_is_rejected():
    with pytest.raises(ValidationError):
        Expense(0, "food")