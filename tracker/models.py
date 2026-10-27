from dataclasses import dataclass, field
from datetime import date


class ValidationError(Exception):
    
    """Exception raised for invalid expense data."""
    pass

@dataclass
class Expense:
    amount: float
    category: str
    note: str = ""
    day: date = field(default_factory=date.today)

    def __post_init__(self):
        if self.amount <= 0:
            raise ValidationError("Amount must be positive")
        if not self.category.strip():
            raise ValidationError("Category cannot be empty")


