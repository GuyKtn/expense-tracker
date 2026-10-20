from dataclasses import dataclass, field
from datetime import date

@dataclass
class Point:
    x: float
    y: float = 0.0

@dataclass
class Visit:
    place: str
    day: date = field(default_factory=date.today)

@dataclass
class Expense:
    amount: float
    category: str
    note: str = ""
    day: date = field(default_factory=date.today)
    