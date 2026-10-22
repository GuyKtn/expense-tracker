import argparse

from tracker.database import Database
from tracker.models import Expense
from datetime import date


def main():
    parser = argparse.ArgumentParser(description="Expense tracker")
    sub = parser.add_subparsers(dest="command", required=True)

    # "add" command
    add = sub.add_parser("add", help="Add an expense")
    add.add_argument("amount", type=float, help="Amount spent")
    add.add_argument("--category", required=True, help="For example: food")
    add.add_argument("--note", default="", help="Optional note")
    add.add_argument("--day", type=date.fromisoformat, help="YYYY-MM-DD (default: today)")

    # "list" command
    sub.add_parser("list", help="List all expenses")

    args = parser.parse_args()

    db = Database("expenses.db")
    try:
        if args.command == "add":
            if args.day is None:
                expense = Expense(args.amount, args.category, args.note)
            else:
                expense = Expense(args.amount, args.category, args.note, args.day)
            new_id = db.add_expense(expense)
            print(f"Added expense #{new_id}")

        elif args.command == "list":
            expenses = db.get_expenses()
            if not expenses:
                print("No expenses yet.")
            for e in expenses:
                print(f"{e.day}  {e.category:<12} {e.amount:>8.2f}  {e.note}")
            print(f"Total: {sum(e.amount for e in expenses):>8.2f}")
    finally:
        db.close()


if __name__ == "__main__":
    main()