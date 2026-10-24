import argparse
import csv

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

    # "summary" command   
    sub.add_parser("summary", help="Totals per category")

    # "export" command
    export = sub.add_parser("export", help="Export expenses to CSV")
    export.add_argument("--output", default="expenses.csv", help="CSV file name")
    
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

        elif args.command == "summary":
            rows = db.summary_by_category()
            if not rows:
                print("No expenses yet.")
            for category, total in rows:
                print(f"{category:<12} {total:>8.2f}")

        elif args.command == "export":
            expenses = db.get_expenses()
            with open(args.output, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["amount", "category", "note", "day"])
                for e in expenses:
                    writer.writerow([e.amount, e.category, e.note, e.day.isoformat()])
            print(f"Exported {len(expenses)} expenses to {args.output}")
    finally:
        db.close()


if __name__ == "__main__":
    main()