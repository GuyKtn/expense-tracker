import sqlite3
from tracker.models import Expense
from datetime import date

class Database:
    def __init__(self, db_path: str):
        self.conn = sqlite3.connect(db_path)
        self._create_tables()

    def _create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                amount REAL NOT NULL,
                category TEXT NOT NULL,
                note TEXT,
                day DATE NOT NULL
            )
        ''')
        self.conn.commit()

    def add_expense(self, expense: Expense) -> int:
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO expenses (amount, category, note, day)
            VALUES (?, ?, ?, ?)
        ''', (expense.amount, expense.category, expense.note, expense.day.isoformat()))
        self.conn.commit()
        return cursor.lastrowid

    def get_expenses(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT amount, category, note, day FROM expenses')
        rows = cursor.fetchall()
        return [
    Expense(amount=amount, category=category, note=note, day=date.fromisoformat(day))
    for amount, category, note, day in rows]

    def summary_by_category(self) -> list[tuple[str, float]]:
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT category, SUM(amount)
            FROM expenses
            GROUP BY category
            ORDER BY SUM(amount) DESC
        """)
        return cursor.fetchall()
        

    def close(self):
        self.conn.close()